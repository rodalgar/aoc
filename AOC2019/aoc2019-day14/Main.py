import re
from collections import defaultdict


class QuantMaterial():
    quantity = None
    material = None

    def __init__(self, quantity, material):
        self.quantity = quantity
        self.material = material

    def __repr__(self):
        return f'[{self.quantity} {self.material}]'

    def parse(rawMaterial):
        result = re.search('([0-9]+) ([A-Z]+)', rawMaterial)

        return QuantMaterial(int(result.groups()[0]), result.groups()[1])


class Reaction():
    requirements = None
    produces = None

    def __init__(self, requirements, produces):
        self.requirements = requirements
        self.produces = produces

    def __repr__(self):
        return f'[{self.requirements}] => [{self.produces}]\n'

    def parse(rawReaction):
        rawMaterials = re.findall('([0-9]+ [A-Z]+)', rawReaction)
        num_materials = len(rawMaterials)

        # Assuming that each reaction produces ONLY ONE element. So, last rawmaterial should be what is produced.

        rawrequirements = rawMaterials[0:num_materials-1]
        rawproduces = rawMaterials[num_materials-1]

        requirements = [QuantMaterial.parse(rr) for rr in rawrequirements]
        produces = QuantMaterial.parse(rawproduces)

        return Reaction(requirements, produces)


