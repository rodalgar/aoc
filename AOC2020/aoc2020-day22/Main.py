# Day 22: Crab Combat

# PART 1


def parse_raw_cards(raw_cards):
    """
    Parses a list of string representing two decks.

    :param raw_cards: List of strings representing two decks.
    :return: Two lists of integer, representing one deck each.
    """
    player_1 = []
    player_2 = []

    active_player = None
    for line in raw_cards:
        if line.startswith('Player 1'):
            active_player = player_1
            continue
        elif line.startswith('Player 2'):
            active_player = player_2
            continue
        if len(line) == 0:
            continue

        active_player.append(int(line))

    return player_1, player_2


def get_score(winning_player, verbose=False):
    """
    Calculates the score based on a deck.

    :param winning_player: Deck of cards.
    :param verbose: If True additional info will be printed.
    :return: Score.
    """
    winning_player.reverse()

    score = 0
    for ix, card_value in enumerate(winning_player, start=1):
        if verbose:
            print(ix, card_value)
        score += ix * card_value
    return score


def play_game(player_1, player_2, verbose=False):
    """
    Plays a math of the non-recursive version of the game (part 1).

    :param player_1: Deck of player 1.
    :param player_2: Deck of player 2.
    :param verbose: If True additional info will be printed.
    :return: Final decks of each player, last turn and score of the winner.
    """
    turn = 0
    while True:
        turn += 1
        card_p1 = player_1[:1][0]
        player_1 = player_1[1:]
        card_p2 = player_2[:1][0]
        player_2 = player_2[1:]

        if verbose:
            print('player 1', card_p1, player_1)
            print('player 2', card_p2, player_2)

        if card_p1 > card_p2:
            if verbose:
                print('p1 wins')
            player_1.append(card_p1)
            player_1.append(card_p2)
        else:
            if verbose:
                print('p2 wins')
            player_2.append(card_p2)
            player_2.append(card_p1)

        if len(player_1) == 0 or len(player_2) == 0:
            break

    winning_player = player_1
    if len(player_1) == 0:
        winning_player = player_2

    score = get_score(winning_player)

    return player_1, player_2, turn, score


# PART 2
def play_recursive_game(player_1, player_2, level=1, verbose=False):
    """
    Plays a math of the recursive version of the game (part 2).

    :param level: Recursion level.
    :param player_1: Deck of player 1.
    :param player_2: Deck of player 2.
    :param verbose: If True additional info will be printed.
    :return: Final decks of each player, last turn and score of the winner.
    """

    if verbose:
        print(f'Begin game {level}')
        print(f'\tplayer 1 {player_1}')
        print(f'\tplayer 2 {player_2}')

    past_turns = set()
    turn = 0
    while True:
        # determine loop-killer condition and exit if needed
        key = '|'.join(['-'.join([str(i) for i in player_1]),
                        '-'.join([str(i) for i in player_2])])
        if verbose:
            print(f'Testing for loop existance. Key: {key}')
        if key in past_turns:
            # Player 1 wins
            if verbose:
                print(f'Key existed in {past_turns}')
            return 1, get_score(player_1)
        past_turns.add(key)

        turn += 1
        # dealing
        card_p1 = player_1[:1][0]
        player_1 = player_1[1:]
        card_p2 = player_2[:1][0]
        player_2 = player_2[1:]

        if verbose:
            print(f'Game {level} turn {turn}')
            print('player 1', card_p1, player_1)
            print('player 2', card_p2, player_2)

        # check if sub-game has to launch
        p1_ready_for_sub_game = card_p1 <= len(player_1)
        p2_ready_for_sub_game = card_p2 <= len(player_2)

        if verbose:
            print(f'p1_ready_for_sub_game: {p1_ready_for_sub_game} p2_ready_for_sub_game: {p2_ready_for_sub_game}')

        p1_won = None
        if p1_ready_for_sub_game and p2_ready_for_sub_game:
            # play sub-game!
            if verbose:
                print('PLAY SUB-GAME!')
            # prepare new decks
            new_player_1 = player_1[:card_p1]
            new_player_2 = player_2[:card_p2]
            if verbose:
                print(f'p1 card {card_p1} p1 remaining {player_1} new p1 {new_player_1}')
                print(f'p2 card {card_p2} p2 remaining {player_2} new p2 {new_player_2}')
            sub_winner, _ = play_recursive_game(new_player_1, new_player_2, level + 1, verbose)
            p1_won = sub_winner == 1
        else:
            p1_won = card_p1 > card_p2

        if p1_won:
            player_1.append(card_p1)
            player_1.append(card_p2)
        else:
            player_2.append(card_p2)
            player_2.append(card_p1)

        if len(player_1) == 0 or len(player_2) == 0:
            break

    winning_player = player_1
    winner = 1
    if len(player_1) == 0:
        winning_player = player_2
        winner = 2

    score = get_score(winning_player, verbose)

    return winner, score


