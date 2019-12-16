import re

PART_1_CYCLES = 1000

position_format = re.compile("""
    ^<x=(?P<x>[-0-9]+),\ y=(?P<y>[-0-9]+),\ z=(?P<z>[-0-9]+)>$
""", re.X)

def parse_initial_position(line):
    match = position_format.match(line)
    return map(int, match.group('x','y','z'))

class Body:
    def __init__(self, name, x, y, z):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0
        self.vy = 0
        self.vz = 0

        self.initial_x = x
        self.initial_y = y
        self.initial_z = z
        self.initial_vx = 0
        self.initial_vy = 0
        self.initial_vz = 0

    def update_velocity(self, other):
        if self.x > other.x:
            self.vx -= 1
        elif self.x < other.x:
            self.vx += 1

        if self.y > other.y:
            self.vy -= 1
        elif self.y < other.y:
            self.vy += 1

        if self.z > other.z:
            self.vz -= 1
        elif self.z < other.z:
            self.vz += 1

    def update_position(self):
        self.x += self.vx
        self.y += self.vy
        self.z += self.vz

    def x_matches_initial(self):
        return self.vx == 0 and self.x == self.initial_x

    def y_matches_initial(self):
        return self.vy == 0 and self.y == self.initial_y

    def z_matches_initial(self):
        return self.vz == 0 and self.z == self.initial_z

def gcd(a,b):
    # Pulled straight from wikipedia. Did not bother to grok.
    orig_a = a
    orig_b = b
    while b != 0:
        t = b
        b = a % b
        a = t

    assert orig_a % a == 0
    assert orig_b % a == 0
    return a

def lcm_2(a,b):
    divisor = gcd(a,b)
    ab = a * b / divisor
    assert ab % a == 0 
    assert ab % b == 0
    return int(ab)


def lcm(x,y,z):
    xy = lcm_2(x,y)
    xyz = lcm_2(xy,z)
    assert xyz % x == 0
    assert xyz % y == 0
    assert xyz % z == 0
    return xyz

def solve_part_1(bodies):
    for _ in range(PART_1_CYCLES):
        for body in bodies:
            for other in bodies:
                if body is other:
                    continue
                body.update_velocity(other)

        for body in bodies:
            body.update_position()

    total_energy = 0
    for body in bodies:
        energy =  abs(body.x)  + abs(body.y)  + abs(body.z)
        energy *= abs(body.vx) + abs(body.vy) + abs(body.vz)
        total_energy += energy

    return total_energy

def solve_part_2(bodies):
    count = PART_1_CYCLES # From part 1

    # Cheated here, had to go to the internet before I realized that each axis
    # of movement does not influence the others, and that there are therefore 3
    # distinct periods of movement along each axis. We can then gather the
    # period for each axis individually, and find the least common multiple to
    # come to an answer

    axis_periods = [None, None, None]
    while not all(axis_periods):
        for body in bodies:
            for other in bodies:
                if body is other:
                    continue
                body.update_velocity(other)

        for body in bodies:
            body.update_position()

        count += 1

        if not axis_periods[0] and all((body.x_matches_initial() for body in bodies)):
            axis_periods[0] = count

        if not axis_periods[1] and all((body.y_matches_initial() for body in bodies)):
            axis_periods[1] = count

        if not axis_periods[2] and all((body.z_matches_initial() for body in bodies)):
            axis_periods[2] = count

        if count % 10000000 == 0:
            print(count)

    #print(axis_periods)

    return lcm(*axis_periods)

def get_puzzle_input():
    puzzle_input = []
    names = ["Io", "Europa", "Ganymede", "Callisto"]
    with open("input.txt") as input_txt:
        for i, line in enumerate(input_txt):
            x, y, z = parse_initial_position(line)
            puzzle_input.append(Body(names[i], x, y, z))
    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")