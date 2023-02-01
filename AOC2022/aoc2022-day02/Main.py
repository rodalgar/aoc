# Day 2: Rock Paper Scissors

ROCK = 'R'
PAPER = 'P'
SCISSORS = 'S'

# game rules
wins_against = {
    ROCK: SCISSORS,
    PAPER: ROCK,
    SCISSORS: PAPER
}

loses_against = {
    ROCK: PAPER,
    PAPER: SCISSORS,
    SCISSORS: ROCK
}

ties_against = {
    ROCK: ROCK,
    PAPER: PAPER,
    SCISSORS: SCISSORS
}

round_outcome_points = {
    'W': 6,
    'T': 3,
    'L': 0
}

action_selected_points = {
    ROCK: 1,
    PAPER: 2,
    SCISSORS: 3
}

# transformations
map_opponent_actions = {
    'A': ROCK,
    'B': PAPER,
    'C': SCISSORS
}

map_your_actions_p1 = {
    'X': ROCK,
    'Y': PAPER,
    'Z': SCISSORS
}

map_your_actions_p2 = {
    'X': wins_against,
    'Y': ties_against,
    'Z': loses_against
}


# PART 1
def get_own_action_part1(raw_step):
    raw_action = raw_step[2]
    return map_your_actions_p1[raw_action]


# PART 2
def get_own_action_part2(raw_step):
    raw_action = raw_step[2]
    opponent_action = map_opponent_actions[raw_step[0]]

    return map_your_actions_p2[raw_action][opponent_action]


# PART 1 & 2
def parse_input(raw_data_in, opponent_rules, your_rules_fun):
    return [f'{opponent_rules[line[0]]} {your_rules_fun(line)}' for line in raw_data_in]


def get_round_outcome(step_guide, win_rules):
    opponent_bet = step_guide[0]
    you_rule = step_guide[2]

    if opponent_bet == you_rule:
        return 'T'
    elif win_rules[you_rule] == opponent_bet:
        return 'W'
    else:
        return 'L'


def do_match(guide):
    total = 0
    for step in guide:
        round_outcome = get_round_outcome(step, wins_against)
        score = action_selected_points[step[2]] + round_outcome_points[round_outcome]
        total += score
    return total


if __name__ == '__main__':
    with open('data/aoc2022-input-day02.txt', 'r') as f:
        raw_data = [line.strip('\n') for line in f.readlines()]

    print('PART 1')
    data = parse_input(raw_data, map_opponent_actions, get_own_action_part1)
    print('>>>SOLUTION: ', do_match(data))

    print('PART 2')
    data = parse_input(raw_data, map_opponent_actions, get_own_action_part2)
    print('>>>SOLUTION: ', do_match(data))
