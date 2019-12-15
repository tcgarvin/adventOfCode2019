from collections import defaultdict
from fractions import Fraction

def solve_part_1(field):
    width = len(field[0])
    height = len(field)

    best_num_asteroids_visible = 0
    best_x = None
    best_y = None
    best_asteroids_above = []
    best_asteroids_below = []
    best_right_side_angles = []
    best_left_side_angles = []
    for x in range(width):
        for y in range(height):
            if field[y][x] == False:
                continue

            # Using slope fractions (which python automatically reduces for us) to remove floating
            # point problems.  This implies a few things:
            #
            # 1. Need to handle denominator 0 as a special case (directly above and below)
            # 2. Need to handle left and right seperately
            asteroids_above = []
            asteroids_below = []

            for j in range(0,y):
                if field[j][x] is True:
                    asteroids_above.append((x,j))

            for j in range(y+1,height):
                if field[j][x] is True:
                    asteroids_below.append((x,j))

            # Left side
            left_side_angles = defaultdict(list)
            for i in range(0, x):
                for j in range(height):
                    if field[j][i] is True:
                        left_side_angles[Fraction(j-y, i-x)].append((i,j))

            # Right side
            right_side_angles = defaultdict(list)
            for i in range(x+1,width):
                for j in range(height):
                    if field[j][i] is True:
                        right_side_angles[Fraction(j-y, i-x)].append((i,j))

            count_asteroid_above = 0
            if len(asteroids_above) > 0:
                count_asteroid_above = 1

            count_asteroid_below = 0
            if len(asteroids_below) > 0:
                count_asteroid_below = 1

            asteroids_visible = count_asteroid_above + count_asteroid_below + len(left_side_angles) + len(right_side_angles)
            if asteroids_visible > best_num_asteroids_visible:
                best_num_asteroids_visible = asteroids_visible
                best_x, best_y = x,y
                best_asteroids_above = asteroids_above
                best_asteroids_below = asteroids_below
                best_left_side_angles = left_side_angles
                best_right_side_angles = right_side_angles

    return best_num_asteroids_visible, ((best_x,best_y), best_asteroids_above, best_asteroids_below, best_left_side_angles, best_right_side_angles)

def sorted_by_distance(asteroids, x, y):
    # manhatten distance is acceptable since all points line along the same line as (x,y)
    return sorted(asteroids, key=lambda coord: abs(coord[0]-x) + abs(coord[1]-y))

def solve_part_2(base_coords,asteroids_above, asteroids_below, left_side_angles, right_side_angles):
    x,y = base_coords
    angles_in_order = []
    angles_in_order.append(sorted_by_distance(asteroids_above, x,y))

    for angle in sorted(right_side_angles.keys()):
        angles_in_order.append(sorted_by_distance(right_side_angles[angle], x,y))

    angles_in_order.append(sorted_by_distance(asteroids_below, x,y))

    for angle in sorted(left_side_angles.keys()):
        angles_in_order.append(sorted_by_distance(left_side_angles[angle], x,y))

    # Vaporize all except the last pass
    passes = max(map(len, angles_in_order))

    inc = 1
    for angle in (angles_in_order):
        if len(angle) > 0:
            #print(f"{inc}: {angle[0][0]},{angle[0][1]}")
            if inc == 200:
                return angle[0][0] * 100 + angle[0][1]
            inc += 1
            del angle[0]

    #for angle in angles_in_order:
    #    del angle[:passes-1]

    #for angle in reversed(angles_in_order):
    #    if len(angle) > 0:
    #        return angle[-1][0] * 100 + angle[-1][1]
    
    raise Exception("Shouldn't have gotten here")

def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            puzzle_input.append([True if c == "#" else False for c in line.strip()])
    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1, relevant_asteroids = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(*relevant_asteroids)
    print(f"Part 2: {answer_2}")