class Grimoire():
    reactions = None

    def __init__(self):
        self.reactions = {}

    def loadReactions(self, rawReactions):
        reactions = [Reaction.parse(rawReaction) for rawReaction in rawReactions.split('\n')]

        for r in reactions:
            assert r.produces.material not in self.reactions, \
                    f'There is already one reaction for material {r.produces.material}!!'
            self.reactions[r.produces.material] = r

        if 'ORE' not in self.reactions:
            self.reactions['ORE'] = Reaction([], QuantMaterial(1, 'ORE'))

    def getReaction(self, formaterial):
        reaction = self.reactions.get(formaterial)
        if reaction is None:
            raise Exception(f'No reaction for {formaterial} found!!!')
        return reaction

    def calculateOre(self, formaterial=QuantMaterial(1, 'FUEL'), verbose=False, surplus=None):
        elements_needed = defaultdict(int)

        if surplus is None:
            elements_surplus = {}
            for reaction in self.reactions:
                elements_surplus[reaction] = 0
        else:
            elements_surplus = surplus

        elements_needed[formaterial.material] = formaterial.quantity
        elements_surplus[formaterial.material] = 0

        while not (len(elements_needed) == 1 and [k for k in elements_needed.keys()][0] == 'ORE'):
            if verbose:
                print(50*'-')
            tmp_elements = defaultdict(int)
            for element in elements_needed:
                if elements_needed[element] != 0:
                    reaction = self.getReaction(element)
                    if reaction.produces.material == 'ORE':
                        if verbose:
                            print('ORE is not produced.')
                        tmp_elements['ORE'] += elements_needed['ORE']
                        continue

                    if verbose:
                        print(f'I need to make {elements_needed[element]} units of {element}. I already had {elements_surplus[element]} units.')

                    if elements_surplus[element] >= elements_needed[element]:
                        if verbose:
                            print(f'I have enough surplus to meet the needs. Surplus left: {elements_surplus[element] - elements_needed[element]}')
                        elements_surplus[element] -= elements_needed[element]
                    else:
                        if verbose:
                            print(f'With {elements_surplus[element]} units of surplus, I still need {elements_needed[element] - elements_surplus[element]} units of {element}.')
                        needed = elements_needed[element] - elements_surplus[element]
                        elements_surplus[element] = 0

                        q = reaction.produces.quantity
                        number_of_needed_reactions = (needed // q) + 1
                        if needed % q == 0:
                            number_of_needed_reactions -= 1
                        if verbose:
                            print(f'The reaction is {reaction}. As I need {needed} units of {element}, I need to produce it {number_of_needed_reactions} times.')
                        for r in reaction.requirements:
                            req_mat = r.material
                            req_qty = r.quantity
                            tmp_elements[req_mat] += req_qty * number_of_needed_reactions

                        produced = q * number_of_needed_reactions
                        if verbose:
                            print(f'So, {produced} units of {element} has been produced.. as I needed {needed} units it has been generated a surplus of {produced - needed} units.')
                        elements_surplus[element] += produced - needed

            if verbose:
                print('elements_needed', elements_needed)
                print('tmp_elements', tmp_elements)
                print('elements_surplus', elements_surplus)
            elements_needed = tmp_elements

        coste = elements_needed['ORE']

        return coste, elements_surplus


############
# PART 1
############
# TESTS
def execute_test_part1(idtest, reactions, expected):
    testlabel = idtest.upper()
    print(f'\n{testlabel}')

    grim = Grimoire()
    grim.loadReactions(reactions)

    print(grim.reactions)

    actual, _ = grim.calculateOre()
    assert expected == actual, f'{testlabel} Failed! expected {expected}, actual {actual}'
    print(f'{testlabel} passed! expected {expected}, actual {actual}')


# TEST 1
reactionsT1 = '10 ORE => 10 A\n\
1 ORE => 1 B\n\
7 A, 1 B => 1 C\n\
7 A, 1 C => 1 D\n\
7 A, 1 D => 1 E\n\
7 A, 1 E => 1 FUEL'

execute_test_part1('TEST 1', reactionsT1, 31)

# TEST 2
reactionsT2 = '9 ORE => 2 A\n\
8 ORE => 3 B\n\
7 ORE => 5 C\n\
3 A, 4 B => 1 AB\n\
5 B, 7 C => 1 BC\n\
4 C, 1 A => 1 CA\n\
2 AB, 3 BC, 4 CA => 1 FUEL'

execute_test_part1('TEST 2', reactionsT2, 165)

# TEST 3
reactionsT3 = '157 ORE => 5 NZVS\n\
165 ORE => 6 DCFZ\n\
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL\n\
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ\n\
179 ORE => 7 PSHF\n\
177 ORE => 5 HKGWZ\n\
7 DCFZ, 7 PSHF => 2 XJWVT\n\
165 ORE => 2 GPVTF\n\
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT'

execute_test_part1('TEST 3', reactionsT3, 13312)


# TEST 4
reactionsT4 = '2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG\n\
17 NVRVD, 3 JNWZP => 8 VPVL\n\
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL\n\
22 VJHF, 37 MNCFX => 5 FWMGM\n\
139 ORE => 4 NVRVD\n\
144 ORE => 7 JNWZP\n\
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC\n\
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV\n\
145 ORE => 6 MNCFX\n\
1 NVRVD => 8 CXFTF\n\
1 VJHF, 6 MNCFX => 4 RFSQX\n\
176 ORE => 6 VJHF'

execute_test_part1('TEST 4', reactionsT4, 180697)

# TEST 5
reactionsT5 = '171 ORE => 8 CNZTR\n\
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL\n\
114 ORE => 4 BHXH\n\
14 VRPVC => 6 BMBT\n\
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL\n\
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT\n\
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW\n\
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW\n\
5 BMBT => 4 WPTQ\n\
189 ORE => 9 KTJDG\n\
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP\n\
12 VRPVC, 27 CNZTR => 2 XDBXC\n\
15 KTJDG, 12 BHXH => 5 XCVML\n\
3 BHXH, 2 VRPVC => 7 MZWV\n\
121 ORE => 7 VRPVC\n\
7 XCVML => 6 RJRHP\n\
5 BHXH, 4 VRPVC => 5 LTCX'

execute_test_part1('TEST 5', reactionsT5, 2210736)

# SOLUTION
print('SOLUTION PART 1')
input_14 = r'data\aoc2019-input-day14.txt'
with open(input_14) as f:
    data14 = f.read()

grim = Grimoire()
grim.loadReactions(data14)

print(grim.reactions)

actual = grim.calculateOre()

print(actual)

#>>>SOLUTION: 365768

############
# PART 2
############
# TESTS
def perform_test_p2(reactions):
    grim = Grimoire()

    grim.loadReactions(reactions)
    print(grim.reactions)

    totalORE = 1000000000000
    ore_per_fuel, _ = grim.calculateOre(QuantMaterial(1, 'FUEL'), verbose=False)
    print('ore_per_fuel', ore_per_fuel)
    theoric_fuel = totalORE // ore_per_fuel

    total_used_ore, surplus = grim.calculateOre(QuantMaterial(theoric_fuel, 'FUEL'), verbose=False)
    maxFUEL = theoric_fuel
    while True:
        # print(f'Calculating ore to produce {maxFUEL} FUEL')
        used_ore, surplus = grim.calculateOre(QuantMaterial(1, 'FUEL'), surplus=surplus, verbose=False)
        # print(f'{used_ore} required to produce {maxFUEL} FUEL')
        if total_used_ore + used_ore <= totalORE:
            maxFUEL += 1
            total_used_ore += used_ore
        else:
            break
        if maxFUEL % 10000 == 0:
            print(f'Used {total_used_ore} ORE ({(total_used_ore / totalORE) * 100}%) to produce {maxFUEL} FUEL')
    return maxFUEL, total_used_ore

def execute_test_part2(idtest, reactions, expected):
    testlabel = idtest.upper()
    print(f'\n{testlabel}')

    maxFUEL, total_used_ore = perform_test_p2(reactions)

    print(maxFUEL)
    print(total_used_ore)

    assert expected == maxFUEL, f'{testlabel} Failed! expected {expected}, actual {actual}'
    print(f'{testlabel} passed! expected {expected}, actual {actual}')


# TEST 1
execute_test_part2('TEST 1', reactionsT3, 82892753)

# TEST 2
execute_test_part2('TEST 2', reactionsT4, 5586022)

# TEST 3
execute_test_part2('TEST 3', reactionsT5, 460664)

# SOLUTION
maxFUEL, _ = perform_test_p2(data14)
print(maxFUEL)

#>>>SOLUTION: 3756877