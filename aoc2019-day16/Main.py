import numpy as np
from scipy.sparse import lil_matrix
from datetime import datetime
from joblib import Parallel, delayed
import multiprocessing
import shelve


def calculate_phase(int_input_sequence):
    original_pattern = [0, 1, 0, -1]
    int_output_sequence = []

    for i in range(1, len(int_input_sequence)+1):
        # expanding the original pattern as many times as iteration is, then flatten the list
        iteration_pattern = [item for sublist in map(lambda x: [x] * i, original_pattern) for item in sublist]
        # "cover" the input sequence with the iteration pattern, which will be repeated as many times as needed
        repeating = (len(int_input_sequence) // len(iteration_pattern)) + 1
        expanded_pattern = repeating * iteration_pattern
        # skip the very first value exactly once
        expanded_pattern = expanded_pattern[1:]
        # take as many items as length has the input sequence
        expanded_pattern = expanded_pattern[:len(int_input_sequence)]

        # do the magic...
        resultado = np.abs(np.sum([i*j for i, j in zip(int_input_sequence, expanded_pattern)])) % 10

        int_output_sequence.append(resultado)

    return int_output_sequence

def calculate_phases(input_sequence, n_phases, taking=None):
    # converting the input string into a int sequence
    int_input_sequence = [item for item in map(lambda x: int(x), input_sequence)]
    for phase in range(n_phases):
        # print(f'| {datetime.now()} | Calculating phase {phase}')
        int_input_sequence = calculate_phase(int_input_sequence)

    # print(f'| {datetime.now()} | Done!')
    if taking is None:
        output = int_input_sequence
    else:
        output = int_input_sequence[:taking]
    return ''.join(map(lambda x: str(x), output))


# TESTS
def test_day16_part1(test_id, sequence, n_phases, expected, taking=8):
    print(f'| {datetime.now()} | Begin test {test_id}!')
    result = calculate_phases(sequence, n_phases, taking)
    assert result == expected, f'| {datetime.now()} | {test_id} failed!! expected {expected}, result {result}'
    print(f'| {datetime.now()} | {test_id} success!!')


sequence_1 = '12345678'
sequence_2 = '80871224585914546619083218645595'
sequence_3 = '19617804207202209144916044189917'
sequence_4 = '69317163492948606335995924319873'
# TEST 1:
test_day16_part1('TEST 1', sequence_1, 1, '48226158')

# TEST 2:
test_day16_part1('TEST 2', sequence_1, 2, '34040438')

# TEST 3:
test_day16_part1('TEST 3', sequence_1, 3, '03415518')

# TEST 4:
test_day16_part1('TEST 4', sequence_1, 4, '01029498')

# TEST 5:
test_day16_part1('TEST 5', sequence_2, 100, '24176176')

# TEST 6:
test_day16_part1('TEST 6', sequence_3, 100, '73745418')

# TEST 7:
test_day16_part1('TEST 7', sequence_4, 100, '52432133')


# SOLUTION
input_16 = r'data\aoc2019-input-day16.txt'
with open(input_16, 'r') as f:
    data16 = f.read()

# print(f'| {datetime.now()} | Begin solving part 1!')
# result = calculate_phases(data16, 100, 8)
# print(result)
# print(f'| {datetime.now()} | Done.')

# >>>SOLUTION: 88323090


# PART 2
# def calculate_phase_fast(int_input_sequence):
#     '''This works!!!'''
#     # print(int_input_sequence)
#     limite = len(int_input_sequence)
#     resultado_oleada = np.zeros_like(int_input_sequence)
#     resultado_rangos = np.zeros_like(int_input_sequence)
#     resultado_oleada[limite-1] = int_input_sequence[limite-1]
#     # print('longitud int_input_sequence', len(int_input_sequence))
#     # result_number_rangos = 0
#     for i in range(limite -2, -1, -1):
#         # print('fila', i)
#         resultado_oleada[i] = resultado_oleada[i+1] + int_input_sequence[i]
#         # print(f'\tLlevábamos {resultado_oleada[i + 1]} y ahora le sumo {int_input_sequence[i]}, quedando {resultado_oleada[i]}')
#         if i <= len(int_input_sequence) / 2:
#             if i > 0:
#                 # print('\tresto posiciones', (2*i)+1, (2*i)+3, int_input_sequence[(2*i)+1:(2*i)+3])
#                 resultado_oleada[i] -= np.sum(int_input_sequence[(2*i)+1:(2*i)+3])
#             else:
#                 # print('\tprimera fila!')
#                 # print('\tresto posiciones', 1, 3, int_input_sequence[1:3])
#                 resultado_oleada[i] -= np.sum(int_input_sequence[1:3])
#
#         # print(f'\tResultado fila {i}. De momento llevamos {resultado_oleada[i]}')
#         indice_rangos = ((i+1) * 3) - 1
#         # print('\tindice_rangos', indice_rangos, 'limite', limite)
#         signo_rango = -1
#         rangos_calculados = 0
#         while indice_rangos < limite:
#             rangos_calculados += 1
#             # print(f'\tAplicamos rango con signo {signo_rango} con las posiciones {indice_rangos} a {indice_rangos+i+1} -> {int_input_sequence[indice_rangos:indice_rangos+i+1]}')
#             resultado_rangos[i] += signo_rango * np.sum(int_input_sequence[indice_rangos:indice_rangos+i+1])
#             # siguiente rango
#             signo_rango *= -1
#             indice_rangos += (i+1) * 2
#             # print(f'\t\tSiguiente rango que intentaremos aplicar será con signo {signo_rango} con las posiciones {indice_rangos} a {indice_rangos+i+1}')
#         # result_number_rangos += rangos_calculados
#         # print(f'fila {i}. Resultado oleada {resultado_oleada[i]}, resultado rangos {resultado_rangos[i]}, total fila: {resultado_oleada[i] + resultado_rangos[i]}')
#         # print(f'\tCalculada fila {i}. Rangos existentes: {rangos_calculados}')
#     # print('rangos alculados', result_number_rangos)
#     return np.abs(resultado_oleada + resultado_rangos) % 10

# BEGIN WIH ALL RANGES AS OVERLAP AND ADDING AND SUBSTRACTING

# def calculate_phase_fast(int_input_sequence):
#     '''Work in progress!!!'''
#     # print(int_input_sequence)
#     limite = len(int_input_sequence)
#     # resultado_all_rangos = np.zeros((int_input_sequence.shape[0], int_input_sequence.shape[0]//2), dtype=int)
#     resultado_all_rangos = lil_matrix((int_input_sequence.shape[0], int_input_sequence.shape[0]//2), dtype=int)
#     resultado_all_rangos[limite-1, 0] = int_input_sequence[limite-1]
#
#     # print('longitud int_input_sequence', len(int_input_sequence))
#     for i in range(limite -2, -1, -1):
#         # print('fila', i)
#         id_rango = 0
#         signo_rango = 1
#         indice_inicio_rango = i
#         indice_fin_rango = i * (id_rango + 2) + 1
#         while indice_inicio_rango < limite:
#             # print(f'Rango {id_rango}. Inicia el rango en {indice_inicio_rango}. Signo {signo_rango}')
#             # Do this range, at this row, overlap with itself at the "previous" row??
#             last_indice_inicio_rango = (i+1) + ((i+2) * 2) * id_rango
#             last_indice_fin_rango = last_indice_inicio_rango + (i + 1) + 1
#             # print(f'\tEste rango ocupa, en esta fila, {indice_inicio_rango}->{indice_fin_rango} y en la fila anterior ocupaba {last_indice_inicio_rango}->{last_indice_fin_rango}')
#             range_overlaps = indice_fin_rango > last_indice_inicio_rango
#             # print(f'\t\tOverlap: {range_overlaps}')
#             if range_overlaps:
#                 # Getting last row result for this range
#                 # print(f'\tEn la fila anterior este rango tenía de resultado {resultado_all_rangos[i+1, id_rango]}')
#                 resultado_all_rangos[i, id_rango] += resultado_all_rangos[i+1, id_rango]
#                 # "Adding" to range
#                 # print(indice_inicio_rango,last_indice_inicio_rango)
#                 # print(f'\tVoy a "añadir" al rango desde {indice_inicio_rango} -> {last_indice_inicio_rango}, es decir: {int_input_sequence[indice_inicio_rango:last_indice_inicio_rango]}')
#                 resultado_all_rangos[i, id_rango] += signo_rango * np.sum(int_input_sequence[indice_inicio_rango:last_indice_inicio_rango])
#                 # "Substracting" from range
#                 # TODO: If the end of the range is out of bounds, don't do anything!
#                 # print(f'\tVoy a "restar" al rango desde {indice_fin_rango} -> {last_indice_fin_rango}, es decir: {int_input_sequence[indice_fin_rango:last_indice_fin_rango]}')
#                 resultado_all_rangos[i, id_rango] -= signo_rango * np.sum(int_input_sequence[indice_fin_rango:last_indice_fin_rango])
#             else:
#                 # print('\tNo se superpone con la fila anterior. No tiene sentido arrastrar y manipular el dato de la fila anterior, lo recalculamos.')
#                 # print(f'\tEl rango se calcula sumando {int_input_sequence[indice_inicio_rango:indice_fin_rango]}. Signo {signo_rango}')
#                 resultado_all_rangos[i, id_rango] += signo_rango * np.sum(int_input_sequence[indice_inicio_rango:indice_fin_rango])
#             # print(resultado_all_rangos[i])
#             # print(resultado_all_rangos)
#             id_rango += 1
#             signo_rango *= -1
#             indice_inicio_rango += (i+1) * 2
#             indice_fin_rango += (i+1) * 2
#             # print(f'\tEl siguiente rango empezaría en {indice_inicio_rango} y terminaría en {indice_fin_rango}')
#
#     print(f'| {datetime.now()} | Terminada la fase, queda sumarlo todo y abs y % 10.')
#     return np.abs(np.sum(resultado_all_rangos, axis=1)) % 10

# ENDING WIH ALL RANGES AS OVERLAP AND ADDING AND SUBSTRACTING
def calculate_matrix_bazaar(int_input_sequence, int_output_sequence, x0, y0, xn, yn):
    pass


def calculate_matrix_slide(int_input_sequence, int_output_sequence, x0, y0, xn, yn):
    int_output_sequence[yn-1] += int_input_sequence[yn-1]
    for i in range(yn - 2, y0 - 1, -1):
        int_output_sequence[i] = int_output_sequence[i+1] + int_input_sequence[i]


def calculate_matrix_division(int_input_sequence, int_output_sequence, x0, y0, xn, yn):
    size = yn - y0
    print(f'| {datetime.now()} | calculate_matrix_division. {x0}->{xn}. Size {size}')
    if size > 5:
        # Still big size. Dividing input matrix into 4 and solving
        # TODO: Watch out of oddity
        new_x = (xn - x0) // 2
        new_y = (yn - y0) // 2
        print(f'| {datetime.now()} | \tDividing as {x0} -> {new_x}')
        # Solving upper left
        calculate_matrix_division(int_input_sequence, int_output_sequence, x0, y0, new_x, new_y)
        # Solving upper right
        calculate_matrix_bazaar(int_input_sequence, int_output_sequence, new_x, y0, xn, new_y)
        # Solving lower right
        calculate_matrix_slide(int_input_sequence, int_output_sequence, new_x, new_y, xn, yn)
        # Solving lower left
        # Just kidding, lower left is a 0 matrix :-)
    else:
        # Matrix small enough to solve as is
        pass


def calculate_phase_fast(int_input_sequence):
    int_ouput_sequence = np.zeros_like(int_input_sequence)
    max_pos = len(int_input_sequence)

    calculate_matrix_division(int_input_sequence, int_ouput_sequence, 0, 0, max_pos, max_pos)

    return int_ouput_sequence


def calculate_phases_fast(input_sequence, n_phases, taking=None):
    # converting the input string into a int sequence
    int_input_sequence = np.array([item for item in map(lambda x: int(x), input_sequence)], dtype=int)
    for phase in range(n_phases):
        print(f'| {datetime.now()} | Calculating phase {phase}')
        int_input_sequence = calculate_phase_fast(int_input_sequence)

    print(f'| {datetime.now()} | Done!')
    if taking is None:
        output = int_input_sequence
    else:
        output = int_input_sequence[:taking]
    return ''.join(map(lambda x: str(x), output))

tam = 20000
int_input = np.ones(tam, dtype=int)
int_output = np.zeros_like(int_input)
# calculate_matrix_slide(int_input, int_output, 0, 0, tam, tam)
calculate_matrix_division(int_input, int_output, 0, 0, tam, tam)
print(int_input)
print(int_output)
exit(0)

# input_sequence = sequence_1
# print('longitud es', len(input_sequence))
# int_input_sequence = np.array([item for item in map(lambda x: int(x), input_sequence)], dtype=int)
# zaska = calculate_phase_fast(int_input_sequence)
#
# print(zaska)
# print('48226158')
# print( np.abs(zaska) % 10 )

# BEGIN CALCULATING WITH BLOCKS AND PARALELISM

# def calculate_phase_block(int_input_sequence_block, expanded_pattern_block):
#     return np.sum([i * j for i, j in zip(int_input_sequence_block, expanded_pattern_block)])
#
# def split_sequences(int_input_sequence, expanded_pattern, block_size):
#     for i in range(0, len(int_input_sequence), block_size):
#         yield int_input_sequence[i:i+block_size], expanded_pattern[i:i+block_size]
#
# def calculate_phase_fast(int_input_sequence, block_size):
#     original_pattern = [0, 1, 0, -1]
#     int_output_sequence = []
#
#     for i in range(1, len(int_input_sequence)+1):
#         # expanding the original pattern as many times as iteration is, then flatten the list
#         iteration_pattern = [item for sublist in map(lambda x: [x] * i, original_pattern) for item in sublist]
#         # "cover" the input sequence with the iteration pattern, which will be repeated as many times as needed
#         repeating = (len(int_input_sequence) // len(iteration_pattern)) + 1
#         expanded_pattern = repeating * iteration_pattern
#         # skip the very first value exactly once
#         expanded_pattern = expanded_pattern[1:]
#         # take as many items as length has the input sequence
#         expanded_pattern = expanded_pattern[:len(int_input_sequence)]
#
#         # do the magic... in parallel...
#         retLst = Parallel(n_jobs=multiprocessing.cpu_count())(delayed(calculate_phase_block)(seq_block, exp_pattern_block) for seq_block, exp_pattern_block in split_sequences(int_input_sequence, expanded_pattern, block_size))
#         # print(type(retLst), retLst, np.sum(retLst))
#         resultado = np.abs(np.sum(retLst)) % 10
#         int_output_sequence.append(resultado)
#
#     return int_output_sequence

# def calculate_phases_fast(input_sequence, n_phases, block_size=10, taking=None):
#     # converting the input string into a int sequence
#     int_input_sequence = [item for item in map(lambda x: int(x), input_sequence)]
#     for phase in range(n_phases):
#         print(f'| {datetime.now()} | Calculating phase {phase}')
#         int_input_sequence = calculate_phase_fast(int_input_sequence, block_size)
#
#     # print(f'| {datetime.now()} | Done!')
#     if taking is None:
#         output = int_input_sequence
#     else:
#         output = int_input_sequence[:taking]
#     return ''.join(map(lambda x: str(x), output))

# def calculate_phases_with_offset(input_sequence, n_phases, taking=None):
#     real_sequence = 10000 * input_sequence
#     print(len(input_sequence), input_sequence)
#     print(len(real_sequence), real_sequence)
#
#     result = calculate_phases(real_sequence, n_phases)
#     offset = int(input_sequence[:7])
#     print(offset)
#     return result[offset:offset+8]

# def calculate_phase_fast(int_input_sequence, expanded_patterns):
#     int_output_sequence = []
#
#     for i in range(1, len(int_input_sequence)+1):
#         expanded_pattern = expanded_patterns[str(i)]
#
#         # do the magic...
#         resultado = np.abs(np.dot(int_input_sequence, expanded_pattern)) % 10
#
#         int_output_sequence.append(resultado)
#
#     return int_output_sequence


# def calculate_phases_fast(input_sequence, n_phases, taking=None):
#     # converting the input string into a int sequence
#     # int_input_sequence = [item for item in map(lambda x: int(x), input_sequence)]
#     int_input_sequence = np.array([item for item in map(lambda x: int(x), input_sequence)], dtype=int)
#     # calculating expanded patterns
#     print(f'| {datetime.now()} | Calculating expanded patterns')
#     expanded_patterns = shelve.open(r'c:\tmp\expanded_patterns_shelve')
#     original_pattern = [0, 1, 0, -1]
#     for i in range(1, len(int_input_sequence)+1):
#         # expanding the original pattern as many times as iteration is, then flatten the list
#         iteration_pattern = [item for sublist in map(lambda x: [x] * i, original_pattern) for item in sublist]
#         # "cover" the input sequence with the iteration pattern, which will be repeated as many times as needed
#         repeating = (len(int_input_sequence) // len(iteration_pattern)) + 1
#         expanded_pattern = repeating * iteration_pattern
#         # skip the very first value exactly once
#         expanded_pattern = expanded_pattern[1:]
#         # take as many items as length has the input sequence
#         expanded_pattern = expanded_pattern[:len(int_input_sequence)]
#         expanded_patterns[str(i)] = np.array(expanded_pattern, dtype=int)
#
#     print(f'| {datetime.now()} | Done.')
#     for phase in range(n_phases):
#         # print(f'| {datetime.now()} | Calculating phase {phase}')
#         int_input_sequence = calculate_phase_fast(int_input_sequence, expanded_patterns)
#
#     expanded_patterns.clear()
#     expanded_patterns.close()
#
#     # print(f'| {datetime.now()} | Done!')
#     if taking is None:
#         output = int_input_sequence
#     else:
#         output = int_input_sequence[:taking]
#     return ''.join(map(lambda x: str(x), output))

# END CALCULATING WITH BLOCKS AND PARALELISM

def calculate_phases_with_offset(input_sequence, n_phases, taking=None):
    real_sequence = 10000 * input_sequence
    # print(len(input_sequence), input_sequence)
    # print(len(real_sequence), real_sequence)

    result = calculate_phases_fast(real_sequence, n_phases, taking)
    offset = int(input_sequence[:7])
    print(offset)
    return result[offset:offset+8]

def test_day16_part2(test_id, sequence, n_phases, expected, taking=8):
    print(f'| {datetime.now()} | Begin test {test_id}!')
    result = calculate_phases_fast(sequence, n_phases, taking=taking)
    assert result == expected, f'| {datetime.now()} | {test_id} failed!! expected {expected}, result {result}'
    print(f'| {datetime.now()} | {test_id} success!!')

def test_day16_part2_with_offset(test_id, sequence, n_phases, expected):
    print(f'| {datetime.now()} | Begin test {test_id}!')
    result = calculate_phases_with_offset(sequence, n_phases, taking=None)
    assert result == expected, f'| {datetime.now()} | {test_id} failed!! expected {expected}, result {result}'
    print(f'| {datetime.now()} | {test_id} success!!')


# TEST
# test_day16_part2('TEST 1', '03036732577212944063491565474664', 100, '84462026')
#
# input_sequence = sequence_1
# print('48226158')
# int_input_sequence = np.array([item for item in map(lambda x: int(x), input_sequence)], dtype=int)
# zaska = calculate_phase_fast(int_input_sequence)
#
# print(zaska)
# exit(0)
# TEST 5
# test_day16_part2('TEST 5b', sequence_2, 100, '24176176')

# TEST 6:
# test_day16_part2('TEST 6b', sequence_3, 100, '73745418')

# TEST 7:
# test_day16_part2('TEST 7b', sequence_4, 100, '52432133')


# TEST 8
# ~ 10 sg avg time for a phase
# test_day16_part2_with_offset('TEST 8', '03036732577212944063491565474664', 100, '84462026')
# exit(0)
# TEST 9:
# test_day16_part2_with_offset('TEST 9', '02935109699940807407585447034323', 100, '78725270')

# TEST 10:
# test_day16_part2_with_offset('TEST 10', '03081770884921959731165446850517', 100, '53553731')


# ~26 min avg time for a phase xD
# test_day16_part2_with_offset('TEST 666', data16, 100, '84462026')

# print(f'| {datetime.now()} | Begin solving part 1! with parallel')
# result = calculate_phases_fast(data16, 100, taking=8)
# print(result)
# print(f'| {datetime.now()} | Done.')
