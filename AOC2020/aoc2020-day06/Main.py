# DAY 6: Custom Customs


# PART 1
def parse_groups(lines):
    """
    Transforms a list of strings into a list of lists, one for each group of persons.

    :param lines: List of strings from the raw input.
    :return: List of lists, one for each group of persons.
    """

    result_groups = []
    group = []
    for line in lines:
        if len(line) == 0:
            result_groups.append(group)
            group = []
        else:
            group.append(line)

    # last line
    if len(group) > 0:
        result_groups.append(group)

    return result_groups


def count_answers_in_group_anyone_yes(group):
    """
    Counts answers of group as the union of all answered questions of every person.

    :param group: Answers of a group of persons.
    :return: Number of questions answered.
    """
    answered_questions = set()
    for person in group:
        for answered_question in person:
            answered_questions.add(answered_question)
    return len(answered_questions)


def count_answers_in_all_groups(count_fun, groups):
    """
    Applies count_fun to each group and sums all results.

    :param count_fun: Function that counts answered questions in a group.
    :param groups: List of groups.
    :return: Sum of all results.
    """
    return sum(map(count_fun, parse_groups(sol_groups)))


# PART 2
def count_answers_in_group_everyone_yes(group):
    """
    Counts answers of group as the intersection of all answered questions of every person.

    :param group: Answers of a group of persons.
    :return: Number of questions answered.
    """

    answered_questions = set(group[0])
    for i in range(1, len(group)):
        person = set(group[i])
        answered_questions = answered_questions.intersection(person)
    return len(answered_questions)


def test_part_2(group, expected):
    """
    Test function for testing part 2.

    :param group: Testing group.
    :param expected: Expected count.
    """
    answered_questions = count_answers_in_group_everyone_yes(group)
    print('Test count_answers_in_group_everyone_yes',
          'RIGHT' if answered_questions == expected else f'WRONG!! Expected {expected} but was {answered_questions}')


if __name__ == '__main__':
    with open('data/aoc2020-input-day06.txt', 'r') as f:
        sol_groups = [line.strip('\n') for line in f.readlines()]

    test_groups = ['abc',
                   '',
                   'a',
                   'b',
                   'c',
                   '',
                   'ab',
                   'ac',
                   '',
                   'a',
                   'a',
                   'a',
                   'a',
                   '',
                   'b']

    test_group = ['abcx',
                  'abcy',
                  'abcz']

    print('PART 1')
    # TEST PART 1
    parsed_groups = parse_groups(test_groups)
    print('Test parse_groups',
          'RIGHT' if len(parsed_groups) == 5 else f'WRONG!! Expected 5 but was {len(parsed_groups)}')

    answered_questions = count_answers_in_group_anyone_yes(test_group)
    print('Test count_answers_in_group_anyone_yes',
          'RIGHT' if answered_questions == 6 else f'WRONG!! Expected 6 but was {answered_questions}')

    group_total = count_answers_in_all_groups(count_answers_in_group_anyone_yes, parse_groups(test_groups))
    print('Test count_answers_in_all_groups',
          'RIGHT' if group_total == 11 else f'WRONG!! Expected 11 but was {group_total}')

    # SOLVING PART 1
    print('SOLUTION PART 1', count_answers_in_all_groups(count_answers_in_group_anyone_yes, parse_groups(sol_groups)))

    print('PART 2')
    # TEST PART 2
    test_part_2(parsed_groups[0], 3)
    test_part_2(parsed_groups[1], 0)
    test_part_2(parsed_groups[2], 1)
    test_part_2(parsed_groups[3], 1)
    test_part_2(parsed_groups[4], 1)

    # SOLVING PART 2
    print('SOLUTION PART 2', count_answers_in_all_groups(count_answers_in_group_everyone_yes, parse_groups(sol_groups)))
