# Day 6: Tuning Trouble

def detect_marker(buff, size=4):
    i = 0
    for _ in buff:
        if i > size - 1:
            if len(set(buff[i - size:i])) == size:
                return i
        i += 1


if __name__ == '__main__':
    with open('data/aoc2022-input-day06.txt', 'r') as f:
        raw_data = f.read()

    print('PART 1')
    print('>>>SOLUTION: ', detect_marker(raw_data))

    print('PART 2')
    print('>>>SOLUTION: ', detect_marker(raw_data, 14))
