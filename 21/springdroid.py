from intcode import get_program_input, IntCodeRuntime, IntCodeStatus

def solve_part_1(puzzle_input):
    instructions = [
        "NOT A T",
        "OR T J",
        "NOT B T",
        "OR T J",
        "NOT C T",
        "OR T J",
        "AND D J",
    ]

    runtime = IntCodeRuntime()
    runtime.set_program(puzzle_input)
    runtime.run()
    print(runtime.get_ascii_output())
    runtime.input_ascii("\n".join(instructions))
    runtime.input_ascii("\nWALK\n")
    runtime.run()

    output = runtime.get_output()
    for num in output:
        try:
            print(chr(num), end="")
        except:
            return num
    return ""

def solve_part_2(puzzle_input):
    # 
    instructions = [
        "NOT A T",
        "OR T J",
        "NOT B T",
        "OR T J",
        "NOT C T",
        "OR T J",
        "AND D J",
        "NOT E T",
        "NOT T T",
        "OR H T",
        "AND T J",
    ]

    runtime = IntCodeRuntime()
    runtime.set_program(puzzle_input)
    runtime.run()
    print(runtime.get_ascii_output())
    runtime.input_ascii("\n".join(instructions))
    runtime.input_ascii("\nRUN\n")
    runtime.run()

    output = runtime.get_output()
    for num in output:
        try:
            print(chr(num), end="")
        except:
            return num
    return ""

if __name__ == "__main__":
    puzzle_input = get_program_input("input.txt")

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")