from collections import defaultdict
import math

FUEL = "FUEL"
ORE = "ORE"
TRILLION = 1000000000000

class ReactionPart:
    def __init__(self, chemical, amount):
        self.chemical = chemical
        self.amount = amount

    def __str__(self):
        return f"ReactionPart({self.chemical}, {self.amount})"

    def __repr__(self):
        return f"ReactionPart({self.chemical}, {self.amount})"

class Reaction:
    def __init__(self, output, ingredients):
        self.output = output
        self.ingredients = ingredients

    def __str__(self):
        return f"<Reaction for {self.output.amount} {self.output.chemical}>"

    def __repr__(self):
        return f"<Reaction for {self.output.amount} {self.output.chemical}>"

def create_reaction_part(part_string):
    split = part_string.strip().split(" ")
    return ReactionPart(split[1], int(split[0]))

def generate_reaction_precedence(reactions, reaction_index):
    # Not hyper performant, but there's not a ton of data anyway
    reaction_precidence = []
    reactions_to_resolve = [reaction_index[FUEL]]

    while len(reactions_to_resolve) > 0:
        current_reaction = reactions_to_resolve.pop(0)
        reaction_precidence.append(current_reaction)
        for part in current_reaction.ingredients:
            if part.chemical == ORE:
                continue

            upstream_reaction = reaction_index[part.chemical]
            if upstream_reaction in reaction_precidence:
                reaction_precidence.remove(upstream_reaction)
            if upstream_reaction not in reactions_to_resolve:
                reactions_to_resolve.append(upstream_reaction)

    return reaction_precidence

def ore_needed_for_fuel(reaction_precidence, fuel_amount):
    need = defaultdict(int)
    need[FUEL] = fuel_amount
    seen = set()
    for reaction in reaction_precidence:
        chemical = reaction.output.chemical
        if chemical == ORE:
            break

        assert chemical not in seen # Precidence thing should be ensuring this
        seen.add(chemical)

        multiple = math.ceil(need[chemical] / reaction.output.amount)
        for part in reaction.ingredients:
            need[part.chemical] += part.amount * multiple

    return need[ORE]


def solve_part_1(puzzle_input):
    reaction_index = {reaction.output.chemical:reaction for reaction in puzzle_input}

    reaction_precidence = generate_reaction_precedence(puzzle_input, reaction_index)

    return ore_needed_for_fuel(reaction_precidence, 1)

def solve_part_2(puzzle_input):
    reaction_index = {reaction.output.chemical:reaction for reaction in puzzle_input}
    reaction_precidence = generate_reaction_precedence(puzzle_input, reaction_index)

    single_fuel_cost = ore_needed_for_fuel(reaction_precidence, 1)

    too_high = int(TRILLION / single_fuel_cost * 10)
    lower_bound = int(TRILLION / single_fuel_cost)

    while too_high - lower_bound > 1:
        bisect = (too_high + lower_bound) // 2
        #print(f"{bisect} ({too_high - bisect})")
        fuel_cost = ore_needed_for_fuel(reaction_precidence, bisect)
        if fuel_cost > TRILLION:
            too_high = bisect
        else:
            lower_bound = bisect

    return lower_bound


def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            io = line.split("=>")
            output = create_reaction_part(io[1])
            inputs = list(map(create_reaction_part, io[0].split(",")))
            puzzle_input.append(Reaction(output,inputs))
    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")