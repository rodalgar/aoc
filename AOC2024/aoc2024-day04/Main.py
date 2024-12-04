# Day 4: Ceres Search

# PART 1
def find_xmas(data: [str], verbose: bool = False) -> int:
    words_found = 0
    for row in range(len(data)):
        for col in range(len(data[0])):
            if data[row][col] == 'X':
                if verbose:
                    print(f'X located at {row} {col}')
                for direction in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (1, 1), (1, -1), (-1, -1)]:
                    new_row = row
                    new_col = col
                    valid_word = True
                    for expected_letter in ['M', 'A', 'S']:
                        new_row = new_row + direction[0]
                        new_col = new_col + direction[1]
                        if verbose:
                            print(f'found {expected_letter} at {new_row}, {new_col}')
                        # check map bounds
                        if 0 <= new_row < len(data) and 0 <= new_col < len(data[0]):
                            if data[new_row][new_col] != expected_letter:
                                valid_word = False
                                break
                        else:
                            valid_word = False
                            break
                    if valid_word:
                        if verbose:
                            print('XMAS found!')
                        words_found += 1
    return words_found


def find_x_mas(data: [str], verbose: bool = False) -> int:
    def validate_corner(analyzed_letter, other_letter):
        if analyzed_letter != 'S' and analyzed_letter != 'M':
            return False
        if analyzed_letter == 'M' and other_letter != 'S':
            return False
        if analyzed_letter == 'S' and other_letter != 'M':
            return False
        return True

    x_mas_found = 0
    for row in range(1, len(data) - 1):
        for col in range(1, len(data[0]) - 1):
            if data[row][col] == 'A':
                if verbose:
                    print(f'A located at {row} {col}')
                # upper left corner
                letter = data[row - 1][col - 1]
                opposite_letter = data[row + 1][col + 1]
                if not validate_corner(letter, opposite_letter):
                    continue

                # upper right corner
                letter = data[row - 1][col + 1]
                opposite_letter = data[row + 1][col - 1]
                if not validate_corner(letter, opposite_letter):
                    continue
                x_mas_found += 1
    return x_mas_found


if __name__ == '__main__':
    with open('data/aoc2024-input-day04.txt', 'r') as f:
        sol_raw_data = [line.strip('\n') for line in f.readlines()]

    print('PART 1')
    print('>>>>SOLUTION: ', find_xmas(sol_raw_data))

    print('PART 2')
    print('>>>>SOLUTION: ', find_x_mas(sol_raw_data))
