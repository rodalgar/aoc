# Day 18: Operation Order
import re


# PART 1
class Expression:
    def evaluate(self):
        pass


class UnaryExpression(Expression):
    param_a = None

    def __init__(self, a):
        self.param_a = a


class BinaryExpression(UnaryExpression):
    param_b = None

    def __init__(self, a, b):
        super().__init__(a)
        self.param_b = b


class LiteralExpression(UnaryExpression):

    def evaluate(self):
        return self.param_a

    def __repr__(self):
        return f'{self.param_a}'


class AdditionExpression(BinaryExpression):

    def evaluate(self):
        return self.param_a.evaluate() + self.param_b.evaluate()

    def __repr__(self):
        return f'({self.param_a} + {self.param_b})'


class MultiplicationExpression(BinaryExpression):

    def evaluate(self):
        return self.param_a.evaluate() * self.param_b.evaluate()

    def __repr__(self):
        return f'({self.param_a} * {self.param_b})'


TOKEN_BEGIN_EXPRESSION = 'TOKEN_BEGIN_EXPRESSION'
TOKEN_END_EXPRESSION = 'TOKEN_END_EXPRESSION'
TOKEN_OPERATOR_ADD = 'TOKEN_OPERATOR_ADD'
TOKEN_OPERATOR_MULTIPLY = 'TOKEN_OPERATOR_MULTIPLY'
TOKEN_PAREN_OPEN = 'TOKEN_PAREN_OPEN'
TOKEN_PAREN_CLOSE = 'TOKEN_PAREN_CLOSE'


def tokenize(string_expression, verbose=False):
    """
    Transforms a string representing an expression into a list of tokens.

    :param string_expression: string representing an expression.
    :param verbose: If True additional info will be printed.
    :return: List of tokens.
    """
    tokens = []

    string_expression = re.sub("([()*+])", r" \1 ", string_expression)
    string_expression = re.sub(" +", " ", string_expression)
    string_expression = re.sub("^ ", "", string_expression)
    string_expression = re.sub(" $", "", string_expression)

    if verbose:
        print(string_expression)

    tokens.append(TOKEN_BEGIN_EXPRESSION)

    for str_tok in string_expression.split(' '):
        if str_tok == '(':
            tokens.append(TOKEN_PAREN_OPEN)
        elif str_tok == ')':
            tokens.append(TOKEN_PAREN_CLOSE)
        elif str_tok == '+':
            tokens.append(TOKEN_OPERATOR_ADD)
        elif str_tok == '*':
            tokens.append(TOKEN_OPERATOR_MULTIPLY)
        else:
            if verbose:
                print(f'\t\t\t\t\t{str_tok}')
            tokens.append(int(str_tok))

    tokens.append(TOKEN_END_EXPRESSION)

    return tokens


def build_parameter(token_list, ix, fun_build_expression, verbose=False):
    """
    Builds a parameter of an expression. It can be a literal value or another complex expression.

    :param fun_build_expression: Function used to build expressions.
    :param token_list: List of tokens.
    :param ix: Index of token_list that marks the beginning of the parameter being built.
    :param verbose: If True additional info will be printed.
    :return: A parameter that can be evaluated.
    """

    ix, token = get_next_token(token_list, ix)

    if token == TOKEN_PAREN_OPEN:
        return fun_build_expression(token_list, ix, verbose)
    else:
        return ix, LiteralExpression(token)


def build_expression_v1(token_list, ix, verbose=False):
    """
    Builds an Expression from token_list beginning at index ix. Keeps adding and/or multiplying numbers until a close
    parenthesis or end expression tokens are found. Rules of part 1.

    :param token_list: List of tokens. Tokenized expression.
    :param ix: Index of token_list that marks the beginning of the expressing being built.
    :param verbose: If True additional info will be printed.
    :return: An Expression that can be evaluated.
    """

    # Parameter A
    if verbose:
        print(f'build_expression_v1. ix is {ix}')
    ix, expression = build_parameter(token_list, ix, build_expression_v1)

    while ix < len(token_list):

        ix, operator = get_next_token(token_list, ix)
        if operator == TOKEN_END_EXPRESSION or operator == TOKEN_PAREN_CLOSE:
            return ix, expression
        elif operator == TOKEN_OPERATOR_ADD:
            ix, exp_b = build_parameter(token_list, ix, build_expression_v1)
            expression = AdditionExpression(expression, exp_b)
        elif operator == TOKEN_OPERATOR_MULTIPLY:
            ix, exp_b = build_parameter(token_list, ix, build_expression_v1)
            expression = MultiplicationExpression(expression, exp_b)

    return ix, expression


