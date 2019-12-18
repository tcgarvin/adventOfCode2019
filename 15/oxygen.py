from collections import defaultdict
from time import sleep

from intcode import get_program_input, IntCodeRuntime, IntCodeStatus

WALL = 0
OPEN = 1
OXYGEN = 2
UNEXPLORED = -1
DROID = -2

DISPLAY_MAP = {
    WALL: "#",
    OPEN: ".",
    OXYGEN: "!",
    UNEXPLORED: " ",
    DROID: "@"
}

class Direction:
    def __init__(self, id, dx, dy):
        self.id = id
        self.dx = dx
        self.dy = dy

MOVE_NORTH = Direction(1,0,1)
MOVE_SOUTH = Direction(2,0,-1)
MOVE_WEST = Direction(3,-1,0)
MOVE_EAST = Direction(4,1,0)
DIRECTIONS = [MOVE_NORTH, MOVE_WEST, MOVE_SOUTH, MOVE_EAST]

class DroidController:
    def __init__(self, runtime):
        self.x = 0
        self.y = 0
        self.runtime = runtime
        self.seen = defaultdict(lambda: UNEXPLORED)
        self.seen[(0,0)] = OPEN
        self.oxygen_system_location = None

    def print_map(self):
        window = [[-1 for _ in range(11)] for __ in range(11)]
        cx = self.x
        cy = self.y
        for i in range(0,11):
            x = i + cx - 5
            for j in range(0,11):
                y = j + cy - 5
                window[j][i] = self.seen[(x,y)]

        window[5][5] = -2

        output = "\n"
        for line in window:
            output = output + "".join((DISPLAY_MAP[cell] for cell in line)) + "\n"

        print(output)

    def move(self, direction):
        self.runtime.input_number(direction.id)
        self.runtime.run()
        output = self.runtime.get_output()
        assert len(output) == 1
        result = output[0]

        new_coord = (self.x + direction.dx, self.y + direction.dy)
        self.seen[new_coord] = result

        if result != WALL:
            self.x += direction.dx
            self.y += direction.dy

        #self.print_map()
        #sleep(1/60)

        return result

    def explore(self, distance, mode=0):
        furthest_distance = distance + 1
        for direction in DIRECTIONS:
            new_coord = (self.x + direction.dx, self.y + direction.dy)
            if self.seen[new_coord] != UNEXPLORED:
                continue

            move_result = self.move(direction)

            if move_result == WALL:
                continue
            elif move_result == OXYGEN and mode == 0:
                self.oxygen_system_location = (self.x,self.y)
                return distance + 1

            found_distance = self.explore(distance + 1, mode)
            if mode == 1:
                furthest_distance = max(furthest_distance, found_distance)
            elif found_distance != -1:
                return found_distance

            opposite_direction = DIRECTIONS[(DIRECTIONS.index(direction) + 2) % 4]
            self.move(opposite_direction)

        if mode == 0:
            return -1
        return furthest_distance
        


def solve_part_1(puzzle_input):
    runtime = IntCodeRuntime()
    runtime.set_program(puzzle_input[:])
    runtime.run()

    droid = DroidController(runtime)
    distance = droid.explore(0)
    return distance, runtime

def solve_part_2(runtime):
    droid = DroidController(runtime)
    return droid.explore(0,mode=1)

if __name__ == "__main__":
    puzzle_input = get_program_input("input.txt")

    answer_1, runtime = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(runtime)
    print(f"Part 2: {answer_2}")