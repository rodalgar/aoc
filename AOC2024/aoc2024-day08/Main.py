# Day 8: Resonant Collinearity
from collections import namedtuple

Antenna = namedtuple('Antenna', 'id row col')
Antinode = namedtuple('Antinode', 'id l_antenna r_antenna row col')


def parse_input(raw_data: [str]) -> ({str: [Antenna]}, (int, int)):
    frequencies = {}
    for ix_row, line in enumerate(raw_data):
        for ix_col in range(len(line)):
            symbol = line[ix_col]
            if symbol != '.':
                if symbol not in frequencies:
                    frequencies[symbol] = []
                frequencies[symbol].append(Antenna(len(frequencies[symbol]), ix_row, ix_col))
    map_geometry = len(raw_data), len(raw_data[0])
    return frequencies, map_geometry


def calculate_distances(frequencies: {str: [Antenna]}) -> {str: [(int, int, int, int)]}:
    distances = {}
    for frequency in frequencies:
        antennas = frequencies[frequency]
        distances[frequency] = []
        for i in range(len(antennas)):
            for j in range(i + 1, len(antennas)):
                distance = (i, j, antennas[i].row - antennas[j].row, antennas[i].col - antennas[j].col)
                distances[frequency].append(distance)
    return distances


def calculate_antinodes(all_antennas: {str: [Antenna]},
                        all_distances: {str: [(int, int, int, int)]},
                        map_geometry: (int, int)
                        ) -> {str: [Antinode]}:
    antinodes = {}
    for frequency in all_distances:
        distances = all_distances[frequency]
        antennas = all_antennas[frequency]
        antinodes[frequency] = []
        for distance in distances:
            l_antenna = antennas[distance[0]]
            r_antenna = antennas[distance[1]]
            l_antinode = Antinode(len(antinodes[frequency]), l_antenna.id, r_antenna.id, l_antenna.row + distance[2],
                                  l_antenna.col + distance[3])
            if (0 <= l_antinode.row < map_geometry[0]) and (0 <= l_antinode.col < map_geometry[1]):
                antinodes[frequency].append(l_antinode)
            r_antinode = Antinode(len(antinodes[frequency]), l_antenna.id, r_antenna.id, r_antenna.row - distance[2],
                                  r_antenna.col - distance[3])
            if (0 <= r_antinode.row < map_geometry[0]) and (0 <= r_antinode.col < map_geometry[1]):
                antinodes[frequency].append(r_antinode)
    return antinodes


def calculate_impact(all_antinodes: {str: [Antinode]}) -> {(int, int)}:
    impact = set()

    for frequency, antinodes in all_antinodes.items():
        for antinode in antinodes:
            impact.add((antinode.row, antinode.col))
    return impact


def part1(all_frequencies: {str: [Antenna]}, map_geometry: (int, int)) -> int:
    distances = calculate_distances(all_frequencies)
    antinodes = calculate_antinodes(all_frequencies, distances, map_geometry)
    impact = calculate_impact(antinodes)
    return len(impact)


# PART 2
def calculate_antinodes_with_resonance(all_antennas: {str: [Antenna]},
                                       all_distances: {str: [(int, int, int, int)]},
                                       map_geometry: (int, int)
                                       ) -> {str: [Antinode]}:
    antinodes = {}
    for frequency in all_distances:
        distances = all_distances[frequency]
        antennas = all_antennas[frequency]
        antinodes[frequency] = []
        antennas_generating_antinodes = set()
        for distance in distances:
            l_antenna = antennas[distance[0]]
            r_antenna = antennas[distance[1]]

            # we save the two antennas to resonate between them even though they would not generate any antinode due to
            # be too close to the map boundaries
            antennas_generating_antinodes.add(l_antenna)
            antennas_generating_antinodes.add(r_antenna)

            # Calculation of left antinode, resonating in the same direction till the end of time
            l_antinode = Antinode(len(antinodes[frequency]), l_antenna.id, r_antenna.id, l_antenna.row + distance[2],
                                  l_antenna.col + distance[3])
            while (0 <= l_antinode.row < map_geometry[0]) and (0 <= l_antinode.col < map_geometry[1]):
                antinodes[frequency].append(l_antinode)
                l_antinode = Antinode(len(antinodes[frequency]), l_antenna.id, r_antenna.id,
                                      l_antinode.row + distance[2],
                                      l_antinode.col + distance[3])

            # Calculation of right antinode, resonating in the same direction till the end of time
            r_antinode = Antinode(len(antinodes[frequency]), l_antenna.id, r_antenna.id, r_antenna.row - distance[2],
                                  r_antenna.col - distance[3])
            while (0 <= r_antinode.row < map_geometry[0]) and (0 <= r_antinode.col < map_geometry[1]):
                antinodes[frequency].append(r_antinode)
                r_antinode = Antinode(len(antinodes[frequency]), l_antenna.id, r_antenna.id,
                                      r_antinode.row - distance[2],
                                      r_antinode.col - distance[3])

        # each antinode-generative antenna is a new antinode (because they are paired with another antenna)
        for antenna in antennas_generating_antinodes:
            new_antinode = Antinode(len(antinodes[frequency]), antenna.id, antenna.id, antenna.row, antenna.col)
            antinodes[frequency].append(new_antinode)

    return antinodes


def part2(all_frequencies: {str: [Antenna]}, map_geometry: (int, int)) -> int:
    distances = calculate_distances(all_frequencies)
    antinodes = calculate_antinodes_with_resonance(all_frequencies, distances, map_geometry)
    impact = calculate_impact(antinodes)
    return len(impact)


if __name__ == '__main__':
    with open('data/aoc2024-input-day08.txt', 'r') as f:
        sol_raw_data = [line.strip('\n') for line in f.readlines()]

    sol_frequencies, sol_map = parse_input(sol_raw_data)

    print('PART 1')
    print('>>>>SOLUTION: ', part1(sol_frequencies, sol_map))

    print('PART 2')
    print('>>>>SOLUTION: ', part2(sol_frequencies, sol_map))
