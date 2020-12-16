# Day 15: Rambunctious Recitation


# PART 1
def manage_spoken_value(actual_turn, memory, spoken):
    """
    Manages a new spoken value, storing it into memory. If it was a new entry it initializes a "last times spoken" list
    which keeps track of the last two times the value was spoken. For the entire history, you can remove the slice and
    keep the entire list (It doesn't matter as the algorithm just uses the last two values)

    :param actual_turn: turn of the game.
    :param memory: Entire memory, all spoken values and the times they were spoken.
    :param spoken: The spoken value in the actual turn.
    """
    all_times_spoken = None
    if spoken not in memory:
        all_times_spoken = []
    else:
        last_time_was_spoken, all_times_spoken = memory[spoken]
    all_times_spoken.append(actual_turn)
    memory[spoken] = (actual_turn, all_times_spoken[-2:])


def play_game(sequence, turn_to_stop, verbose=False, get_all_turn_history=False):
    """
    Plays a match.

    :param sequence: Initial sequence for the match.
    :param turn_to_stop: Turn in which the match will end.
    :param verbose: If True additional info will be printed.
    :param get_all_turn_history: If True the function keeps track of every spoken value every turn.
    :return: List of every spoken value of every turn or just the last spoken value generated.
    """
    actual_turn = 0
    memory = {}
    turn_sequence_generated = []

    # First consume starting sequence
    # In this step, spoken values are taken directly from the sequence.
    for turn0, spoken in enumerate(sequence):
        actual_turn = turn0 + 1
        # SPOKE
        if verbose:
            print('Spoken', (actual_turn, spoken))

        # MANAGE
        manage_spoken_value(actual_turn, memory, spoken)

        last_played = (actual_turn, spoken)
        if get_all_turn_history:
            turn_sequence_generated.append(last_played)

    # Now, go on. This is where the fun starts.
    # In this step, spoken value is either 0 (if last value was still not spoken) or the difference when it was last
    # spoken and the later.
    while True:
        actual_turn += 1
        # SPOKE
        if verbose:
            print(last_played, memory)

        _, last_spoken = last_played
        _, last_all_times_spoken = memory[last_spoken]
        if verbose:
            print(last_spoken, last_all_times_spoken)

        if len(last_all_times_spoken) == 1:
            spoken = 0
        else:
            l = last_all_times_spoken[-1]
            l2 = last_all_times_spoken[-2]
            spoken = l - l2
            if verbose:
                print(f'\tactual_turn {actual_turn} last_spoken {last_spoken} mem {memory[last_spoken]} l {l} l2 {l2}')

        if verbose:
            print(f'New spoken is {spoken}')
        last_played = (actual_turn, spoken)
        if get_all_turn_history:
            turn_sequence_generated.append(last_played)
        if verbose:
            print(f'Turn {actual_turn} generates {last_played}')

        # MANAGE
        manage_spoken_value(actual_turn, memory, spoken)

        if actual_turn % 1000000 == 0:
            print(f'Actual turn {actual_turn}')

        if actual_turn == turn_to_stop:
            break

    if get_all_turn_history:
        return turn_sequence_generated, memory
    else:
        return [last_played], memory


def test_guessing(sequence, test_last_turn, expected):
    generated_turns, _ = play_game(sequence, test_last_turn)
    result = generated_turns[-1][1]
    print(f'Testing play_game {sequence}',
          'RIGHT' if result == expected else f'WRONG!! Expected {expected} but was {result}')


if __name__ == '__main__':
    print('PART 1')
    # TEST
    last_turn = 2020
    test_sequence = [0, 3, 6]
    test_guessing(test_sequence, last_turn, 436)
    test_guessing([1, 3, 2], last_turn, 1)
    test_guessing([2, 1, 3], last_turn, 10)
    test_guessing([1, 2, 3], last_turn, 27)
    test_guessing([2, 3, 1], last_turn, 78)
    test_guessing([3, 2, 1], last_turn, 438)
    test_guessing([3, 1, 2], last_turn, 1836)

    # SOLVING PART 1
    sol_sequence = [0, 8, 15, 2, 12, 1, 4]
    s, m = play_game(sol_sequence, 2020)
    print('SOLUTION PART 1:', s[-1][1])
    print()

    # PART 2
    print('PART 2')
    # TEST
    last_turn = 30000000
    test_guessing(test_sequence, last_turn, 175594)
    test_guessing([1, 3, 2], last_turn, 2578)
    test_guessing([2, 1, 3], last_turn, 3544142)
    test_guessing([1, 2, 3], last_turn, 261214)
    test_guessing([2, 3, 1], last_turn, 6895259)
    test_guessing([3, 2, 1], last_turn, 18)
    test_guessing([3, 1, 2], last_turn, 362)

    # SOLVING PART 2
    s, _ = play_game(sol_sequence, 30000000)
    print('SOLUTION PART 2:', s[-1][1])
