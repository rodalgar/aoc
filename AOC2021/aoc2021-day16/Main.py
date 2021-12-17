# Day 16: Packet Decoder
from __future__ import annotations
from typing import List

from Packet import Packet
from Utils import bin_to_dec

conversion_table = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'
}


def raw_input_to_strbin(raw_hex_input: str) -> str:
    return ''.join(map(lambda x: conversion_table[x], raw_hex_input))


def strbin_to_packet(strbin_in: str) -> List[Packet]:
    index = 0
    limit = len(strbin_in)
    packets = []

    while index < limit:
        version, index = bin_to_dec(strbin_in, index, 3)
        type_id, index = bin_to_dec(strbin_in, index, 3)
        packet = Packet.packet_factory(version, type_id)
        index = packet.read_packet_data(strbin_in, index, discard_excess=True)

        packets.append(packet)

    return packets


if __name__ == '__main__':
    with open('data/aoc2021-input-day16.txt', 'r') as f:
        sol_raw_instructions = f.readline().strip('\n')

    sol_packets = strbin_to_packet(raw_input_to_strbin(sol_raw_instructions))

    # PART 1
    print('PART 1')
    print('>>>SOLUTION', sol_packets[0].get_all_versions())

    # PART 2
    print('PART 2')
    print('>>>SOLUTION:', sol_packets[0].evaluate())
