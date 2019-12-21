from intcode import IntCodeRuntime, IntCodeStatus, get_program_input

def print_map(to_print,highlight):
    for j,line in enumerate(to_print):
        for i, char in enumerate(line):
            if (i,j) == highlight:
                char = "O"
            print(char, end="")
        print("")

def solve_part_1(puzzle_input):
    runtime = IntCodeRuntime()
    runtime.set_program(puzzle_input[:])
    runtime.run()

    output = runtime.get_output()
    ascii_output = "".join(chr(code) for code in output)
    print(ascii_output)

    scaffold_map = []
    current_line = []
    for char in ascii_output:
        if char == "\n":
            scaffold_map.append(current_line)
            current_line = []
        else:
            current_line.append(char)

    alignment_sum = 0
    for j in range(1,len(scaffold_map)-2):
        for i in range(1, len(scaffold_map[j])-1):
            if scaffold_map[j][i] == "#" and \
               scaffold_map[j][i+1] == "#" and scaffold_map[j+1][i] == "#" and \
               scaffold_map[j][i-1] == "#" and scaffold_map[j-1][i] == "#":
            
                alignment_sum += j * i
    
    return alignment_sum

def solve_part_2(puzzle_input):
    # Not hard to do the paths by hand
    PART_2_PATH = "R,12,L,8,L,4,L,4,L,8,R,6,L,6,R,12,L,8,L,4,L,4,L,8,R,6,L,6,L,8,L,4,R,12,L,6,L,4,R,12,L,8,L,4,L,4,L,8,L,4,R,12,L,6,L,4,R,12,L,8,L,4,L,4,L,8,L,4,R,12,L,6,L,4,L,8,R,6,L,6"
    sub_paths = {
        "A": "R,12,L,8,L,4,L,4",
        "B": "L,8,L,4,R,12,L,6,L,4",
        "C": "L,8,R,6,L,6"
    }

    main_path = "A,C,A,C,B,A,B,A,B,C"

    logic_input = [main_path, sub_paths["A"], sub_paths["B"], sub_paths["C"], "n"]

    program = puzzle_input[:]
    program[0] = 2
    runtime = IntCodeRuntime()
    runtime.set_program(program)

    for line in logic_input:
        for char in line:
            runtime.input_number(ord(char))
        runtime.input_number(ord("\n"))

    runtime.run()

    return runtime.get_output()[-1]

if __name__ == "__main__":
    puzzle_input = get_program_input("input.txt")

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")