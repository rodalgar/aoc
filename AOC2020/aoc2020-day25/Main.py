# Day 25: Combo Breaker


def obtain_loop_size(base, modulus, public_key, verbose=False):
    """Instructions to obtain loop size is the same as performing modular exponentiation (with base `b` 7
    and `modulus` 20201227) until an exponent `e` is found such as `b ^ e mod modulus` equals the public key.
    """
    i = 1
    while True:
        if public_key == pow(base, i, modulus):
            return i
        i += 1
        if verbose and i % 1000000 == 0:
            print(i)
    return None


def get_encryption_key(public_key_device_1, loop_size_device_2, modulus):
    """Obtains the encryption key applying key of device 2 to public key of device 1"""
    return pow(public_key_device_1, loop_size_device_2, modulus)


if __name__ == '__main__':
    with open('data/aoc2020-input-day25.txt', 'r') as f:
        public_keys = [int(line.strip('\n')) for line in f.readlines()]

    device_1_public_key = public_keys[0]
    device_2_public_key = public_keys[1]
    modulo = 20201227
    subject_number = 7

    test_cards_public_key = 5764801
    test_doors_public_key = 17807724

    print('PART 1')
    # TEST PART 1
    expected_loop_size_door = 11
    loop_size_door = obtain_loop_size(subject_number, modulus=modulo, public_key=test_doors_public_key)
    print('Testing obtain_loop_size (door)',
          'RIGHT' if expected_loop_size_door == loop_size_door
          else f'WRONG!! Expected {expected_loop_size_door} but was {loop_size_door}')

    expected_loop_size_card = 8
    loop_size_card = obtain_loop_size(subject_number, modulus=modulo, public_key=test_cards_public_key)
    print('Testing obtain_loop_size (card)',
          'RIGHT' if expected_loop_size_card == loop_size_card
          else f'WRONG!! Expected {expected_loop_size_card} but was {loop_size_card}')

    expected_encryption_key = 14897079
    test_encryption_key = get_encryption_key(test_cards_public_key, loop_size_door, modulo)
    print('Testing get_encryption_key (card)',
          'RIGHT' if expected_encryption_key == test_encryption_key
          else f'WRONG!! Expected {expected_encryption_key} but was {test_encryption_key}')

    test_encryption_key = get_encryption_key(test_doors_public_key, loop_size_card, modulo)
    print('Testing get_encryption_key (door)',
          'RIGHT' if expected_encryption_key == test_encryption_key
          else f'WRONG!! Expected {expected_encryption_key} but was {test_encryption_key}')

    # SOLVING PART 1
    print('Solving part 1:')
    loop_size_device1 = obtain_loop_size(subject_number, modulus=modulo, public_key=device_1_public_key)
    print(f'Loop size of device 1 ({device_1_public_key}) is {loop_size_device1}')

    loop_size_device2 = obtain_loop_size(subject_number, modulus=modulo, public_key=device_2_public_key)
    print(f'Loop size of device 2 ({device_2_public_key}) is {loop_size_device2}')

    ek_device1 = get_encryption_key(device_1_public_key, loop_size_device2, modulo)
    ek_device2 = get_encryption_key(device_2_public_key, loop_size_device1, modulo)

    print(f'Encryption keys of device 1 {ek_device1}')
    print(f'Encryption keys of device 2 {ek_device2}')

    print('SOLUTION PART 1:', ek_device1)
