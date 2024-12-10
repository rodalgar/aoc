# Day 9: Disk Fragmenter

def parse_input(raw_data: str) -> [str]:
    file_id = 0
    blocks = []
    processing_data = True
    for data in raw_data:
        if processing_data:
            for _ in range(int(data)):
                blocks.append(str(file_id))
            file_id += 1
            processing_data = False
        else:
            for _ in range(int(data)):
                blocks.append('.')
            processing_data = True
    return blocks


def defragment_by_block(expanded_disk: [str], verbose: bool = False) -> [str]:
    # left pointer points at the first blank block
    left_pointer = 0
    while expanded_disk[left_pointer] != '.':
        left_pointer += 1
    # right pointer points at the last data block
    right_pointer = len(expanded_disk) - 1
    while expanded_disk[right_pointer] == '.':
        right_pointer -= 1
    if verbose:
        print(f'defragmenting {expanded_disk}')
        print(f'left_pointer: {left_pointer} ({expanded_disk[left_pointer]})'
              f'right_pointer: {right_pointer} ({expanded_disk[right_pointer]})')

    while left_pointer < right_pointer:
        # Move block
        #   Write new block
        expanded_disk[left_pointer] = expanded_disk[right_pointer]
        #   Delete old block
        expanded_disk[right_pointer] = '.'
        # move left pointer
        left_pointer += 1
        while expanded_disk[left_pointer] != '.':
            left_pointer += 1
        # move right pointer
        right_pointer -= 1
        while expanded_disk[right_pointer] == '.':
            right_pointer -= 1

    return expanded_disk


def calculate_checksum(disk: [str]) -> int:
    checksum = 0
    for ix, data in enumerate(disk):
        if data != '.':
            checksum += ix * int(data)
    return checksum


def defragment_by_file(expanded_disk: [str], verbose: bool = False) -> [str]:
    # left pointer points at the first blank block
    left_pointer = 0
    while expanded_disk[left_pointer] != '.':
        left_pointer += 1
    # right pointer_init, right_pointer_end point to the beginning and last block of the rightmost unprocessed file
    right_pointer_end = len(expanded_disk) - 1
    while expanded_disk[right_pointer_end] == '.':
        right_pointer_end -= 1
    last_file_id = expanded_disk[right_pointer_end]
    right_pointer_init = right_pointer_end
    while right_pointer_init >= 0 and expanded_disk[right_pointer_init - 1] == last_file_id:
        right_pointer_init -= 1

    if verbose:
        print(f'defragmenting {expanded_disk}')
        print(f'left_pointer: {left_pointer} ({expanded_disk[left_pointer]}) '
              f'right_pointer: {right_pointer_init}:{right_pointer_end} '
              f'({expanded_disk[right_pointer_init:right_pointer_end + 1]})')

    while last_file_id != '-1':
        if verbose:
            print(f'trying to relocate file {last_file_id}')
            print(f'left_pointer: {left_pointer} ({expanded_disk[left_pointer]}) '
                  f'right_pointer: {right_pointer_init}:{right_pointer_end} '
                  f'({expanded_disk[right_pointer_init:right_pointer_end + 1]})')

        size_requested = right_pointer_end - right_pointer_init + 1
        initial_blank = left_pointer
        if verbose:
            print(f'\tsize of file {size_requested}. beginning search at {initial_blank}')

        file_was_moved = False
        all_gaps_exhausted = False
        init_gap_used = None

        while not all_gaps_exhausted:
            # looking for "hueco"
            seeker_init = seeker_end = initial_blank
            # check if file fits in the gap
            fits = False
            if size_requested == 1:
                fits = True
                file_was_moved = True
                init_gap_used = seeker_init
            else:
                while seeker_end < len(expanded_disk) - 1 and expanded_disk[seeker_end + 1] == '.':
                    seeker_end += 1
                    if seeker_end - seeker_init + 1 == size_requested:
                        if verbose:
                            print(f'FITSSSS at {seeker_init}:{seeker_end}')
                        fits = True
                        file_was_moved = True
                        init_gap_used = seeker_init
                        break
            if fits:
                # Moving block
                #   Write new block
                if verbose:
                    print(f'MOVING. file is at {right_pointer_init},{right_pointer_end}. '
                          f'Moving to {seeker_init},{seeker_end}')
                copy_pointer = seeker_init
                while copy_pointer <= seeker_end:
                    expanded_disk[copy_pointer] = last_file_id
                    copy_pointer += 1
                #   Delete old block
                delete_pointer = right_pointer_init
                while delete_pointer <= right_pointer_end:
                    expanded_disk[delete_pointer] = '.'
                    delete_pointer += 1
                if verbose:
                    print(f'file {last_file_id} moved, expanded_disk so far {expanded_disk}')
                break  # while True
            else:
                if verbose:
                    print(f'file {last_file_id} do not fit at gap on {initial_blank} '
                          f'(was only {seeker_end - seeker_init + 1} wide)')
                # try next gap
                # filling actual gap
                initial_blank = seeker_end
                while expanded_disk[initial_blank] == '.':
                    if initial_blank == len(expanded_disk) - 1:
                        all_gaps_exhausted = True
                        break
                    initial_blank += 1
                # looking for the next gap
                while not all_gaps_exhausted and expanded_disk[initial_blank] != '.':
                    if initial_blank >= right_pointer_init:
                        all_gaps_exhausted = True
                        break
                    if initial_blank == len(expanded_disk) - 1:
                        all_gaps_exhausted = True
                        break
                    initial_blank += 1

        # advancing left pointer if file was moved
        if file_was_moved:
            # if the gap used was the leftmost one we need to search the next gap to set the new limit
            if left_pointer == init_gap_used:
                while expanded_disk[left_pointer] != '.':
                    left_pointer += 1
        # advancing right pointer (always changes the file to move)
        last_file_id = str(int(last_file_id) - 1)
        if verbose:
            print(f'new file_id to relocate will be {last_file_id}')

        while right_pointer_end > 0 and expanded_disk[right_pointer_end] != last_file_id:
            right_pointer_end -= 1

        right_pointer_init = right_pointer_end
        while right_pointer_init > 0 and expanded_disk[right_pointer_init - 1] == last_file_id:
            right_pointer_init -= 1
        if right_pointer_init <= left_pointer:
            if verbose:
                print(f'file will not be moved, no free space left to the left')
            break

    return expanded_disk


if __name__ == '__main__':
    with open('data/aoc2024-input-day09.txt', 'r') as f:
        sol_raw_data = f.readline().strip('\n')

    sol_expanded_data = parse_input(sol_raw_data)

    print('PART 1')
    print('>>>>SOLUTION: ', calculate_checksum(defragment_by_block(sol_expanded_data.copy())))

    print('PART 2')
    print('>>>>SOLUTION: ', calculate_checksum(defragment_by_file(sol_expanded_data.copy())))
