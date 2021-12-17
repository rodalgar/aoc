from __future__ import annotations

import operator
from functools import reduce

from Utils import bin_to_str, bin_to_dec


class Packet:
    PACKET_TYPE_LITERAL = 4
    PACKET_TYPE_OPERATOR_SUM = 0
    PACKET_TYPE_OPERATOR_PRODUCT = 1
    PACKET_TYPE_OPERATOR_MINIMUM = 2
    PACKET_TYPE_OPERATOR_MAXIMUM = 3
    PACKET_TYPE_OPERATOR_GREATER_THAN = 5
    PACKET_TYPE_OPERATOR_LESS_THAN = 6
    PACKET_TYPE_OPERATOR_EQUAL_TO = 7

    SUB_PACKET_TYPE_MORE_GROUPS = 1
    SUB_PACKET_TYPE_LAST_GROUP = 0

    version = None
    type_id = None

    def __init__(self, version, type_id):
        self.type_id = type_id
        self.version = version

    def read_packet_data(self, strbin_in: str, index: int, discard_excess: bool) -> int:
        return index

    @staticmethod
    def discard_excess(strbin_in: str, index: int) -> int:
        remaining = index % 4
        if remaining != 0:
            whole = index // 4
            excess = (whole * 4) - 1
            str_excess, index = bin_to_str(strbin_in, index, excess)
        else:
            excess = len(strbin_in) - index
            str_excess, index = bin_to_str(strbin_in, index, excess)
        return index

    def get_all_versions(self) -> int:
        return self.version

    def evaluate(self) -> int:
        pass

    def __repr__(self):
        return f"P[version{self.version},type_id{self.type_id}][AV: {self.get_all_versions()}]"

    @staticmethod
    def packet_factory(version: int, type_id: int) -> Packet:
        # LITERAL
        if type_id == Packet.PACKET_TYPE_LITERAL:
            return LiteralPacket(version, type_id)
        # OPERATORS
        if type_id == Packet.PACKET_TYPE_OPERATOR_SUM:
            return SumOperatorPacket(version, type_id)
        if type_id == Packet.PACKET_TYPE_OPERATOR_PRODUCT:
            return ProductOperatorPacket(version, type_id)
        if type_id == Packet.PACKET_TYPE_OPERATOR_MINIMUM:
            return MinimumOperatorPacket(version, type_id)
        if type_id == Packet.PACKET_TYPE_OPERATOR_MAXIMUM:
            return MaximumOperatorPacket(version, type_id)
        if type_id == Packet.PACKET_TYPE_OPERATOR_GREATER_THAN:
            return GreaterThanOperatorPacket(version, type_id)
        if type_id == Packet.PACKET_TYPE_OPERATOR_LESS_THAN:
            return LessThanOperatorPacket(version, type_id)
        if type_id == Packet.PACKET_TYPE_OPERATOR_EQUAL_TO:
            return EqualToOperatorPacket(version, type_id)

        # Not literal nor operator..... :D
        return Packet(version, type_id)


class LiteralPacket(Packet):
    literal_value = None

    def read_packet_data(self, strbin_in: str, index: int, discard_excess: bool) -> int:
        done_reading_packet = False
        strbin_packet_content = ''
        while not done_reading_packet:
            type_of_subpacket, index = bin_to_dec(strbin_in, index, 1)
            subpacket_group_content, index = bin_to_str(strbin_in, index, 4)
            strbin_packet_content += subpacket_group_content
            done_reading_packet = type_of_subpacket == Packet.SUB_PACKET_TYPE_LAST_GROUP

        self.literal_value = int(strbin_packet_content, 2)

        if discard_excess:
            index = self.discard_excess(strbin_in, index)
        return index

    def __repr__(self):
        msg = super().__repr__()
        return f"{msg}. LIT({self.literal_value})"

    def evaluate(self) -> int:
        return self.literal_value


