import string
def parse_instruction(instruction:int):
    digits = str(instruction).zfill(5)
    mode3 = int(digits[0])
    mode2 = int(digits[1])
    mode1 = int(digits[2])
    opcode = int(digits[3:])
    return opcode, mode1, mode2, mode3

def get_param(program, pc, param_number, mode):
    param = program[pc + param_number]
    if mode == 0:
        param = program[param]
    return param

def run_program(program, debug=False):
    p = program
    halt = False
    pc = 0
    while halt == False:
        instruction = p[pc]
        opcode, mode1, mode2, mode3 = parse_instruction(instruction)

        # Addition
        if opcode == 1:
            param1 = get_param(p, pc, 1, mode1)
            param2 = get_param(p, pc, 2, mode2)
            assert mode3 == 0
            if debug:
                print(f"{p[pc:pc+4]}: p[{p[pc+3]}] = {param1} + {param2}")
            p[p[pc+3]] = param1 + param2
            pc += 4

        # Multiplication
        elif opcode == 2:
            param1 = get_param(p, pc, 1, mode1)
            param2 = get_param(p, pc, 2, mode2)
            assert mode3 == 0
            if debug:
                print(f"{p[pc:pc+4]}: p[{p[pc+3]}] = {param1} * {param2}")
            p[p[pc+3]] = param1 * param2
            pc += 4

        # Input
        elif opcode == 3:
            assert mode1 == 0
            user_input = int(input("Please Input Number: "))
            p[p[pc+1]] = user_input
            if debug:
                print(f"{p[pc:pc+2]}: p[{p[pc+1]}] = {user_input}")
            pc += 2

        # Output
        elif opcode == 4:
            param1 = get_param(p, pc, 1, mode1)
            if debug:
                print(f"{p[pc:pc+2]}: {param1} (p[{pc + 1}])")
            else:
                print(f"{param1}")
            pc += 2

        elif opcode == 5:
            param1 = get_param(p, pc, 1, mode1)
            param2 = get_param(p, pc, 2, mode2)
            if param1 != 0:
                if debug:
                    print(f"{p[pc:pc+4]}: TODO")
                pc = param2
            else:
                if debug:
                    print(f"{p[pc:pc+4]}: TODO")
                pc += 3

        elif opcode == 6:
            param1 = get_param(p, pc, 1, mode1)
            param2 = get_param(p, pc, 2, mode2)
            if param1 == 0:
                if debug:
                    print(f"{p[pc:pc+4]}: TODO")
                pc = param2
            else:
                if debug:
                    print(f"{p[pc:pc+4]}: TODO")
                pc += 3

        elif opcode == 7:
            param1 = get_param(p, pc, 1, mode1)
            param2 = get_param(p, pc, 2, mode2)
            assert mode3 == 0
            if debug:
                print(f"{p[pc:pc+4]}: p[{p[pc+3]}] = {param1} < {param2}")
            p[p[pc+3]] = int(param1 < param2)
            pc += 4

        elif opcode == 8:
            param1 = get_param(p, pc, 1, mode1)
            param2 = get_param(p, pc, 2, mode2)
            assert mode3 == 0
            if debug:
                print(f"{p[pc:pc+4]}: p[{p[pc+3]}] = {param1} == {param2}")
            p[p[pc+3]] = int(param1 == param2)
            pc += 4

        # Halt
        elif opcode == 99:
            halt = True

        else:
            raise Exception(f"Something went wrong at {pc}, value {instruction}")

    return p[0]

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


def get_program_input(filename):
    puzzle_input = []
    with open(filename) as input_txt:
        for line in input_txt:
            puzzle_input = list(map(int, line.split(",")))

    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_program_input("input.txt")

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")