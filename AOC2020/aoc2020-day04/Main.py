# DAY 4: Passport Processing
import re


# Utility functions
def parse_batch(lines):
    """
    Transform a list of strings (raw input) into a list of dictionaries, one for each parsed password.

    :param lines: List of strings from the raw input.
    :return: List of dictionaries, one for each password.
    """

    result_batch = []
    password = {}
    for line in lines:
        if len(line) == 0:
            result_batch.append(password)
            password = {}
        else:
            for word in line.split(' '):
                chunk = word.split(':')
                # TODO: Should we check for malformed strings?
                # TODO: Should we check if verb already exists?
                password[chunk[0]] = chunk[1]

    # last line
    if len(password) > 0:
        result_batch.append(password)

    return result_batch


def test_validation_function(function, value, expected):
    """
    Function to test field validations at part 2

    :param function: Validation function to test.
    :param value: Value to test function to.
    :param expected: Expected value from function.
    :return: Whether function returns the expected value or not.
    """
    result = function(value)
    print(f'{function}', 'RIGHT' if result == expected else f'WRONG, obtained {result}, expected {expected}')


# PART 1
def get_passwords_with_length_ok(passwords):
    """
    Filters all passwords that do not follow length policies. All passwords must have all 8 entries with value. Entry
    cid is an exception as it is optional.

    :param passwords: List of parsed passwords to filter
    :return: List of parsed password which follow length policies.
    """

    valid_passwords = []

    for password in passwords:
        if len(password) == 8:
            valid_passwords.append(password)
        elif len(password) == 7 and 'cid' not in password:
            valid_passwords.append(password)

    # [password for password in passwords if len(password) == 8 or (len(password) == 7 and ('cid' not in password))]

    return valid_passwords


# PART 2
def check_is_int_in_range(value, min_value, max_value):
    """
    Checks if a string contains a 4 digit integer and, if it does, whether it is in the range defined by min_value and
    max_value or not.

    :param value: string containing the number.
    :param min_value: minimum value accepted for value.
    :param max_value: maximum value accepted for value.
    :return:
    """
    if len(value) != 4:
        return False
    if re.match("\d{4}", value):
        int_value = int(value)
        return min_value <= int_value <= max_value
    return False


# PASSWORD FIELD VALIDATIONS
def validate_byr(value):
    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    return check_is_int_in_range(value, 1920, 2002)


def validate_iyr(value):
    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    return check_is_int_in_range(value, 2010, 2020)


def validate_eyr(value):
    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    return check_is_int_in_range(value, 2020, 2030)


def validate_ecl(value):
    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    return value in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']


def validate_pid(value):
    # pid (Passport ID) - a nine-digit number, including leading zeroes
    if len(value) != 9:
        return False
    return re.match("\d{9}", value) is not None


def validate_cid(value):
    # cid (Country ID) - ignored, missing or not.
    return True


def validate_hcl(value):
    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    return re.match("#[0-9a-f]{6}", value) is not None


def validate_hgt(value):
    # hgt (Height) - a number followed by either cm or in:
    #   If cm, the number must be at least 150 and at most 193.
    #   If in, the number must be at least 59 and at most 76.
    if re.match("\d+in", value):
        data = int(value.replace("in", ""))
        return 59 <= data <= 76
    elif re.match("\d+cm", value):
        data = int(value.replace("cm", ""))
        return 150 <= data <= 193
    return False


def check_if_all_fields_are_ok(passwords, verbose=False):
    """
    Filters all passwords that contains invalid fields.

    :param verbose: If True additional info will be printed.
    :param passwords: List of parsed passwords.
    :return: List of parsed passwords whose fields are all valid.
    """

    valid_passwords = []
    for password in passwords:
        # Everybody is True until proven False
        password_valid = True
        for field_name, field_value in password.items():
            if field_name == 'byr':
                password_valid = password_valid and validate_byr(field_value)
            elif field_name == 'iyr':
                password_valid = password_valid and validate_iyr(field_value)
            elif field_name == 'eyr':
                password_valid = password_valid and validate_eyr(field_value)
            elif field_name == 'ecl':
                password_valid = password_valid and validate_ecl(field_value)
            elif field_name == 'pid':
                password_valid = password_valid and validate_pid(field_value)
            elif field_name == 'cid':
                password_valid = password_valid and validate_cid(field_value)
            elif field_name == 'hcl':
                password_valid = password_valid and validate_hcl(field_value)
            elif field_name == 'hgt':
                password_valid = password_valid and validate_hgt(field_value)
            else:
                # unknown field name... invalid!
                print(f'Password {password} has unknown field name: {field_name} ({field_value}). INVALID! BWAHAHA!')
                password_valid = False

            if verbose and not password_valid:
                print(f'Password {password} has invalid value on field {field_name}  ({field_value})')
                break

        if password_valid:
            valid_passwords.append(password)
    return valid_passwords


