# Day 21: Allergen Assessment
import re
from collections import defaultdict


# PART 1
def parse_menu(raw_menu):
    """
    Parses a list of string representing a list of dishes.

    :param raw_menu: list of string representing a menu.
    :return: List of dishes as tuple (x, y) being x a list of ingredients of the dish and y a list of allergens.
    """
    ingredients_pattern = r'^.*(?= \(contains)'
    allergen_pattern = r'\(contains (.*)\)'

    dishes = []

    for food in raw_menu:
        clean_food = re.sub(',', '', food)
        ingredients = re.findall(ingredients_pattern, clean_food)[0].split(' ')
        allergens = re.findall(allergen_pattern, clean_food)[0].split(' ')
        dishes.append((ingredients, allergens))

    return dishes


def classify_allergens(dishes):
    """
    Given a list of dishes, counts how many times each allergen and ingredient is present in the dishes.

    :param dishes: List of dishes to be classified.
    :return: how many times each ingredient appears per allergen, and how many times each allergen appears.
    """
    cnt_allergens = defaultdict(int)
    ingredients_per_allergen = {}

    for dish in dishes:
        ingredients, allergens = dish
        # counting allergens
        for allergen in allergens:
            cnt_allergens[allergen] += 1

        # counting ingredients per allergen
        for ingredient in ingredients:
            for allergen in allergens:
                if allergen not in ingredients_per_allergen:
                    ingredients_per_allergen[allergen] = defaultdict(int)
                ingredients_per_allergen[allergen][ingredient] += 1

    return ingredients_per_allergen, cnt_allergens


def detect_safe_ingredients(classified_ingredients, cnt_allergens, verbose=False):
    """
    Determines the allergens of each ingredient. Separates the allergen ingredients of the ones which are not.

    :param classified_ingredients: List of occurrences of all ingredients, per allergen.
    :param cnt_allergens: How many times each allergen is on the menu.
    :param verbose: If True additional info will be printed.
    :return: List of safe ingredients and which allergen has each ingredient.
    """
    definitive_assignments = {}

    while True:
        something_changed = False
        for allergen, ingredient_list in classified_ingredients.items():
            this_allergen = cnt_allergens[allergen]
            if verbose:
                print(f'allergen {allergen} is present in {this_allergen} dishes')
            ing_candidates = [ing_name
                              for ing_name, ing_cnt
                              in ingredient_list.items()
                              if ing_cnt == this_allergen and ing_name not in definitive_assignments]
            if verbose:
                print(f'candidates for {allergen} are {ing_candidates}!')
            if len(ing_candidates) == 1:
                something_changed = True
                the_ingredient = ing_candidates[0]
                if verbose:
                    print(f'Assigning {the_ingredient} the allergen {allergen}!')
                definitive_assignments[the_ingredient] = allergen

        if not something_changed:
            break

    safe_ingredients = {ing_name
                        for ings in classified_ingredients.values()
                        for ing_name in ings.keys()
                        if ing_name not in definitive_assignments}

    unassigned_allergens = [allergen
                            for allergen in classified_ingredients.keys()
                            if allergen not in definitive_assignments.values()]

    if len(unassigned_allergens) > 0:
        print(f'There are still some allergens unassigned!!', unassigned_allergens)

    return safe_ingredients, definitive_assignments


def count_ingredients_occurrences(all_dishes, ingredients_to_count):
    """
    Counts how many times ingredients of a list appear across all dishes.

    :param all_dishes: All the dishes.
    :param ingredients_to_count: Ingredients to count.
    :return: Total occurrences.
    """

    total = 0
    for ingredients, _ in all_dishes:
        for ingredient in ingredients:
            if ingredient in ingredients_to_count:
                total += 1

    return total


# PART 2
def create_canonical_dangerous_ingredient_list(assignments):
    """
    Given all allergen assigned to the ingredients, calculates the canonical dangerous ingredient list.
    :param assignments: Allergens assigned to ingredients.
    :return: the canonical dangerous ingredient list.
    """
    inverse_assignments = {v: k for k, v in assignments.items()}
    allergens = [k for k in inverse_assignments.keys()]
    allergens.sort()

    ingredients_list = [inverse_assignments[allergen] for allergen in allergens]

    return ','.join(ingredients_list)


