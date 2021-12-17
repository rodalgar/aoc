import pytest

from Main import raw_input_to_strbin, strbin_to_packet

# TESTS PART 1
raw_test_data_1 = 'D2FE28'
"""Example of one literal packet, 3 segments"""

raw_test_data_2 = '38006F45291200'
"""Example of one operator packet, 2 literal subpackets, length in bits"""

raw_test_data_3 = 'EE00D40C823060'
"""Example of one operator packet, 3 literal subpackets, length in packets"""

raw_test_data_4 = '8A004A801A8002F478'
"""Represents an operator packet (version 4) which contains an operator packet (version 1) which contains an operator 
packet (version 5) which contains a literal value (version 6); this packet has a version sum of 16. """

raw_test_data_5 = '620080001611562C8802118E34'
"""represents an operator packet (version 3) which contains two sub-packets; each sub-packet is an operator packet 
that contains two literal values. This packet has a version sum of 12. """

raw_test_data_6 = 'C0015000016115A2E0802F182340'
"""has the same structure as the previous example, but the outermost packet uses a different length type ID. This 
packet has a version sum of 23. """

raw_test_data_7 = 'A0016C880162017C3686B18A3D4780'
"""is an operator packet that contains an operator packet that contains an operator packet that contains five literal 
values; it has a version sum of 31. """


def get_test_input(string):
    return raw_input_to_strbin(string)


@pytest.mark.parametrize("test_data, expected", [
    (raw_test_data_1, '110100101111111000101000'),
    (raw_test_data_2, '00111000000000000110111101000101001010010001001000000000'),
    (raw_test_data_3, '11101110000000001101010000001100100000100011000001100000'),
    (raw_test_data_4, '100010100000000001001010100000000001101010000000000000101111010001111000'),
    (raw_test_data_5,
     '01100010000000001000000000000000000101100001000101010110001011001000100000000010000100011000111000110100'),
    (raw_test_data_6,
     '11000000000000010101000000000000000000010110000100010101101000101110000010000000001011'
     '11000110000010001101000000'),
    (raw_test_data_7,
     '101000000000000101101100100010000000000101100010000000010111110000110110100001101011000'
     '110001010001111010100011110000000'),
])
def test_raw_input_to_strbin(test_data, expected):
    data = raw_input_to_strbin(test_data)
    assert data == expected


@pytest.mark.parametrize("test_data, expected, expected_versions", [
    (raw_test_data_1, 'P[version6,type_id4][AV: 6]. LIT(2021)', 6),
    (raw_test_data_2, '<P[version1,type_id6][AV: 9]. OPER(P[version6,type_id4][AV: 6]. LIT(10),'
                      'P[version2,type_id4][AV: 2]. LIT(20))', 9),
    (raw_test_data_3, 'MAXP[version7,type_id3][AV: 14]. OPER(P[version2,type_id4][AV: 2]. LIT(1),'
                      'P[version4,type_id4][AV: 4]. LIT(2),P[version1,type_id4][AV: 1]. LIT(3))', 14),
    (raw_test_data_4, 'MINP[version4,type_id2][AV: 16]. OPER(MINP[version1,type_id2][AV: 12]. '
                      'OPER(MINP[version5,type_id2][AV: 11]. OPER(P[version6,type_id4][AV: 6]. LIT(15))))', 16),
    (raw_test_data_5, 'SUP[version3,type_id0][AV: 12]. OPER(SUP[version0,type_id0][AV: 5]. '
                      'OPER(P[version0,type_id4][AV: 0]. LIT(10),P[version5,type_id4][AV: 5]. LIT(11)),'
                      'SUP[version1,type_id0][AV: 4]. OPER(P[version0,type_id4][AV: 0]. LIT(12),'
                      'P[version3,type_id4][AV: 3]. LIT(13)))', 12),
    (raw_test_data_6, 'SUP[version6,type_id0][AV: 23]. OPER(SUP[version0,type_id0][AV: 6]. '
                      'OPER(P[version0,type_id4][AV: 0]. LIT(10),P[version6,type_id4][AV: 6]. LIT(11)),'
                      'SUP[version4,type_id0][AV: 11]. OPER(P[version7,type_id4][AV: 7]. LIT(12),'
                      'P[version0,type_id4][AV: 0]. LIT(13)))', 23),
    (raw_test_data_7, 'SUP[version5,type_id0][AV: 31]. OPER(SUP[version1,type_id0][AV: 26]. '
                      'OPER(SUP[version3,type_id0][AV: 25]. OPER(P[version7,type_id4][AV: 7]. LIT(6),'
                      'P[version6,type_id4][AV: 6]. LIT(6),P[version5,type_id4][AV: 5]. LIT(12),'
                      'P[version2,type_id4][AV: 2]. LIT(15),P[version2,type_id4][AV: 2]. LIT(15))))', 31),
])
def test_strbin_to_packet(test_data, expected, expected_versions):
    input_data = get_test_input(test_data)
    data = strbin_to_packet(input_data)
    assert data[0].__repr__() == expected
    assert data[0].get_all_versions() == expected_versions


# TESTS PART 2
test_part2_ej1 = 'C200B40A82'
test_part2_ej2 = '04005AC33890'
test_part2_ej3 = '880086C3E88112'
test_part2_ej4 = 'CE00C43D881120'
test_part2_ej5 = 'D8005AC2A8F0'
test_part2_ej6 = 'F600BC2D8F'
test_part2_ej7 = '9C005AC2F8F0'
test_part2_ej8 = '9C0141080250320F1802104A08'


@pytest.mark.parametrize("test_data, expected", [
    (test_part2_ej1, 3),
    (test_part2_ej2, 54),
    (test_part2_ej3, 7),
    (test_part2_ej4, 9),
    (test_part2_ej5, 1),
    (test_part2_ej6, 0),
    (test_part2_ej7, 0),
    (test_part2_ej8, 1)
])
def test_evaluate(test_data, expected):
    input_data = get_test_input(test_data)
    data = strbin_to_packet(input_data)
    assert data[0].evaluate() == expected
