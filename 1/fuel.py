from functools import reduce

def solve_part_1(module_weights):
    total = 0
    for weight in puzzle_input:
        total += weight // 3 - 2

    return total

def solve_part_2(puzzle_input):
    total = 0
    for weight in puzzle_input:
        fuel_requirement = weight // 3 - 2

        while fuel_requirement > 0:
            total += fuel_requirement
            fuel_requirement = fuel_requirement // 3 - 2

    return total

def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            puzzle_input.append(int(line))
    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")
