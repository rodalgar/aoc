# Day 16: Ticket Translation
import re


# PART 1
def parse_category(line):
    """
    Parses a string that represents a category and its ranges.

    :param line: string representing a category.
    :return: Tuple (x, y, z, i, k) being x category name, y-z first range and i-k the second range.
    """
    (cat, min1, max1, min2, max2) = re.findall("^([^:]+): (\d+)-(\d+) or (\d+)-(\d+)$", line)[0]

    return cat, int(min1), int(max1), int(min2), int(max2)


def parse_ticket(line):
    """
    Parses a string that represents a ticket.

    :param line: string representing a ticket.
    :return: list of int representing values of the ticket.
    """
    return [int(x) for x in line.split(',')]


def parse_raw_tickets(raw_input):
    """
    Parses raw input notes into parsed sections.

    :param raw_input: List of string representing raw notes.
    :return: Tuple (x, y, z) being x list of test_categories, y my ticket and z list of nearby tickets.
    """

    parsing = 0
    num_item = 0

    nearby_tickets = []
    categories = []
    my_ti = None
    for i in range(len(raw_input)):
        num_item += 1
        line = raw_input[i]
        if len(line) == 0:
            parsing += 1
            num_item = 0
            continue

        if parsing == 0:
            # test_categories
            categories.append(parse_category(line))
        elif parsing == 1:
            # Ignore first line of my ticket section.
            if num_item == 1:
                continue
            # my ticket
            my_ti = parse_ticket(line)
        else:
            # Ignore first line of nearby tickets section.
            if num_item == 1:
                continue
            nearby_tickets.append(parse_ticket(line))

    return categories, my_ti, nearby_tickets


def validate_ticket(ticket, categories, verbose=False):
    """
    Checks if all values of ticket are found inside of one of the ranges of at least one category. Values that fail to
    comply to at least one category are kept under 'unassigned_data'. The function also checks if a category holds
    just only one value of the ticket (it keeps it under 'category_assignments') it it can hold more than one value
    is kept under 'category_candidates'.

    :param ticket: Ticket to validate.
    :param categories: Categories to check the ticket to.
    :param verbose: If True additional info will be printed.
    :return: Tuple (x, y, z, i) being x True if ticket is valid, y as 'category_assignments', z as
        'category_candidates' and i as 'unassigned_data'.
    """

    if verbose:
        print('Validating', ticket)
    category_candidates = {}
    category_assignments = {}
    unassigned_data = list(range(len(ticket)))
    # for data in ticket:
    for ix in range(len(ticket)):
        data = ticket[ix]
        if verbose:
            print(f'\tData is {data}')
        for cat in categories:
            if verbose:
                print(f'\tCat is {cat}')
            if (cat[1] <= data <= cat[2]) or (cat[3] <= data <= cat[4]):
                if verbose:
                    print('\t\tOK!!!')
                if cat not in category_candidates:
                    category_candidates[cat] = []
                category_candidates[cat].append(ix)
                if ix in unassigned_data:
                    unassigned_data.remove(ix)

    if verbose:
        print('Assigning values to categories as candidates finished.', ticket, category_candidates)

    while True:
        if verbose:
            print('Removing already processed categories...', category_candidates)
        category_candidates = {k: v for k, v in category_candidates.items() if len(v) > 0}
        if verbose:
            print('Looking for candidates', category_candidates)
        some_candidate_was_assigned = False
        for cat, candidates in category_candidates.items():
            if verbose:
                print('FOR', cat, candidates)
            if len(candidates) > 1:
                if verbose:
                    print('More than one candidate to chose from. We will wait to see if another category picks one '
                          'of them and removes ambiguity...')
                continue
            if cat in category_assignments:
                if verbose:
                    print(f'Category {cat} already has assigned candidates: {category_assignments[cat]}')
                continue

            # Direct assignment
            if verbose:
                print(f'BINGO! Category has just one candidate! Direct assignment!')
            candidate = candidates[0]
            category_assignments[cat] = candidate
            some_candidate_was_assigned = True
            if verbose:
                print('\t\t\t', category_candidates, category_assignments)
            for other_cat, other_candidates in category_candidates.items():
                if candidate in other_candidates:
                    category_candidates[other_cat].remove(candidate)
            if verbose:
                print('\t\t\t', category_candidates, category_assignments)

        if verbose:
            print('Status:')
            print(f'\tcategory_candidates {category_candidates}')
            print(f'\tcategory_assignments {category_assignments}')

        if len(category_candidates) == 0:
            if verbose:
                print('All categories have been processed!!')
            break

        if not some_candidate_was_assigned:
            if verbose:
                print('No more candidates can be asigned.')
            return len(unassigned_data) == 0, category_assignments, category_candidates, unassigned_data

    if len(unassigned_data) > 0:
        if verbose:
            print(f'There are {len(unassigned_data)} ticket values that could not be assigned to any category...')
        return False, category_assignments, category_candidates, unassigned_data

    return True, category_assignments, category_candidates, unassigned_data


