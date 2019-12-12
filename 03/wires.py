from collections import defaultdict
from collections import namedtuple

WirePlace = namedtuple('WirePlace', ['x', 'y', 'distance'])

def manhattan_distance(x_y_coords):
    return abs(x_y_coords[0]) + abs(x_y_coords[1])

def wire_distance(places):
    return places[0].distance + places[1].distance

def solve_part_1(wires):
    coordinate_index = defaultdict(dict)

    for i, wire in enumerate(wires):
        x = 0
        y = 0
        total_distance = 0
        for direction, distance in wire:
            for _ in range(distance):
                if direction == "U":
                    y += 1
                elif direction == "D":
                    y -= 1
                elif direction == "L":
                    x -= 1
                elif direction == "R":
                    x += 1
                else:
                    raise Exception(f"Invalid direction {direction}")

                total_distance += 1

                location = coordinate_index[(x,y)]
                if i not in location:
                    location[i] = WirePlace(x, y, total_distance)

    intersection_points = list(filter(lambda item: len(item[1]) > 1, coordinate_index.items()))
    #print(list(intersection_points))
    closest_coord, _ = sorted(intersection_points, key=lambda item: manhattan_distance(item[0]))[0]
    
    return manhattan_distance(closest_coord), intersection_points

def solve_part_2(intersection_points):
    #print(intersection_points)
    _, places = sorted(intersection_points, key=lambda item: wire_distance(item[1]))[0]
    print(places)
    return wire_distance(places)

def get_puzzle_input():
    wires = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            segments = map(lambda token:(token[0], int(token[1:])), line.split(","))
            wires.append(segments)
    return wires

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1, board = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(board)
    print(f"Part 2: {answer_2}")