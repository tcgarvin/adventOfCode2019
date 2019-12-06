import sys
import os
from intcode import get_program_input, run_program

def solve_part_1(puzzle_input):
    return run_program(puzzle_input)

def solve_part_2(puzzle_input):
    return ""

if __name__ == "__main__":
    puzzle_input = get_program_input("input.txt")

    print("Enter `1` for Part 1, or `5` for Part 2.")
    solve_part_1(puzzle_input)