def get_scanning_error_rate(ticket, categories):
    """
    Get the scanning_error_rate of a ticket.

    :param ticket: Parsed ticket.
    :param categories: List of parsed categories.
    :return: Sum of ticket values that could not be assigned to any category.
    """
    isvalid, assign, remaining, unassigned = validate_ticket(ticket, categories)
    ser = 0
    if not isvalid:
        for una in unassigned:
            ser += ticket[una]
    return ser


def get_ser_from_tickets(tickets, categories):
    """
    Gets the scanning_error_rate of a list of tickets.

    :param tickets: List of parsed tickets.
    :param categories: List of parsed categories.
    :return: Sum of scanning_error_rate of every ticket.
    """
    total_ser = 0
    for t in tickets:
        total_ser += get_scanning_error_rate(t, categories)
    return total_ser


# PART 2
def filter_valid_tickets(tickets, categories, verbose=False):
    """
    Given a list of tickets, filters out all invalid tickets and returns every possible direct assignment of a ticket
    value to a category and the remaining categories to assign values to and their candidates.

    :param tickets: List of parsed tickets.
    :param categories: List of parsed categories.
    :param verbose: If True additional info will be printed.
    :return: List of tuple (x, y) being x dictionary of direct assignments and y dictionary of unassigned categories
    and their candidates.
    """
    valid_tickets = []
    for ticket in tickets:
        isvalid, assign, remaining, unassigned = validate_ticket(ticket, categories)

        if isvalid:
            if verbose:
                print(isvalid, assign, remaining, unassigned)
            valid_tickets.append((ticket, assign, remaining))
        else:
            if verbose:
                print(f'Ticket {ticket} is invalid!')
    return valid_tickets


