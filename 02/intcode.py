from collections import deque
from enum import Enum

from defaultlist import defaultlist  # I am a terrible person

class IntCodeStatus(Enum):
    RUNNABLE = 0
    IOBLOCK = 1
    HALTED = 2
    UNINITIALIZED = 3

def parse_instruction(instruction:int):
    digits = str(instruction).zfill(5)
    mode3 = int(digits[0])
    mode2 = int(digits[1])
    mode1 = int(digits[2])
    opcode = int(digits[3:])
    return opcode, mode1, mode2, mode3

class IntCodeRuntime:
    def __init__(self):
        self._program = defaultlist(lambda: 0)
        self._program[0] = 99
        self._status = IntCodeStatus.UNINITIALIZED
        self._input = deque()
        self._output_buffer = list()
        self._program_counter = 0
        self._relative_base_offset = 0

    def set_program(self, program):
        assert self._program[0] == 99
        self._program = defaultlist(lambda: 0)
        self._program.extend(program)
        self._program_counter = 0
        self._status = IntCodeStatus.RUNNABLE

    def get_exit_code(self):
        assert self._status == IntCodeStatus.HALTED
        return self._program[0]

    def get_status(self):
        return self._status

    def get_output(self):
        result = self._output_buffer[:]
        self._output_buffer.clear()
        return result

    def get_param_address(self, param_number, mode):
        address = self._program_counter + param_number
        if mode == 0:
            address = self._program[address]
        elif mode == 2:
            address = self._relative_base_offset + self._program[address]
        return address

    def input_number(self, number):
        self._input.appendleft(number)

    def run(self, debug=False):
        p = self._program

        # If not runnable, see if we can become runnable
        if self._status == IntCodeStatus.HALTED:
            return
        elif self._status == IntCodeStatus.UNINITIALIZED:
            raise Exception("Cannot run uninitialized program")
        elif self._status == IntCodeStatus.IOBLOCK:
            if len(self._input) > 0:
                self._status = IntCodeStatus.RUNNABLE
            else:
                return
    
        while self._status == IntCodeStatus.RUNNABLE:
            pc = self._program_counter
            instruction = p[pc]
            opcode, mode1, mode2, mode3 = parse_instruction(instruction)
            pa1 = self.get_param_address(1, mode1)
            pa2 = self.get_param_address(2, mode2)
            pa3 = self.get_param_address(3, mode3)

            # Addition
            if opcode == 1:
                param1 = p[pa1]
                param2 = p[pa2]
                assert mode3 != 1
                if debug:
                    print(f"{p[pc:pc+4]}: p[{pa3}] = {param1} + {param2}")
                p[pa3] = param1 + param2
                pc += 4

            # Multiplication
            elif opcode == 2:
                param1 = p[pa1]
                param2 = p[pa2]
                assert mode3 != 1
                if debug:
                    print(f"{p[pc:pc+4]}: p[{pa3}] = {param1} * {param2}")
                p[pa3] = param1 * param2
                pc += 4

            # Input
            elif opcode == 3:
                assert mode1 != 1
                if len(self._input) == 0:
                    self._status = IntCodeStatus.IOBLOCK
                    return
                user_input = self._input.pop()
                p[pa1] = user_input
                if debug:
                    print(f"{p[pc:pc+2]}: p[{pa1}] = {user_input}")
                pc += 2

            # Output
            elif opcode == 4:
                param1 = p[pa1]
                if debug:
                    print(f"{p[pc:pc+2]}: {param1} (p[{pa1}])")

                self._output_buffer.append(param1)
                pc += 2

            # Absolute Jump if Not Equal to Zero
            elif opcode == 5:
                param1 = p[pa1]
                param2 = p[pa2]
                if param1 != 0:
                    if debug:
                        print(f"{p[pc:pc+4]}: TODO")
                    pc = param2
                else:
                    if debug:
                        print(f"{p[pc:pc+4]}: TODO")
                    pc += 3

            # Absolute Jump if Equal to Zero
            elif opcode == 6:
                param1 = p[pa1]
                param2 = p[pa2]
                if param1 == 0:
                    if debug:
                        print(f"{p[pc:pc+4]}: TODO")
                    pc = param2
                else:
                    if debug:
                        print(f"{p[pc:pc+4]}: TODO")
                    pc += 3

            # Test Less Than
            elif opcode == 7:
                param1 = p[pa1]
                param2 = p[pa2]
                assert mode3 != 1
                if debug:
                    print(f"{p[pc:pc+4]}: p[{pa3}] = {param1} < {param2}")
                p[pa3] = int(param1 < param2)
                pc += 4

            # Test Equality
            elif opcode == 8:
                param1 = p[pa1]
                param2 = p[pa2]
                assert mode3 != 1
                if debug:
                    print(f"{p[pc:pc+4]}: p[{pa3}] = {param1} == {param2}")
                p[pa3] = int(param1 == param2)
                pc += 4

            # Update relative base offset
            elif opcode == 9:
                param1 = p[pa1]
                if debug:
                    print(f"{p[pc:pc+2]}: rel = {self._relative_base_offset} + {param1}")
                self._relative_base_offset += param1
                pc += 2

            # Halt
            elif opcode == 99:
                self._status = IntCodeStatus.HALTED

            else:
                raise Exception(f"Something went wrong at {pc}, value {instruction}")

            self._program_counter = pc

def solve_part_1(program):
    p = program[:]
    p[1] = 12
    p[2] = 2
    runtime = IntCodeRuntime()
    runtime.set_program(p)
    runtime.run()
    return runtime.get_exit_code()

PART_2_EXPECTED_OUTPUT = 19690720
def solve_part_2(puzzle_input):
    output = 0
    for i in range(100):
        for j in range(100):
            program = puzzle_input[:]
            program[1] = i
            program[2] = j
            runtime = IntCodeRuntime()
            runtime.set_program(program)
            runtime.run()
            output = runtime.get_exit_code()
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