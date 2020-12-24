# Day 19: Monster Messages
import re


# PART 1
class Rule:
    rule_code = None

    def __init__(self, rule_code):
        self.rule_code = rule_code

    def check(self, message, position, verbose):
        pass


class RuleTerminal(Rule):
    symbol = None

    def __init__(self, rule_code, symbol):
        super().__init__(rule_code)
        self.symbol = symbol

    def check(self, message, position, verbose=False, level=0):
        if verbose:
            print('Check RuleTerminal', f'message [{message}] position {position}, symbol [{self.symbol}]')

        if position >= len(message):
            if verbose:
                print('')
            return False, position

        result = message[position] == self.symbol
        return result, position + 1 if result else position

    def __repr__(self):
        return f'"{self.symbol}"'


class RuleNonTerminal(Rule):
    rule_sets = None
    calculated_patterns = None

    def __init__(self, rule_code):
        super().__init__(rule_code)
        # TODO: Order rule sets? First all-terminal rule sets, Last recursive rule sets.
        self.rule_sets = []

    def is_axiom(self):
        return self.rule_code == '0'

    def check(self, message, position, verbose=False, level=0):
        if verbose:
            print(f'Level is {level}, position {position}')
        for rule_set in self.rule_sets:
            if verbose:
                print(f'\tStarting to validate rule set: {rule_set}')
            relative_position = position
            all_rules_ok = True
            for rule in rule_set:
                result, end_position = rule.check(message, relative_position, verbose, level + 1)
                if verbose:
                    print(f'Back to level {level} with {result}, started from position {position}')
                if not result:
                    all_rules_ok = False
                    break
                else:
                    relative_position = end_position

            if all_rules_ok:
                if self.is_axiom():
                    if verbose:
                        print('Axiom!')
                    if end_position != len(message):
                        if verbose:
                            print(f'String length ({len(message)}) and ending'
                                  f' position of accepted pattern ({end_position}) does not match')
                        # break
                        return False, position
                    else:
                        if verbose:
                            print(f'String length ({len(message)}) and ending position ({end_position}) match!')
                        return True, end_position
                else:
                    if verbose:
                        print(f"This is not the axiom (It's {self.rule_code}), but it's ok!")
                    return True, end_position
        if verbose:
            print(f'Rule {self.rule_code}. Not any of the rules can validate the string. From position {position}')
        return False, position

    def __repr__(self):
        return f'{self.rule_code} -> ({self.rule_sets})'


def test_check_rule(test_case_description, rule, message, from_position, expected, verbose=False):
    if verbose:
        print('message', message)
        print('from_position', from_position)
        print('verbose', verbose)
    result, _ = rule.check(message, from_position, verbose)

    print(f'{test_case_description} {message}:',
          'RIGHT' if result == expected else f'WRONG!! Expected {expected} but was {result}')


def parse_rules(raw_rules):
    rules = {}
    str_rules = {}
    messages = []
    cnt = 0
    for raw_rule in raw_rules:
        if len(raw_rule) == 0:
            cnt += 1
            continue

        if cnt == 0:
            chunks = raw_rule.split(':')
            rule_code = chunks[0]
            if '"' in chunks[1]:
                rule = re.sub("^ ", "", chunks[1])
                rules[rule_code] = RuleTerminal(rule_code, rule.strip('"'))
            else:
                raw_rule_sets = re.sub("^ ", "", chunks[1])
                rule_sets = re.sub(' \| ', '$', raw_rule_sets).split('$')
                str_rules[rule_code] = []

                for rule_set in rule_sets:
                    str_rule_set = []
                    for rule in rule_set.split(' '):
                        str_rule_set.append(rule)
                    str_rules[rule_code].append(str_rule_set)

                rules[rule_code] = RuleNonTerminal(rule_code)
        elif cnt == 1:
            messages.append(raw_rule)

    for rule_code, str_rule_sets in str_rules.items():
        rule = rules[rule_code]
        for str_rule_set in str_rule_sets:
            rule_set = []
            for str_rule in str_rule_set:
                rule_set.append(rules[str_rule])
            rule.rule_sets.append(rule_set)

    return rules, messages