def get_next_token(token_list, ix):
    """
    Gets the next token in the list.

    :param token_list: List of tokens.
    :param ix: Index of the next token.
    :return: Index of the next token, and the actual token.
    """
    token = token_list[ix]
    return ix + 1, token


def process_tokens(token_list, fun_build_expression, verbose=False):
    """
    Transforms an entire token list into an Expression.

    :param token_list: List of tokens.
    :param fun_build_expression: Functino to use to build expressions. Used in parts 1 and 2.
    :param verbose: If True additional info will be printed.
    :return: An expression that can be evaluated.
    """

    ix = 0
    expression = None
    while ix < len(token_list):
        ix, token = get_next_token(token_list, ix)
        if verbose:
            print(f'Token: {token}')

        if token == TOKEN_BEGIN_EXPRESSION:
            ix, expression = fun_build_expression(token_list, ix, verbose)
            if verbose:
                print(f'Returning from {fun_build_expression} ix is {ix} and expression is [{expression}]')
        else:
            raise Exception(f'process_tokens. Unexpected token {token}')

    return expression


def test_evaluate_expression(str_expression, fun_build_expression, expected, verbose=False):
    """
    Test function to test process_tokens.

    :param str_expression: String expression use case.
    :param fun_build_expression: Function used to build expressions.
    :param expected: Expected value of the built expression evaluation.
    :param verbose: If True additional info will be printed.
    """

    if verbose:
        print(f'Evaluating {str_expression}')
    test_expression = process_tokens(tokenize(str_expression), fun_build_expression, verbose)
    res = test_expression.evaluate()

    print(f'Expression [{str_expression}][{test_expression}] evaluation is: {res}.',
          'RIGHT' if res == expected else f'WRONG!! Expected {expected}!!')
    if verbose:
        print()


def sum_expressions(expressions, fun_build_expression):
    """
    Transforms a list of strings represeting expressions into Expressions. Then all of them are evaluated and their
    values summed up.

    :param expressions: List of string whose sum is to be calculated.
    :param fun_build_expression: Function used for build expressions.
    :return: Total value of all Expressions summed up.
    """

    total = 0

    for str_expression in expressions:
        total += process_tokens(tokenize(str_expression), fun_build_expression).evaluate()

    return total


# PART 2
def build_expression_v2(token_list, ix, verbose=False):
    """
    Builds an Expression from token_list beginning at index ix. Rules of part 2.

    :param token_list: List of tokens. Tokenized expression.
    :param ix: Index of token_list that marks the beginning of the expressing being built.
    :param verbose: If True additional info will be printed.
    :return: An Expression that can be evaluated.
    """

    # Parameter A
    if verbose:
        print(f'build_expression_v2 ix is {ix}')
    ix, expression = build_parameter(token_list, ix, build_expression_v2, verbose)

    while ix < len(token_list):

        ix, operator = get_next_token(token_list, ix)
        if operator == TOKEN_OPERATOR_ADD:
            ix, exp_b = build_parameter(token_list, ix, build_expression_v2, verbose)
            expression = AdditionExpression(expression, exp_b)
        elif operator == TOKEN_OPERATOR_MULTIPLY:
            ix, exp_b = build_expression_v2(token_list, ix, verbose)
            if verbose:
                print(f'\tBack from {build_expression_v2} ix is {ix} and exp_b is [{exp_b}]')

            expression = MultiplicationExpression(expression, exp_b)
            if verbose:
                print(f'\tExpression is: {expression}')
            return ix, expression
        elif operator == TOKEN_END_EXPRESSION or operator == TOKEN_PAREN_CLOSE:
            return ix, expression

    return ix, expression