def guess_assignments(valid_tickets, verbose=False):
    """
    Given a list of direct category assignments the function guesses which one of the possible candidates of each
    remaining unassigned category will fit in. The algorithm keeps iterating over the unassigned categories finding
    common occurrences category-value and goes on narrowing down possibilities until there is only one candidate for
    each category.

    :param valid_tickets: List of tuple, representing direct assignments already done and the remaining unassigned
    categories.
    :param verbose: If True additional info will be printed.
    :return: Tuple (x, y) being x all assigned categories and y remaining unassigned categories.
    """
    assigned_categories = {}
    remaining_categories = {}
    for valid_ticket in valid_tickets:
        _, direct_assignment, remaining = valid_ticket
        for k, v in direct_assignment.items():
            if verbose:
                print(f'Assigning to category {k} value {v}')
            if k in assigned_categories and direct_assignment[k] != v:
                raise Exception(f'\tThere was already a different direct assignment '
                                f'to category {k}: {direct_assignment[k]}')
            else:
                assigned_categories[k] = v
        for k, v in remaining.items():
            if verbose:
                print(f'Storing unassigned category {k} along with its candidates {v}')
            if k not in remaining_categories:
                remaining_categories[k] = []
            remaining_categories[k].append(v)

    if verbose:
        print(f'assigned_categories: {assigned_categories} remaining_categories: {remaining_categories}')

    while True:
        # Generate new direct assignments
        if verbose:
            print("Analyzing 'remaining' to generate new direct assignments.")
        remaining_categories_to_remove = set()
        for k, v in remaining_categories.items():
            if verbose:
                print(f'\tAnalyzing {k}')
            common_values = None
            for candidates in v:
                if common_values is None:
                    common_values = set(candidates)
                else:
                    common_values = common_values.intersection(candidates)
            if verbose:
                print(f'\t\tcommon_values: {common_values}')
            if len(common_values) == 1:
                unique_value = list(common_values)[0]
                if verbose:
                    print(f'DING! Direct assignment can be made! category {k} is assigned value  {unique_value}')

                assigned_categories[k] = unique_value
                # Marking category to be removed when the loop ends as it has been determined which candidate to use.
                remaining_categories_to_remove.add(k)

                # As the value has been just assigned to category k we remove this value of every candidate list of the
                # remaining categories (it won't be assigned to another category)
                for _, v2 in remaining_categories.items():
                    for candidates in v2:
                        if unique_value in candidates:
                            candidates.remove(unique_value)

        # Removing marked categories.
        for k in remaining_categories_to_remove:
            del (remaining_categories[k])

        if len(remaining_categories) == 0:
            break

    return assigned_categories, remaining_categories


def solve_part_2(my_ticket, assignments):
    """
    Function to solve part 2. It gets categories that start with 'departure' and accumulate the ticket value it its
    position.
    :param my_ticket: my ticket.
    :param assignments: Direct assignments done.
    :return: Multiplicative accumulation of ticket values at positions stated by categories which start with 'departure'
    """
    part_2_solution = 1
    for k, v in assignments.items():
        if k[0].startswith('departure'):
            part_2_solution *= my_ticket[v]

    return part_2_solution


def test_validate_ticket(case_ticket, case_categories, expected_value):
    """
    Function to test validate_ticket.

    :param case_ticket: test case ticket.
    :param case_categories: test case categories.
    :param expected_value: expected value.
    """
    result, _, _, _ = validate_ticket(case_ticket, case_categories)
    print('Test validate_ticket', case_ticket,
          'RIGHT' if result == expected_value else f'WRONG!! Expected {expected_value} but was {result}')


def test_get_scanning_error_rate(case_ticket, case_categories, expected_value):
    """
    Function to test get_scanning_error_rate.

    :param case_ticket: test case ticket.
    :param case_categories: test case categories.
    :param expected_value: expected value.
    :return:
    """
    result = get_scanning_error_rate(case_ticket, case_categories)
    print('Test get_scanning_error_rate', case_ticket,
          'RIGHT' if result == expected_value else f'WRONG!! Expected {expected_value} but was {result}')


