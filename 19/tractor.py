from math import ceil, floor
from intcode import get_program_input, IntCodeRuntime, IntCodeStatus

def send_drone(program, x, y):
    runtime = IntCodeRuntime()
    runtime.set_program(puzzle_input[:])
    runtime.input_number(x)
    runtime.input_number(y)
    runtime.run()
    return runtime.get_output()[0]

def solve_part_1(puzzle_input):
    detected_grid = []
    points_affected = 0

    for y in range(50):
        line = []
        detected_grid.append(line)
        last_reading = 0
        edge_down = False
        for x in range(50):
            if edge_down:
                line.append(0)
                continue

            reading = send_drone(puzzle_input, x, y)
            line.append(reading)
            points_affected += reading

            if last_reading == 1 and reading == 0:
                edge_down = True
            last_reading = reading

    #for line in detected_grid:
    #    translation = ("." if d == 0 else "#" for d in line)
    #    print("".join(translation))

    return points_affected

def solve_part_2(puzzle_input):
    # ll -> Lower Left
    llx = 4
    lly = 5
    conservative_bottom_slope = (5/4)
    aggressive_bottom_slope = (4/3)
    conservative_top_slope = (11/10)
    aggressive_top_slope = (10/9)
    aggressive_spread = (conservative_bottom_slope - aggressive_top_slope) * 2
    estimated_deficit = int(98 // aggressive_spread)
    solution = None
    while solution is None:
        llx = llx + estimated_deficit

        #Binary search for lower-left y
        min_lly = lly + floor(estimated_deficit * conservative_bottom_slope)
        assert send_drone(puzzle_input, llx, min_lly) == 1
        max_lly = lly + ceil(estimated_deficit * aggressive_bottom_slope) + 1
        assert send_drone(puzzle_input, llx, max_lly) == 0
        while max_lly - min_lly > 1:
            try_lly = (max_lly + min_lly) // 2
            reading = send_drone(puzzle_input, llx, try_lly)
            if reading == 1:
                min_lly = try_lly
            else:
                max_lly = try_lly

        lly = min_lly

        ulx = llx
        uly = lly - 99

        if send_drone(puzzle_input, ulx, uly) == 0:
            # Binary search for beam top
            min_top = uly
            max_top = lly
            while max_top - min_top > 1:
                try_top = (max_top + min_top) // 2
                reading = send_drone(puzzle_input, ulx, try_top)
                if reading == 1:
                    max_top = try_top
                else:
                    min_top = try_top

            top = max_top
            estimated_deficit = max(1, int((top - uly) // aggressive_spread))
            continue

        urx = ulx + 99
        ury = uly

        if send_drone(puzzle_input, urx, ury) == 0:
            #binary search for beam right
            max_right = urx
            min_right = ulx
            while max_right - min_right > 1:
                try_right = (max_right + min_right) // 2
                reading = send_drone(puzzle_input, try_right, ury)
                if reading == 1:
                    min_right = try_right
                else:
                    max_right = try_right

            right = min_right
            estimated_deficit = max(1, int((urx - right) // (aggressive_spread * 2)))
            continue

        solution = (ulx, uly)

    return solution[0] * 10000 + solution[1]

if __name__ == "__main__":
    puzzle_input = get_program_input("input.txt")

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")