def filter_valid_messages_with_check(rule, messages, verbose=False):
    valid_messages = []
    invalid_messages = []

    for message in messages:
        result, _ = rule.check(message, 0, verbose)
        if result:
            valid_messages.append(message)
        else:
            invalid_messages.append(message)
    return valid_messages, invalid_messages


# PART 2

if __name__ == '__main__':
    with open('data/aoc2020-input-day19.txt', 'r') as f:
        sol_raw_notes = [line.strip('\n') for line in f.readlines()]

    raw_test_rules_1 = ['0: 1 2',
                        '1: "a"',
                        '2: 1 3 | 3 1',
                        '3: "b"']

    raw_test_rules_2 = ['0: 4 1 5',
                        '1: 2 3 | 3 2',
                        '2: 4 4 | 5 5',
                        '3: 4 5 | 5 4',
                        '4: "a"',
                        '5: "b"']

    raw_test_rules_3 = ['42: 9 14 | 10 1',
                        '9: 14 27 | 1 26',
                        '10: 23 14 | 28 1',
                        '1: "a"',
                        '11: 42 31',
                        '5: 1 14 | 15 1',
                        '19: 14 1 | 14 14',
                        '12: 24 14 | 19 1',
                        '16: 15 1 | 14 14',
                        '31: 14 17 | 1 13',
                        '6: 14 14 | 1 14',
                        '2: 1 24 | 14 4',
                        '0: 8 11',
                        '13: 14 3 | 1 12',
                        '15: 1 | 14',
                        '17: 14 2 | 1 7',
                        '23: 25 1 | 22 14',
                        '28: 16 1',
                        '4: 1 1',
                        '20: 14 14 | 1 15',
                        '3: 5 14 | 16 1',
                        '27: 1 6 | 14 18',
                        '14: "b"',
                        '21: 14 1 | 1 14',
                        '25: 1 1 | 1 14',
                        '22: 14 14',
                        '8: 42',
                        '26: 14 22 | 1 20',
                        '18: 15 15',
                        '7: 14 5 | 1 21',
                        '24: 14 1',
                        '',
                        'abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa',
                        'bbabbbbaabaabba',
                        'babbbbaabbbbbabbbbbbaabaaabaaa',
                        'aaabbbbbbaaaabaababaabababbabaaabbababababaaa',
                        'bbbbbbbaaaabbbbaaabbabaaa',
                        'bbbababbbbaaaaaaaabbababaaababaabab',
                        'ababaaaaaabaaab',
                        'ababaaaaabbbaba',
                        'baabbaaaabbaaaababbaababb',
                        'abbbbabbbbaaaababbbbbbaaaababb',
                        'aaaaabbaabaaaaababaa',
                        'aaaabbaaaabbaaa',
                        'aaaabbaabbaaaaaaabbbabbbaaabbaabaaa',
                        'babaaabbbaaabaababbaabababaaab',
                        'aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba']

    raw_notes_1 = ['0: 4 1 5',
                   '1: 2 3 | 3 2',
                   '2: 4 4 | 5 5',
                   '3: 4 5 | 5 4',
                   '4: "a"',
                   '5: "b"',
                   '',
                   'ababbb',
                   'bababa',
                   'abbbab',
                   'aaabbb',
                   'aaaabbb']

    print('PART 1')
    # TEST PART 1
    rt_a = RuleTerminal('0', 'a')
    test_check_rule('Test check terminal rt_a a pos 0', rt_a, 'a', 0, True)
    test_check_rule('Test check terminal rt_a b pos 0', rt_a, 'b', 0, False)

    rnt1_a = RuleNonTerminal('0')
    rnt1_a.rule_sets.append([rt_a])
    test_check_rule('Test check non-terminal rnt1_a a pos 0', rnt1_a, 'a', 0, True)
    test_check_rule('Test check non-terminal rnt1_a b pos 0', rnt1_a, 'b', 0, False)

    rt_b = RuleTerminal('0', 'b')
    rnt2_a_b = RuleNonTerminal('0')
    rnt2_a_b.rule_sets.append([rt_a])
    rnt2_a_b.rule_sets.append([rt_b])
    test_check_rule('Test check non-terminal rnt2_a_b a pos 0', rnt2_a_b, 'a', 0, True)
    test_check_rule('Test check non-terminal rnt2_a_b b pos 0', rnt2_a_b, 'b', 0, True)
    test_check_rule('Test check non-terminal rnt2_a_b c pos 0', rnt2_a_b, 'c', 0, False)

    rnt3_ab = RuleNonTerminal('0')
    rnt3_ab.rule_sets.append([rt_a, rt_b])
    test_check_rule('Test check non_terminal rnt3_ab ab pos 0', rnt3_ab, 'ab', 0, True)
    test_check_rule('Test check non_terminal rnt3_ab ba pos 0', rnt3_ab, 'ba', 0, False)

    rnt4_rnt1 = RuleNonTerminal('0')
    rnt4_rnt1.rule_sets.append([rnt1_a])
    test_check_rule('Test check non_terminal rnt4_rnt1 a pos 0', rnt4_rnt1, 'a', 0, True)
    test_check_rule('Test check non_terminal rnt4_rnt1 b pos 0', rnt4_rnt1, 'b', 0, False)

    test_rules_1, test_messages_1 = parse_rules(raw_notes_1)
    test_rules_2, test_messages_2 = parse_rules(raw_test_rules_2)
    print('Test parse_rules (1a)',
          'RIGHT' if len(test_rules_1) == 6 else f'WRONG!! Expected 6 but was {len(test_rules_1)}')
    print('Test parse_rules (1b)',
          'RIGHT' if len(test_messages_1) == 5 else f'WRONG!! Expected 5 but was {len(test_messages_1)}')
    print('Test parse_rules (2a)',
          'RIGHT' if len(test_rules_2) == 6 else f'WRONG!! Expected 6 but was {len(test_rules_2)}')
    print('Test parse_rules (2b)',
          'RIGHT' if len(test_messages_2) == 0 else f'WRONG!! Expected 0 but was {len(test_messages_2)}')

    test_check_rule('Test check non-terminal rnt1_a a pos 0', rnt1_a, 'a', 0, True)
    test_check_rule('Test check_rule 1 a', test_rules_1['0'], test_messages_1[0], 0, True)
    test_check_rule('Test check_rule 1 b', test_rules_1['0'], test_messages_1[1], 0, False)
    test_check_rule('Test check_rule 1 c', test_rules_1['0'], test_messages_1[2], 0, True)
    test_check_rule('Test check_rule 1 d', test_rules_1['0'], test_messages_1[3], 0, False)
    test_check_rule('Test check_rule 1 e', test_rules_1['0'], test_messages_1[4], 0, False)

    test_valid, test_invalid = filter_valid_messages_with_check(test_rules_1['0'], test_messages_1)
    expected_valid = ['ababbb', 'abbbab']
    expected_invalid = ['bababa', 'aaabbb', 'aaaabbb']
    print('Testing filter_valid_messages_with_check (valid)',
          'RIGHT' if test_valid == expected_valid else f'WRONG!! Expected {expected_valid} but was {test_valid}')
    print('Testing filter_valid_messages_with_check (invalid)',
          'RIGHT' if test_invalid == expected_invalid
          else f'WRONG!! Expected {expected_invalid} but was {test_invalid}')

    # SOLVING PART 1
    sol_rules, sol_messages = parse_rules(sol_raw_notes)
    sol_valid, sol_invalid = filter_valid_messages_with_check(sol_rules['0'], sol_messages)

    print('SOLUTION PART 1', len(sol_valid))

    # PART 2 is still work in progress!!!
    quit()

    print('PART 2')
    # TEST PART 2
    rnt5_S = RuleNonTerminal('0')
    # rnt5_A = RuleNonTerminal('A')
    rnt5_a = RuleTerminal('a', 'a')
    # rnt5_S.rule_sets.append([rnt5_A])
    # rnt5_A.rule_sets.append([rnt5_a])
    # rnt5_S.rule_sets.append([rnt5_A, rnt5_S])
    rnt5_S.rule_sets.append([rnt5_a])
    # rnt5_S.rule_sets.append([rnt5_a, rnt5_S])
    rnt5_S.rule_sets.append([rnt5_a, rnt5_a])
    rnt5_S.rule_sets.append([rnt5_a, rnt5_a, rnt5_a])
    rnt5_S.rule_sets.append([rnt5_a, rnt5_a, rnt5_a, rnt5_a])

    test_check_rule('Test check recursive rnt5_S a pos 0', rnt5_S, 'a', 0, True)
    test_check_rule('Test check recursive rnt5_S aa pos 0', rnt5_S, 'aa', 0, True)
    test_check_rule('Test check recursive rnt5_S aaa pos 0', rnt5_S, 'aaa', 0, True)
    test_check_rule('Test check recursive rnt5_S aaaaa pos 0', rnt5_S, 'aaaaa', 0, True)

    rnt6_S = RuleNonTerminal('0')
    rnt6_A = RuleNonTerminal('A')
    rnt6_B = RuleNonTerminal('B')
    rnt6_C = RuleNonTerminal('C')
    rnt6_a = RuleTerminal('a', 'a')
    rnt6_b = RuleTerminal('b', 'b')
    rnt6_A.rule_sets.append([rnt6_a])
    rnt6_B.rule_sets.append([rnt6_b])
    rnt6_C.rule_sets.append(([rnt6_A]))
    rnt6_S.rule_sets.append([rnt6_C, rnt6_B])
    rnt6_S.rule_sets.append([rnt6_C, rnt6_S, rnt6_B])

    test_check_rule('Test check recursive rnt6_S ab pos 0', rnt6_S, 'ab', 0, True)
    test_check_rule('Test check recursive rnt6_S aabb pos 0', rnt6_S, 'aabb', 0, True, verbose=True)
    test_check_rule('Test check recursive rnt6_S aaabbb pos 0', rnt6_S, 'aaabbb', 0, True)

    # Test
    test_rules_3, test_messages_3 = parse_rules(raw_test_rules_3)
    rule_8 = test_rules_3['8']
    rule_42 = test_rules_3['42']
    rule_8.rule_sets.append([rule_42, rule_8])

    rule_11 = test_rules_3['11']
    rule_31 = test_rules_3['31']
    # rule_11.rule_sets.append([rule_42, rule_11, rule_31])
    for i in range(10):
        the_list = []
        for j in range(i+1):
            the_list.append(rule_42)
        # the_list.append(rule_11)
        for j in range(i+1):
            the_list.append(rule_31)
        rule_11.rule_sets.append(the_list)


        test_valid, test_invalid = filter_valid_messages_with_check(test_rules_3['0'], test_messages_3)
        print(len(test_valid), test_valid)
        print(len(test_invalid))

        result, _ = test_rules_3['0'].check('babbbbaabbbbbabbbbbbaabaaabaaa', 0, verbose=True)

    # regenerate sol_rules
    sol_rules, sol_messages = parse_rules(sol_raw_notes)

    rule_8 = sol_rules['8']
    rule_42 = sol_rules['42']
    rule_8.rule_sets.append([rule_42, rule_8])
    # rule_8.rule_sets.append([rule_42, rule_42, rule_8])
    # rule_8.rule_sets.append([rule_42, rule_42, rule_42, rule_8])
    # rule_8.rule_sets.append([rule_42, rule_42, rule_42, rule_42, rule_8])

    rule_11 = sol_rules['11']
    rule_31 = sol_rules['31']
    # rule_11.rule_sets.append([rule_42, rule_42, rule_31, rule_31])
    # rule_11.rule_sets.append([rule_42, rule_42, rule_42, rule_31, rule_31, rule_31])
    # rule_11.rule_sets.append([rule_42, rule_42, rule_42, rule_42, rule_31, rule_31, rule_31, rule_31])
    rule_11.rule_sets.append([rule_42, rule_11, rule_31])

    print(sol_rules['0'])
    sol_valid, sol_invalid = filter_valid_messages_with_check(sol_rules['0'], sol_messages)

    print(len(sol_messages))
    print(len(sol_valid))
    print(len(sol_invalid))

    print('SOLUTION PART 2', len(sol_valid))