if __name__ == '__main__':
    with open('data/aoc2020-input-day16.txt', 'r') as f:
        sol_notes = [line.strip('\n') for line in f.readlines()]

    print('PART 1')
    # TEST PART 1
    test_notes = ['class: 1-3 or 5-7',
                  'row: 6-11 or 33-44',
                  'seat: 13-40 or 45-50',
                  '',
                  'your ticket:',
                  '7,1,14',
                  '',
                  'nearby tickets:',
                  '7,3,47',
                  '40,4,50',
                  '55,2,20',
                  '38,6,12']

    test_notes_2 = ['class: 0-1 or 4-19',
                    'row: 0-5 or 8-19',
                    'seat: 0-13 or 16-19',
                    '',
                    'your ticket:',
                    '11,12,13',
                    '',
                    'nearby tickets:',
                    '3,9,18',
                    '15,1,5',
                    '5,14,9']

    test_categories, test_my_ticket, test_nearby_tickets = parse_raw_tickets(test_notes)
    expected = 3
    print('Test parse_raw_tickets, test_categories',
          'RIGHT' if len(test_categories) == expected
          else f'WRONG!! Expected {expected} but was {len(test_categories)}')
    expected = [7, 1, 14]
    print('Test parse_raw_tickets, test_my_ticket',
          'RIGHT' if test_my_ticket == expected else f'WRONG!! Expected {expected} but was {test_my_ticket}')
    expected = 4
    print('Test parse_raw_tickets, test_nearby_tickets',
          'RIGHT' if len(test_nearby_tickets) == expected
          else f'WRONG!! Expected {expected} but was {len(test_nearby_tickets)}')

    test_validate_ticket([7, 3, 47], test_categories, True)
    test_validate_ticket([40, 4, 50], test_categories, False)
    test_validate_ticket([55, 2, 20], test_categories, False)
    test_validate_ticket([38, 6, 12], test_categories, False)

    test_get_scanning_error_rate([7, 3, 47], test_categories, 0)
    test_get_scanning_error_rate([40, 4, 50], test_categories, 4)
    test_get_scanning_error_rate([55, 2, 20], test_categories, 55)
    test_get_scanning_error_rate([38, 6, 12], test_categories, 12)

    foo = get_ser_from_tickets(test_nearby_tickets, test_categories)
    print('Test get_ser_from_tickets', 'RIGHT' if foo == 71 else f'WRONG!! Expected {71} but was {expected}')

    # SOLVE PART 1
    sol_categories, sol_my_ticket, sol_nearby_tickets = parse_raw_tickets(sol_notes)
    foo = get_ser_from_tickets(sol_nearby_tickets, sol_categories)
    print('SOLUTION PART 1', foo)
    print()

    print('PART 2')
    # TEST PART 2
    categories_2, my_ticket_2, nearby_tickets_2 = parse_raw_tickets(test_notes_2)

    test_valid_tickets = filter_valid_tickets(test_nearby_tickets, test_categories)
    test_valid_tickets_2 = filter_valid_tickets(nearby_tickets_2, categories_2)

    print('Test filter_valid_tickets (1)',
          'RIGHT' if len(test_valid_tickets) == 1 else f'WRONG!! Expected 1 but was {len(test_valid_tickets)}')
    print('Test filter_valid_tickets (2)',
          'RIGHT' if len(test_valid_tickets_2) == 3 else f'WRONG!! Expected 3 but was {len(test_valid_tickets_2)}')

    test_assigned, test_unassigned = guess_assignments(test_valid_tickets_2)
    print('Test guess_assignment (1)',
          'RIGHT' if test_assigned[('seat', 0, 13, 16, 19)] == 2
          else f"WRONG!! Expected 2 but was {test_assigned[('seat', 0, 13, 16, 19)]}")
    print('Test guess_assignment (2)',
          'RIGHT' if test_assigned[('class', 0, 1, 4, 19)] == 1
          else f"WRONG!! Expected 1 but was {test_assigned[('class', 0, 1, 4, 19)]}")
    print('Test guess_assignment (3)',
          'RIGHT' if test_assigned[('row', 0, 5, 8, 19)] == 0
          else f"WRONG!! Expected 0 but was {test_assigned[('row', 0, 5, 8, 19)]}")

    print('Test guess_assignments, test_unassigned',
          'RIGHT' if len(test_unassigned) == 0 else f'WRONG!! Expected 0 but was {len(test_unassigned)}')

    # SOLVE PART 2
    sol_valid_tickets = filter_valid_tickets(sol_nearby_tickets, sol_categories)
    sol_assigned, sol_unassigned = guess_assignments(sol_valid_tickets)
    solution = solve_part_2(sol_my_ticket, sol_assigned)
    print('SOLUTION PART 2', solution)
