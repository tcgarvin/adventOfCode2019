from collections import defaultdict

from intcode import get_program_input, IntCodeRuntime, IntCodeStatus

WEST = (-1,0)
SOUTH = (0,-1)
EAST = (1,0)
NORTH = (0,1)

DIRECTIONS = (WEST, SOUTH, EAST, NORTH)

LEFT_TURN = 0
RIGHT_TURN = 1

def get_new_direction(current_direction, turn):
    current_direction = DIRECTIONS.index(current_direction)
    if turn == LEFT_TURN:
        shift = 1
    elif turn == RIGHT_TURN:
        shift = -1

    new_direction = DIRECTIONS[(current_direction + shift) % len(DIRECTIONS)]
    return new_direction

def solve(puzzle_input, start_square=0):
    painted = set()
    grid = defaultdict(int)

    runtime = IntCodeRuntime()
    runtime.set_program(puzzle_input[:])

    x,y = (0,0)
    grid[(x,y)] = start_square
    dx,dy = NORTH
    while runtime.get_status() != IntCodeStatus.HALTED:
        runtime.input_number(grid[(x,y)])
        runtime.run()
        output = runtime.get_output()
        assert len(output) == 2
        grid[(x,y)] = output[0]
        painted.add((x,y))
        dx,dy = get_new_direction((dx,dy),output[1])
        x,y = (x + dx, y + dy)

    return len(painted), grid

def solve_part_1(puzzle_input):
    painted, grid = solve(puzzle_input)
    return painted

def solve_part_2(puzzle_input):
    painted, grid = solve(puzzle_input, 1)
    
    # Cheating here, inspected the grid by hand and found it to be 6 lines high
    grid_array = [[0 for _ in range(50)] for _ in range(6)]

    for x,y in grid.keys():
        grid_array[-y][x] = grid[(x,y)]

    result = "\n"
    for line in grid_array:
        result = result + "".join(("#" if x == 1 else " " for x in line)) + "\n"
    return result

if __name__ == "__main__":
    puzzle_input = get_program_input("input.txt")

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")