if __name__ == '__main__':
    with open('data/aoc2020-input-day22.txt', 'r') as f:
        sol_raw_cards = [line.strip('\n') for line in f.readlines()]

    test_raw_cards_1 = ['Player 1:',
                        '9',
                        '2',
                        '6',
                        '3',
                        '1',
                        '',
                        'Player 2:',
                        '5',
                        '8',
                        '4',
                        '7',
                        '10']

    print('PART 1')
    # TESTING PART 1
    expected_p1 = [9, 2, 6, 3, 1]
    expected_p2 = [5, 8, 4, 7, 10]
    p1, p2 = parse_raw_cards(test_raw_cards_1)
    # print(p1, p2)
    print('Testing parse_raw_cards, p1',
          'RIGHT' if p1 == expected_p1 else f'WRONG!! Expected {expected_p1} but was {p1}')
    print('Testing parse_raw_cards, p2',
          'RIGHT' if p2 == expected_p2 else f'WRONG!! Expected {expected_p2} but was {p2}')

    expected_exit_p1 = []
    expected_exit_p2 = [1, 7, 4, 9, 5, 8, 6, 10, 2, 3]
    expected_turns = 29
    expected_score = 306
    test_exit_p1, test_exit_p2, test_turn, test_score = play_game(p1, p2)
    print('Testing play_game, p1',
          'RIGHT' if test_exit_p1 == expected_exit_p1
          else f'WRONG!! Expected {expected_exit_p1} but was {test_exit_p1}')
    print('Testing play_game, p2',
          'RIGHT' if test_exit_p2 == expected_exit_p2
          else f'WRONG!! Expected {expected_exit_p2} but was {test_exit_p2}')
    print('Testing play_game, turns',
          'RIGHT' if test_turn == expected_turns
          else f'WRONG!! Expected {expected_turns} but was {test_turn}')
    print('Testing play_game, score',
          'RIGHT' if test_score == expected_score
          else f'WRONG!! Expected {expected_score} but was {test_score}')

    # SOLVING PART 1
    sol_p1, sol_p2 = parse_raw_cards(sol_raw_cards)
    sol_exit_p1, sol_exit_p2, sol_turn, sol_score = play_game(sol_p1, sol_p2)

    print('SOLUTION PART 1:', sol_score)
    print()

    print('PART 2')
    # TESTING PART 2
    expected_winner = 2
    expected_score = 291
    test_winner, test_score = play_recursive_game(p1, p2)
    print('Testing play_recursive_game, winner',
          'RIGHT' if test_winner == expected_winner else f'WRONG!! Expected {expected_winner} but was {test_winner}')
    print('Testing play_recursive_game, score',
          'RIGHT' if test_score == expected_score else f'WRONG!! Expected {expected_score} but was {test_score}')

    # SOLVING PART 2
    sol_winner, sol_score = play_recursive_game(sol_p1, sol_p2)
    print(f'winner is {sol_winner} with score {sol_score}')
