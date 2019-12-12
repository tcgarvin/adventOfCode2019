from intcode import IntCodeRuntime, get_program_input

def solve_part_1(puzzle_input):
    runtime = IntCodeRuntime()
    runtime.set_program(puzzle_input)
    runtime.input_number(1)
    runtime.run()
    return "\n" + "\n".join(map(str, runtime.get_output()))

def solve_part_2(puzzle_input):
    return ""

if __name__ == "__main__":
    puzzle_input = get_program_input("input.txt")

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")