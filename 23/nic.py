from intcode import IntCodeRuntime, IntCodeStatus, get_program_input
from typing import List

def solve_part_1(puzzle_input):
    nics : List[IntCodeRuntime] = []
    for i in range(50):
        runtime = IntCodeRuntime()
        runtime.set_program(puzzle_input[:])
        runtime.run()
        runtime.input_number(i)
        runtime.run()
        nics.append(runtime)

    final_output = None
    while final_output is None:
        for nic in nics:
            if len(nic._input) == 0:
                nic.input_number(-1)
            nic.run()
            output = nic.get_output()
            for p in range(0, len(output), 3):
                address, x, y = output[p:p+3]

                if address == 255:
                    final_output = y
                elif address < 50:
                    nics[address].input_number(x)
                    nics[address].input_number(y)
                else:
                    raise Exception(f"Invalid address {address}")

    return final_output

def solve_part_2(puzzle_input):
    nics : List[IntCodeRuntime] = []
    for i in range(50):
        runtime = IntCodeRuntime()
        runtime.set_program(puzzle_input[:])
        runtime.run()
        runtime.input_number(i)
        runtime.run()
        nics.append(runtime)

    nat_x = None
    nat_y = None
    last_restart_y = None
    final_output = None
    while final_output is None:
        idle = True

        for nic in nics:
            if len(nic._input) == 0:
                nic.input_number(-1)
            else:
                idle = False
            nic.run()
            output = nic.get_output()
            for p in range(0, len(output), 3):
                idle = False
                address, x, y = output[p:p+3]

                if address == 255:
                    nat_x = x
                    nat_y = y
                elif address < 50:
                    nics[address].input_number(x)
                    nics[address].input_number(y)
                else:
                    raise Exception(f"Invalid address {address}")

        if idle is True:
            if nat_y == last_restart_y:
                final_output = nat_y
            nics[0].input_number(nat_x)
            nics[0].input_number(nat_y)
            last_restart_y = nat_y

    return final_output

if __name__ == "__main__":
    puzzle_input = get_program_input("input.txt")

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")