if __name__ == '__main__':
    with open('data/aoc2020-input-day18.txt', 'r') as f:
        sol_expressions = [line.strip('\n') for line in f.readlines()]

    test_expression_1 = "1 + 2 * 3 + 4 * 5 + 6"
    test_expression_1b = "1 + (2 * 3) + (4 * (5 + 6))"
    test_expression_2 = "2 * 3 + (4 * 5)"
    test_expression_3 = "5 + (8 * 3 + 9 + 3 * 4 * 3)"
    test_expression_4 = "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))"
    test_expression_5 = "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2"

    test_simple_literal_expression = "3"
    test_simple_addition_expression = "2 + 3"
    test_simple_additions = "1 + 3 + 10"
    test_simple_multiplication_expression = "4 * 5"
    test_simple_multi_add_expression = "2 * 3 + 7"

    print('PART 1')
    # TEST PART 1
    test_tokens_1 = tokenize(test_expression_5)

    expected_tokens = [TOKEN_BEGIN_EXPRESSION, TOKEN_PAREN_OPEN, TOKEN_PAREN_OPEN, 2, TOKEN_OPERATOR_ADD, 4,
                       TOKEN_OPERATOR_MULTIPLY, 9, TOKEN_PAREN_CLOSE, TOKEN_OPERATOR_MULTIPLY, TOKEN_PAREN_OPEN, 6,
                       TOKEN_OPERATOR_ADD, 9, TOKEN_OPERATOR_MULTIPLY, 8, TOKEN_OPERATOR_ADD, 6, TOKEN_PAREN_CLOSE,
                       TOKEN_OPERATOR_ADD, 6, TOKEN_PAREN_CLOSE, TOKEN_OPERATOR_ADD, 2, TOKEN_OPERATOR_ADD, 4,
                       TOKEN_OPERATOR_MULTIPLY, 2, TOKEN_END_EXPRESSION]

    print('Testing tokenize',
          'RIGHT' if test_tokens_1 == expected_tokens
          else f'WRONG!! Expected {expected_tokens} but was {test_tokens_1}')

    test_evaluate_expression(test_simple_literal_expression, build_expression_v1, 3)
    test_evaluate_expression("(3)", build_expression_v1, 3)
    test_evaluate_expression("(((((3)))))", build_expression_v1, 3)
    test_evaluate_expression(test_simple_addition_expression, build_expression_v1, 5)
    test_evaluate_expression(test_simple_additions, build_expression_v1, 14)
    test_evaluate_expression(test_simple_multiplication_expression, build_expression_v1, 20)
    test_evaluate_expression(test_simple_multi_add_expression, build_expression_v1, 13)

    test_evaluate_expression(test_expression_1, build_expression_v1, 71)
    test_evaluate_expression(test_expression_1b, build_expression_v1, 51)
    test_evaluate_expression(test_expression_2, build_expression_v1, 26)
    test_evaluate_expression(test_expression_3, build_expression_v1, 437)
    test_evaluate_expression(test_expression_4, build_expression_v1, 12240)
    test_evaluate_expression(test_expression_5, build_expression_v1, 13632)

    expected_addition = 25872
    result = sum_expressions([test_expression_4, test_expression_5], build_expression_v1)
    print('Testing sum_expressions',
          'RIGHT' if expected_addition == result else f'WRONG!! Expected {expected_addition} but was {result}')

    # SOLVING PART 1
    print('SOLUTION PART 1', sum_expressions(sol_expressions, build_expression_v1))
    print()

    print('PART 2')
    # TEST PART 2
    test_evaluate_expression(test_simple_literal_expression, build_expression_v2, 3)
    test_evaluate_expression("(3)", build_expression_v2, 3)
    test_evaluate_expression("(((((3)))))", build_expression_v2, 3)
    test_evaluate_expression(test_simple_addition_expression, build_expression_v2, 5)
    test_evaluate_expression(test_simple_additions, build_expression_v2, 14)
    test_evaluate_expression(test_simple_multiplication_expression, build_expression_v2, 20)
    test_evaluate_expression(test_simple_multi_add_expression, build_expression_v2, 20)

    test_evaluate_expression(test_expression_1, build_expression_v2, 231)
    test_evaluate_expression(test_expression_1b, build_expression_v2, 51)
    test_evaluate_expression(test_expression_2, build_expression_v2, 46)
    test_evaluate_expression(test_expression_3, build_expression_v2, 1445)
    test_evaluate_expression(test_expression_4, build_expression_v2, 669060)
    test_evaluate_expression(test_expression_5, build_expression_v2, 23340)

    # SOLVING PART 2
    print('SOLUTION PART 2', sum_expressions(sol_expressions, build_expression_v2))