class OperatorPacket(Packet):
    LENGTH_TYPE_IN_BITS = 0
    LENGTH_TYPE_IN_PACKETS = 1

    sub_packets = None

    def __init__(self, version: int, type_id: int):
        super().__init__(version, type_id)
        self.sub_packets = []

    def read_packet_data(self, strbin_in: str, index: int, discard_excess: bool) -> int:
        length_type_id, index = bin_to_dec(strbin_in, index, 1)
        sub_packets = []
        if length_type_id == OperatorPacket.LENGTH_TYPE_IN_BITS:
            length_in_bits, index = bin_to_dec(strbin_in, index, 15)
            limit = index + length_in_bits
            while index < limit:
                version, index = bin_to_dec(strbin_in, index, 3)
                type_id, index = bin_to_dec(strbin_in, index, 3)
                sub_packet = Packet.packet_factory(version, type_id)
                index = sub_packet.read_packet_data(strbin_in, index, discard_excess=False)
                sub_packets.append(sub_packet)

        elif length_type_id == OperatorPacket.LENGTH_TYPE_IN_PACKETS:
            length_in_packets, index = bin_to_dec(strbin_in, index, 11)
            for n_packet in range(length_in_packets):
                version, index = bin_to_dec(strbin_in, index, 3)
                type_id, index = bin_to_dec(strbin_in, index, 3)
                sub_packet = Packet.packet_factory(version, type_id)
                index = sub_packet.read_packet_data(strbin_in, index, discard_excess=False)
                sub_packets.append(sub_packet)

        if discard_excess:
            index = Packet.discard_excess(strbin_in, index)
        self.sub_packets = sub_packets

        return index

    def get_all_versions(self) -> int:
        sub_versions = 0
        for sub in self.sub_packets:
            sub_versions += sub.get_all_versions()
        return self.version + sub_versions

    def __repr__(self):
        msg = super().__repr__()
        return f"{msg}. OPER({','.join(map(lambda x: x.__repr__(), self.sub_packets))})"


class SumOperatorPacket(OperatorPacket):
    def evaluate(self) -> int:
        return reduce(operator.add, map(lambda x: x.evaluate(), self.sub_packets))

    def __repr__(self):
        msg = super().__repr__()
        return f"SU{msg}"


class ProductOperatorPacket(OperatorPacket):
    def evaluate(self) -> int:
        product = 1
        for subpacket_value in map(lambda x: x.evaluate(), self.sub_packets):
            product *= subpacket_value
        return product

    def __repr__(self):
        msg = super().__repr__()
        return f"PR{msg}"


class MinimumOperatorPacket(OperatorPacket):
    def evaluate(self) -> int:
        return min(map(lambda x: x.evaluate(), self.sub_packets))

    def __repr__(self):
        msg = super().__repr__()
        return f"MIN{msg}"


class MaximumOperatorPacket(OperatorPacket):
    def evaluate(self) -> int:
        return max(map(lambda x: x.evaluate(), self.sub_packets))

    def __repr__(self):
        msg = super().__repr__()
        return f"MAX{msg}"


class GreaterThanOperatorPacket(OperatorPacket):
    def evaluate(self) -> int:
        return 1 if self.sub_packets[0].evaluate() > self.sub_packets[1].evaluate() else 0
    def __repr__(self):
        msg = super().__repr__()
        return f">{msg}"


class LessThanOperatorPacket(OperatorPacket):
    def evaluate(self) -> int:
        return 1 if self.sub_packets[0].evaluate() < self.sub_packets[1].evaluate() else 0

    def __repr__(self):
        msg = super().__repr__()
        return f"<{msg}"


class EqualToOperatorPacket(OperatorPacket):
    def evaluate(self) -> int:
        return 1 if self.sub_packets[0].evaluate() == self.sub_packets[1].evaluate() else 0

    def __repr__(self):
        msg = super().__repr__()
        return f"=={msg}"
