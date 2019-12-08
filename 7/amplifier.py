from itertools import permutations
from intcode import IntCodeRuntime, IntCodeStatus, get_program_input


def solve_part_1(puzzle_input):
    amplifier_configurations = permutations(range(5))

    highest_signal = 0
    best_configuration = None
    for configuration in amplifier_configurations:
        print(configuration)
        signal = 0
        for amp_i in range(5):
            amp_config = configuration[amp_i]
            program = puzzle_input[:]

            runtime = IntCodeRuntime()
            runtime.set_program(program)
            runtime.input_number(amp_config)
            runtime.input_number(signal)
            runtime.run()
            signal = runtime.get_output()[0]

        if signal > highest_signal:
            highest_signal = signal
            best_configuration = configuration

    return highest_signal

def solve_part_2(puzzle_input):
    return ""

if __name__ == "__main__":
    puzzle_input = get_program_input("input.txt")

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")