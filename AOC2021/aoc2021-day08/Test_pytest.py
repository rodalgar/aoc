from Main import parse_input, count_tokens_with_length_at, solve_line, solve_lines
from Token import Token

test_data_single_line = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"
test_data_multi_line = ["be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe",
                        "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc",
                        "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg",
                        "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb",
                        "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea",
                        "fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb",
                        "dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe",
                        "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef",
                        "egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb",
                        "gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"]


def get_single_parsed_line():
    return [[[Token('acedgfb'), Token('cdfbe'), Token('gcdfa'), Token('fbcad'), Token('dab'), Token('cefabd'),
              Token('cdfgeb'),
              Token('eafb'), Token('cagedb'), Token('ab')],
             [Token('cdfeb'), Token('fcadb'), Token('cdfeb'), Token('cdbaf')]]]


def get_multi_parsed_line():
    return [[[Token('be'), Token('cfbegad'), Token('cbdgef'), Token('fgaecd'), Token('cgeb'), Token('fdcge'),
              Token('agebfd'), Token('fecdb'), Token('fabcd'), Token('edb')],
             [Token('fdgacbe'), Token('cefdb'), Token('cefbgd'), Token('gcbe')]],
            [[Token('edbfga'), Token('begcd'), Token('cbg'), Token('gc'), Token('gcadebf'), Token('fbgde'),
              Token('acbgfd'), Token('abcde'), Token('gfcbed'), Token('gfec')],
             [Token('fcgedb'), Token('cgb'), Token('dgebacf'), Token('gc')]],
            [[Token('fgaebd'), Token('cg'), Token('bdaec'), Token('gdafb'), Token('agbcfd'), Token('gdcbef'),
              Token('bgcad'), Token('gfac'), Token('gcb'), Token('cdgabef')],
             [Token('cg'), Token('cg'), Token('fdcagb'), Token('cbg')]],
            [[Token('fbegcd'), Token('cbd'), Token('adcefb'), Token('dageb'), Token('afcb'), Token('bc'),
              Token('aefdc'), Token('ecdab'), Token('fgdeca'), Token('fcdbega')],
             [Token('efabcd'), Token('cedba'), Token('gadfec'), Token('cb')]],
            [[Token('aecbfdg'), Token('fbg'), Token('gf'), Token('bafeg'), Token('dbefa'), Token('fcge'),
              Token('gcbea'), Token('fcaegb'), Token('dgceab'), Token('fcbdga')],
             [Token('gecf'), Token('egdcabf'), Token('bgf'), Token('bfgea')]],
            [[Token('fgeab'), Token('ca'), Token('afcebg'), Token('bdacfeg'), Token('cfaedg'), Token('gcfdb'),
              Token('baec'), Token('bfadeg'), Token('bafgc'), Token('acf')],
             [Token('gebdcfa'), Token('ecba'), Token('ca'), Token('fadegcb')]],
            [[Token('dbcfg'), Token('fgd'), Token('bdegcaf'), Token('fgec'), Token('aegbdf'), Token('ecdfab'),
              Token('fbedc'), Token('dacgb'), Token('gdcebf'), Token('gf')],
             [Token('cefg'), Token('dcbef'), Token('fcge'), Token('gbcadfe')]],
            [[Token('bdfegc'), Token('cbegaf'), Token('gecbf'), Token('dfcage'), Token('bdacg'), Token('ed'),
              Token('bedf'), Token('ced'), Token('adcbefg'), Token('gebcd')],
             [Token('ed'), Token('bcgafe'), Token('cdgba'), Token('cbgef')]],
            [[Token('egadfb'), Token('cdbfeg'), Token('cegd'), Token('fecab'), Token('cgb'), Token('gbdefca'),
              Token('cg'), Token('fgcdab'), Token('egfdb'), Token('bfceg')],
             [Token('gbdfcae'), Token('bgc'), Token('cg'), Token('cgb')]],
            [[Token('gcafb'), Token('gcf'), Token('dcaebfg'), Token('ecagb'), Token('gf'), Token('abcdeg'),
              Token('gaef'), Token('cafbge'), Token('fdbac'), Token('fegbdc')],
             [Token('fgae'), Token('cfgab'), Token('fg'), Token('bagce')]]]


def test_parse_input():
    data = parse_input(test_data_single_line)
    assert data[0][0].signals == Token('acedgfb').signals
    assert data[0][1].signals == Token('cdfbe').signals
    assert data[0][2].signals == Token('gcdfa').signals
    assert data[0][3].signals == Token('fbcad').signals
    assert data[0][4].signals == Token('dab').signals
    assert data[0][5].signals == Token('cefabd').signals
    assert data[0][6].signals == Token('cdfgeb').signals
    assert data[0][7].signals == Token('eafb').signals
    assert data[0][8].signals == Token('cagedb').signals
    assert data[0][9].signals == Token('ab').signals

    assert data[1][0].signals == Token('cdfeb').signals
    assert data[1][1].signals == Token('fcadb').signals
    assert data[1][2].signals == Token('cdfeb').signals
    assert data[1][3].signals == Token('cdbaf').signals


def test_count_tokens_with_length_at():
    test_data = get_multi_parsed_line()
    data = count_tokens_with_length_at(test_data, Token.special_lengths, 1)
    assert len(data) == 26


def test_solve_line():
    test_data = get_single_parsed_line()[0]
    data = solve_line(test_data)
    assert data == 5353


def test_solve_lines():
    test_data = get_multi_parsed_line()
    data = solve_lines(test_data)
    assert data == 61229
