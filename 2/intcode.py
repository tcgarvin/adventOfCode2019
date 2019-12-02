def run_program(program):
    p = program
    for pc in range(0, len(p), 4):
        opcode = p[pc]
        if opcode == 1:
            p[p[pc+3]] = p[p[pc+1]] + p[p[pc+2]]
        elif opcode == 2:
            p[p[pc+3]] = p[p[pc+1]] * p[p[pc+2]]
        elif opcode == 99:
            return p[0]
        else:
            raise Exception(f"Something went wrong at {pc}, value {opcode}")

    raise Exception("Reached EOF without 99")

def solve_part_1(program):
    p = program[:]
    p[1] = 12
    p[2] = 2
    return run_program(p)

PART_2_EXPECTED_OUTPUT = 19690720
def solve_part_2(puzzle_input):
    output = 0
    for i in range(100):
        for j in range(100):
            program = puzzle_input[:]
            program[1] = i
            program[2] = j
            output = run_program(program)
            if output == PART_2_EXPECTED_OUTPUT:
                return 100 * i + j

    raise Exception(f"No pair of values resulted in {PART_2_EXPECTED_OUTPUT}")


def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            puzzle_input = list(map(int, line.split(",")))

    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")