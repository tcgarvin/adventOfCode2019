from time import sleep

from intcode import get_program_input, IntCodeRuntime, IntCodeStatus

tileset = {
    0: " ",
    1: "X",
    2: "=",
    3: "T",
    4: "o"
}

def refresh_screen(screen, segment_display, program_output):
    # Super hacky, would be more intuitive as a class method
    for i in range(0, len(program_output), 3):
        x = program_output[i]
        y = program_output[i+1]
        tile_id = program_output[i+2]

        if x == -1 and y == 0:
            segment_display = tile_id
            continue
        else:
            screen[y][x] = tileset[tile_id]

    to_print = [f"Score: {segment_display}"]
    for line in screen:
        to_print.append("".join(line))
    print("\n".join(to_print))
    return segment_display

def solve_part_1(puzzle_input):
    runtime = IntCodeRuntime()
    runtime.set_program(puzzle_input[:])
    runtime.run()

    output = runtime.get_output()
    tile_ids = output[2::3]
    count_blocks = 0
    for tile_id in tile_ids:
        if tile_id == 2:
            count_blocks += 1

    return count_blocks

joystick_signal_map = {
    "a": -1,
    "s": 0,
    "d": 1
}

def get_joystick_input(screen):
    ball_x = None
    paddle_x = None
    for line in reversed(screen):
        if ball_x is None and "o" in line:
            ball_x = line.index("o")

        if paddle_x is None and "T" in line:
            paddle_x = line.index("T")

        if ball_x is not None and paddle_x is not None:
            break
    
    if paddle_x < ball_x:
        return "d"
    elif paddle_x > ball_x:
        return "a"
    return "s"

def solve_part_2(puzzle_input):
    puzzle_input[0] = 2
    runtime = IntCodeRuntime()
    runtime.set_program(puzzle_input[:])
    screen = [[None for _ in range(45)] for __ in range(24)]
    segment_display = 0
    
    while runtime.get_status() != IntCodeStatus.HALTED:
        runtime.run()
        output = runtime.get_output()
        segment_display = refresh_screen(screen, segment_display, output)
        #joystick_input = input("Joystick Input: ")
        sleep(1/60)
        joystick_input = get_joystick_input(screen)
        joystick_signal = joystick_signal_map[joystick_input]
        runtime.input_number(joystick_signal)

    return "Game Over"

if __name__ == "__main__":
    puzzle_input = get_program_input("input.txt")

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")