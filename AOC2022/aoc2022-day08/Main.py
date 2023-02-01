# Day 8: Treetop Tree House


def print_visible_trees(grid, visible, house=None):
    for i in range(len(grid)):
        row = ''
        for j in range(len(grid[0])):
            if house is not None and house[0] == j and house[1] == i:
                row += 'O'
            elif (i, j) in visible:
                row += 'X'
            else:
                row += ' '
        print(row)


# PART 1
def get_visible_trees(grid):
    max_cols = len(grid[0])
    max_rows = len(grid)

    def h_sweep(first_col, last_col, step):
        visible = []

        for i in range(max_rows):
            visible.append((i, first_col))
            tallest = grid[i][first_col]

            for j in range(first_col + step, last_col, step):
                if grid[i][j] > tallest:
                    visible.append((i, j))
                    tallest = grid[i][j]
                if tallest == 9:
                    break
        return visible

    def v_sweep(first_row, last_row, step):
        visible = []

        for j in range(max_cols):
            visible.append((first_row, j))
            tallest = grid[first_row][j]

            for i in range(first_row + step, last_row, step):
                if grid[i][j] > tallest:
                    visible.append((i, j))
                    tallest = grid[i][j]
                if tallest == 9:
                    break

        return visible

    visible_trees = set(h_sweep(0, max_cols, 1))  # right
    visible_trees |= set(h_sweep(max_cols - 1, -1, -1))  # left
    visible_trees |= set(v_sweep(0, max_rows, 1))  # down
    visible_trees |= set(v_sweep(max_rows - 1, -1, -1))  # up

    return visible_trees


# PART 2
def get_scenic_score(grid, row, col):
    max_cols = len(grid[0])
    max_rows = len(grid)
    tree_size = grid[row][col]

    def h_pulse(pos_ini, pos_end, step):
        num_visible = 0
        for j in range(pos_ini, pos_end, step):
            num_visible += 1
            if grid[row][j] >= tree_size:
                break
        return num_visible

    def v_pulse(pos_ini, pos_end, step):
        num_visible = 0
        for i in range(pos_ini, pos_end, step):
            num_visible += 1
            if grid[i][col] >= tree_size:
                break
        return num_visible

    score = h_pulse(col + 1, max_cols, 1)  # to right
    score *= h_pulse(col - 1, -1, -1)  # to left
    score *= v_pulse(row + 1, max_rows, 1)  # to down
    score *= v_pulse(row - 1, -1, -1)  # upwards

    return score


def get_best_scenic_score(grid):
    max_cols = len(grid[0])
    max_rows = len(grid)

    best_score = -1
    best_tree = (0, 0)

    for i in range(1, max_rows - 1):
        for j in range(1, max_cols - 1):
            score = get_scenic_score(grid, i, j)
            if score >= best_score:
                best_score = score
                best_tree = (i, j)

    return best_score, best_tree


if __name__ == '__main__':
    with open('data/aoc2022-input-day08.txt', 'r') as f:
        raw_data = [line.strip('\n') for line in f.readlines()]

    print('PART 1')
    print('>>>SOLUTION: ', len(get_visible_trees(raw_data)))

    print('PART 2')
    print('>>>SOLUTION: ', get_best_scenic_score(raw_data))