if __name__ == '__main__':
    with(open('data/aoc2020-input-day04.txt', 'r')) as f:
        sol_raw = [line.strip('\n') for line in f.readlines()]

    print('PART 1')
    # TEST PART 1
    test_batch = ['ecl:gry pid:860033327 eyr:2020 hcl:#fffffd',
        'byr:1937 iyr:2017 cid:147 hgt:183cm',
        '',
        'iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884',
        'hcl:#cfa07d byr:1929',
        '',
        'hcl:#ae17e1 iyr:2013',
        'eyr:2024',
        'ecl:brn pid:760753108 byr:1931',
        'hgt:179cm',
        '',
        'hcl:#cfa07d eyr:2025 pid:166559648',
        'iyr:2011 ecl:brn hgt:59in']

    test_result = parse_batch(test_batch)
    print('Testing parse_batch:', 'RIGHT' if len(test_result) == 4 else 'WRONG!!')
    valid_passwords = get_passwords_with_length_ok(test_result)
    print('Testing get_passwords_with_length_ok', 'RIGHT' if len(valid_passwords) == 2 else 'WRONG!!')

    # SOLVING PART 1
    sol_valids = get_passwords_with_length_ok(parse_batch(sol_raw))

    print('SOLUTION PART 1', len(sol_valids))

    print('PART 2')
    # TEST PART 2
    print('TESTING FIELD VALIDATIONS')
    # byr valid:   2002
    # byr invalid: 2003
    test_validation_function(validate_byr, '2002', True)
    test_validation_function(validate_byr, '2003', False)
    # hgt valid:   60in
    # hgt valid:   190cm
    # hgt invalid: 190in
    # hgt invalid: 190
    test_validation_function(validate_hgt, '60in', True)
    test_validation_function(validate_hgt, '190cm', True)
    test_validation_function(validate_hgt, '190in', False)
    test_validation_function(validate_hgt, '190', False)
    # hcl valid:   #123abc
    # hcl invalid: #123abz
    # hcl invalid: 123abc
    test_validation_function(validate_hcl, '#123abc', True )
    test_validation_function(validate_hcl, '#123abz', False )
    test_validation_function(validate_hcl, '123abc', False )
    # ecl valid:   brn
    # ecl invalid: wat
    test_validation_function(validate_ecl, 'brn', True)
    test_validation_function(validate_ecl, 'wat', False)
    # pid valid:   000000001
    # pid invalid: 0123456789
    test_validation_function(validate_pid, '000000001', True)
    test_validation_function(validate_pid, '0123456789', False)

    print('Testing all fields')
    print('Invalid passwords')
    test_invalid_passwords = ['eyr:1972 cid:100',
        'hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926',
        '',
        'iyr:2019',
        'hcl:#602927 eyr:1967 hgt:170cm',
        'ecl:grn pid:012533040 byr:1946',
        '',
        'hcl:dab227 iyr:2012',
        'ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277',
        '',
        'hgt:59cm ecl:zzz',
        'eyr:2038 hcl:74454a iyr:2023',
        'pid:3556412378 byr:2007']

    foo = check_if_all_fields_are_ok(get_passwords_with_length_ok(parse_batch(test_invalid_passwords)), verbose=True)
    print('Testing, all passwords invalid:', 'RIGHT' if len(foo) == 0 else f'WRONG! Expecting 0 valid but was ({len(foo)})')

    print('Valid passwords')
    test_valid_passwords = ['pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980',
        'hcl:#623a2f',
        '',
        'eyr:2029 ecl:blu cid:129 byr:1989',
        'iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm',
        '',
        'hcl:#888785',
        'hgt:164cm byr:2001 iyr:2015 cid:88',
        'pid:545766238 ecl:hzl',
        'eyr:2022',
        '',
        'iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719']

    foo = check_if_all_fields_are_ok(get_passwords_with_length_ok(parse_batch(test_valid_passwords)))
    print('Testing, all passwords valid:', 'RIGHT' if len(foo) == 4 else f'WRONG! Expecting 4 valid but was ({len(foo)})')

    # SOLVING PART 2
    foo = check_if_all_fields_are_ok(get_passwords_with_length_ok(parse_batch(sol_raw)))
    print('SOLUTION PART 2', len(foo))
