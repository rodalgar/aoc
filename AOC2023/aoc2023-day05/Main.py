# Day 5: If You Give A Seed A Fertilizer
from typing import Optional


RangeInfo = tuple[int, int, int]
Mapping = list[str, str, list[RangeInfo], Optional[list]]


def parse_input(raw_data: list[str]) -> tuple[list[int], Mapping]:
    seeds = list(map(int, raw_data[0].split(':')[1].strip().split(' ')))

    begin_map = None
    current_map: Optional[Mapping] = None
    mapping: Optional[Mapping] = None

    for line in raw_data[1:]:
        if len(line) == 0:
            begin_map = True
            continue
        if begin_map:
            begin_map = False
            map_data = line.split(' ')[0].split('-')
            map_from = map_data[0]
            map_to = map_data[2]
            last_map = current_map
            current_map: list[str, str, list[RangeInfo], Optional[Mapping]] = [map_from, map_to, [], None]
            if mapping is None:
                mapping = current_map
            if last_map is not None:
                last_map[3] = current_map
            continue

        current_map[2].append(tuple(map(int, line.split(' '))))

    i_map = mapping
    while i_map[3] is not None:
        i_map[2].sort(key=lambda x: x[1])
        i_map = i_map[3]
    else:
        i_map[2].sort(key=lambda x: x[1])

    return seeds, mapping


def range_map_stage(seed_ranges: list[tuple[int, int]], mappings: Mapping) -> list[tuple[int, int]]:
    new_seed_ranges = []
    ix_seed = 0
    ix_mapping = 0
    init_seed = seed_ranges[ix_seed][0]
    len_seed = seed_ranges[ix_seed][1]
    init_mapping = mappings[2][ix_mapping][1]
    len_mapping = mappings[2][ix_mapping][2]
    vals_mapping = mappings[2][ix_mapping][0]

    while ix_seed is not None and ix_mapping is not None:
        if init_mapping < init_seed:
            # there is a mapping range before the first seed range
            delta = init_seed - init_mapping
            if delta > len_mapping:
                # whole mapping is before the seed range, does not affect anything
                # 'moving' mapping range
                ix_mapping += 1
                if ix_mapping == len(mappings[2]):
                    ix_mapping = None
                else:
                    init_mapping = mappings[2][ix_mapping][1]
                    len_mapping = mappings[2][ix_mapping][2]
                    vals_mapping = mappings[2][ix_mapping][0]
            elif delta < len_mapping:
                # both range overlap but there's more mapping range unused
                # 'moving' mapping range
                init_mapping += delta
                vals_mapping += delta
                len_mapping -= delta
            else:
                # range overlap and mapping range is fully used
                # 'moving' mapping range
                ix_mapping += 1
                if ix_mapping == len(mappings[2]):
                    ix_mapping = None
                else:
                    init_mapping = mappings[2][ix_mapping][1]
                    len_mapping = mappings[2][ix_mapping][2]
                    vals_mapping = mappings[2][ix_mapping][0]
        elif init_mapping == init_seed:
            # mapping range and seed range starts on the same 'location'
            delta = min(len_seed, len_mapping)
            new_seed_ranges.append((vals_mapping, delta))
            # 'moving' seed range
            len_seed -= delta
            if len_seed == 0:
                ix_seed += 1
                if ix_seed == len(seed_ranges):
                    ix_seed = None
                else:
                    init_seed = seed_ranges[ix_seed][0]
                    len_seed = seed_ranges[ix_seed][1]
            else:
                init_seed += delta
            # 'moving' mapping range
            len_mapping -= delta
            if len_mapping == 0:
                ix_mapping += 1
                if ix_mapping == len(mappings[2]):
                    ix_mapping = None
                else:
                    init_mapping = mappings[2][ix_mapping][1]
                    len_mapping = mappings[2][ix_mapping][2]
                    vals_mapping = mappings[2][ix_mapping][0]
            else:
                init_mapping += delta
                vals_mapping += delta
        else:
            # seed range come first
            delta = init_mapping - init_seed
            if delta < len_seed:
                new_seed_ranges.append((init_seed, delta))
                # 'moving' seed range
                len_seed -= delta
                if len_seed == 0:
                    ix_seed += 1
                    if ix_seed == len(seed_ranges):
                        ix_seed = None
                    else:
                        init_seed = seed_ranges[ix_seed][0]
                        len_seed = seed_ranges[ix_seed][1]
                else:
                    init_seed += delta
            elif delta >= len_seed:
                new_seed_ranges.append((init_seed, len_seed))
                # 'moving' mapping range
                ix_seed += 1
                if ix_seed == len(seed_ranges):
                    ix_seed = None
                else:
                    init_seed = seed_ranges[ix_seed][0]
                    len_seed = seed_ranges[ix_seed][1]

    # ran out of seeds or mappings... if there are more seed ranges they pass on the next stage as is.
    # Notice the first seed range (if any) considers being partially modified by the past loop.
    # we don't do anything about remaining mappings... condition was for avoiding iterations that will
    # not change the result because there are no seeds to transform
    while ix_seed is not None:
        new_seed_ranges.append((init_seed, len_seed))
        ix_seed += 1
        if ix_seed == len(seed_ranges):
            ix_seed = None
        else:
            init_seed = seed_ranges[ix_seed][0]
            len_seed = seed_ranges[ix_seed][1]

    return new_seed_ranges


def range_map_stages(seed_ranges: list[tuple[int, int]], mappings: Mapping) -> list[tuple[int, int]]:
    current_mapping = mappings

    while current_mapping is not None:
        seed_ranges.sort(key=lambda x: x[0])
        seed_ranges = range_map_stage(seed_ranges, current_mapping)
        current_mapping = current_mapping[3]

    # 'seeds' are now 'locations' (hopefully)
    return seed_ranges


def range_part1(seeds: list[int], mappings: Mapping) -> int:
    seed_ranges = [(seed, 1) for seed in seeds]
    locations = range_map_stages(seed_ranges, mappings)
    return min([location[0] for location in locations])


def range_part2(seeds: list[int], mappings: Mapping) -> int:
    seed_ranges = [tuple(seeds[ix:ix + 2]) for ix in range(0, len(seeds), 2)]
    locations = range_map_stages(seed_ranges, mappings)
    return min([location[0] for location in locations])


if __name__ == '__main__':
    with open('data/aoc2023-input-day05.txt', 'r') as f:
        sol_raw_data = [line.strip('\n') for line in f.readlines()]

    sol_seeds, sol_maps = parse_input(sol_raw_data)

    print('PART 1')
    print('>>>>SOLUTION: ', range_part1(sol_seeds, sol_maps))

    print('PART 2')
    print('>>>>SOLUTION: ', range_part2(sol_seeds, sol_maps))