if __name__ == '__main__':
    with open('data/aoc2020-input-day21.txt', 'r') as f:
        sol_raw_dishes = [line.strip('\n') for line in f.readlines()]

    test_raw_menu_1 = ['mxmxvkd kfcds sqjhc nhms (contains dairy, fish)',
                       'trh fvjkl sbzzf mxmxvkd (contains dairy)',
                       'sqjhc fvjkl (contains soy)',
                       'sqjhc mxmxvkd sbzzf (contains fish)']

    print('PART 1')
    # TEST PART 1
    test_dishes = parse_menu(test_raw_menu_1)
    test_dish = test_dishes[0]
    expected_ingredients = ['mxmxvkd', 'kfcds', 'sqjhc', 'nhms']
    expected_allergens = ['dairy', 'fish']
    print('Testing parse_menu, n_dishes',
          'RIGHT' if len(test_dishes) == 4 else f'WRONG!! Expected 4 but was {len(test_dishes)}')
    print('Testing parse_menu, ingredients',
          'RIGHT' if test_dish[0] == expected_ingredients
          else f'WRONG!! Expected {expected_ingredients} but was {test_dish[0]}')
    print('Testing parse_menu, allergens',
          'RIGHT' if test_dish[1] == expected_allergens
          else f'WRONG!! Expected {expected_allergens} but was {test_dish[1]}')

    test_classified_ingredients, test_cnt_allergens = classify_allergens(test_dishes)
    print('Testing classify_allergens, dairy',
          'RIGHT' if test_cnt_allergens['dairy'] == 2 else f'WRONG!! Expected 2 but was {test_cnt_allergens["dairy"]}')
    print('Testing classify_allergens, fish',
          'RIGHT' if test_cnt_allergens['fish'] == 2 else f'WRONG!! Expected 2 but was {test_cnt_allergens["fish"]}')
    print('Testing classify_allergens, soy',
          'RIGHT' if test_cnt_allergens['soy'] == 1 else f'WRONG!! Expected 1 but was {test_cnt_allergens["soy"]}')

    test_safe_ingredients, test_definitive_al = detect_safe_ingredients(test_classified_ingredients, test_cnt_allergens)
    expected_safe_ingredients = {'nhms', 'sbzzf', 'trh', 'kfcds'}
    expected_assignments = {'mxmxvkd': 'dairy', 'sqjhc': 'fish', 'fvjkl': 'soy'}
    print('Testing detect_safe_ingredients, safe',
          'RIGHT' if test_safe_ingredients == expected_safe_ingredients
          else f'WRONG!! Expected {expected_safe_ingredients} but was {test_safe_ingredients}')
    print('Testing detect_safe_ingredients, assignments',
          'RIGHT' if test_definitive_al == expected_assignments
          else f'WRONG!! Expected {expected_assignments} but was {test_definitive_al}')

    foo = count_ingredients_occurrences(test_dishes, test_safe_ingredients)
    print('Testing count_ingredients_occurrences', 'RIGHT' if foo == 5 else f'WRONG!! Expected 5 but was {foo}')

    # SOLVE PART 1
    sol_dishes = parse_menu(sol_raw_dishes)
    sol_classified_ingredients, sol_cnt_allergens = classify_allergens(sol_dishes)
    sol_safe_ingredients, sol_definitive_al = detect_safe_ingredients(sol_classified_ingredients, sol_cnt_allergens)
    foo = count_ingredients_occurrences(sol_dishes, sol_safe_ingredients)

    print('SOLUTION PART 1:', foo)
    print()

    print('PART 2')
    # TEST PART 2
    expected_cdi = 'mxmxvkd,sqjhc,fvjkl'
    test_cdi = create_canonical_dangerous_ingredient_list(test_definitive_al)
    print('Testing create_canonical_dangerous_ingredient_list',
          'RIGHT' if test_cdi == expected_cdi else f'WRONG!! Expected {expected_cdi} but was {test_cdi}')

    # SOLVE PART 2
    print('SOLUTION PART 2:', create_canonical_dangerous_ingredient_list(sol_definitive_al))
