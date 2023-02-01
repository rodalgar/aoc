# Day 7: No Space Left On Device
from functools import partial

FS_ENTRY_TYPE_FILE = 'F'
FS_ENTRY_TYPE_DIR = 'D'


def parse_input(raw_data_in):
    # 0   , 1   , 2   , 3         , 4
    # name, type, size, parent_dir, children (if dir)
    root = ['/', FS_ENTRY_TYPE_DIR, 0, None, {}]
    wd = root
    reading_content = False
    for line in raw_data_in:
        parts = line.split(' ')
        if parts[0] == '$':
            reading_content = False
            if parts[1] == 'cd':
                if parts[2] == '/':
                    wd = root
                elif parts[2] == '..':
                    wd = wd[3]
                else:
                    if parts[2] not in wd[4]:
                        print(f'DIR {parts[2]} NOT FOUND IN {wd[0]}!!')
                    else:
                        child = wd[4][parts[2]]
                        if child[1] != FS_ENTRY_TYPE_DIR:
                            print(f'cd CAN ONLY CHANGE TO DIRECTORIES! {parts[2]} IS NOT A DIRECTORY')
                        wd = child
            elif parts[1] == 'ls':
                reading_content = True
        else:
            if not reading_content:
                print(f'SYNTAX ERROR, COMMAND {line} UNKNOWN')
            if parts[1] in wd[4]:
                print(f'DIRECTORY {wd[0]} ALREADY CONTAINS AN ENTRY NAMED {parts[1]}')
            if parts[0] != 'dir':
                size = int(parts[0])
                wd[4][parts[1]] = [parts[1], FS_ENTRY_TYPE_FILE, size, wd, None]
                iwd = wd
                while iwd is not None:
                    iwd[2] += size
                    iwd = iwd[3]
            else:
                wd[4][parts[1]] = [parts[1], FS_ENTRY_TYPE_DIR, 0, wd, {}]
    return root


# PART 1
def eval_files_p1(file):
    return file[1] == FS_ENTRY_TYPE_DIR and file[2] <= 100000


def get_dirs_recur(root, eval_fun):
    selected_dirs = []

    if root[1] == FS_ENTRY_TYPE_DIR:
        if eval_fun(root):
            selected_dirs.append(root)
        for c in root[4]:
            selected_dirs += get_dirs_recur(root[4][c], eval_fun)

    return selected_dirs


# PART 2
def eval_files_p2(file, limit):
    return file[1] == FS_ENTRY_TYPE_DIR and file[2] >= limit


def solve_p2(root, total_space, required_space):
    free_space = total_space - root[2]
    to_free = required_space - free_space

    candidate_size = None
    if to_free > 0:
        f_partial = partial(eval_files_p2, limit=to_free)
        candidates = [(file[0], file[2])
                      for file in get_dirs_recur(root, f_partial)]
        candidates.sort(key=lambda a: a[1])
        if len(candidates) > 0:
            candidate_size = candidates[0][1]

    return candidate_size


if __name__ == '__main__':
    with open('data/aoc2022-input-day07.txt', 'r') as f:
        raw_data = [line.strip('\n') for line in f.readlines()]

    data = parse_input(raw_data)

    print('PART 1')
    directories = get_dirs_recur(data, eval_files_p1)
    print('>>>SOLUTION: ', sum((file[2] for file in directories)))

    print('PART 2')
    print('>>>SOLUTION: ', solve_p2(data, 70000000, 30000000))
