from fractions import Fraction

def order_by_distance(x, y, asteroids):


def solve_part_1(field):
    width = len(field[0])
    height = len(field)

    best_num_asteroids_visible = 0
    best_x = None
    best_y = None
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
                    asteroids_above.append((i,j))
                    break

            for j in range(y+1,height):
                if field[j][x] is True:
                    asteroids_below.append((i,j))
                    break

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
            if len(asteroids_above) > 0
                count_asteroid_above = 1

            count_asteroid_below = 0
            if len(asteroids_below) > 0:
                count_asteroid_below = 1

            asteroids_visible = count_asteroid_above + count_asteroid_below + len(left_side_angles) + len(right_side_angles)
            if asteroids_visible > best_num_asteroids_visible:
                best_num_asteroids_visible = asteroids_visible
                best_x, best_y = x,y

    return best_num_asteroids_visible, ((x,y), asteroids_above, asteroids_below, left_side_angles, right_side_angles)

def solve_part_2(base_coords,asteroids_above, asteroids_below, left_side_angles, right_side_angles):
    angles_in_order = []
    angles_in_order.append(asteroids_above)

    for asteroids in sorted(left_side_angles.keys())
    
    return ""

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

    answer_2 = solve_part_2(relevant_asteroids)
    print(f"Part 2: {answer_2}")