import sys
import os
from intcode import IntCodeRuntime, IntCodeStatus, get_program_input

def solve_part_1(puzzle_input, system_id):
    runtime = IntCodeRuntime()
    runtime.set_program(puzzle_input)
    runtime.input_number(system_id)
    runtime.run()
    for line in runtime.get_output():
        print(line)


if __name__ == "__main__":
    puzzle_input = get_program_input("input.txt")

    system_id = int(input("Enter `1` for Part 1, or `5` for Part 2: "))
    solve_part_1(puzzle_input, system_id)