from collections import defaultdict

class Mass:
    def __init__(self):
        self.satellites = set()
        self.orbiting = None
        self.neighbors = set()

    def add_satellite(self, satellite):
        self.satellites.add(satellite)
        self.neighbors.add(satellite)

    def add_target_of_orbit(self, center):
        self.orbiting = center
        self.neighbors.add(center)

    def get_orbits(self):
        total_orbits = 0
        total_satellites = 0
        for satellite in self.satellites:
            orbits, num_satellites = satellite.get_orbits()
            total_orbits += orbits
            total_satellites += num_satellites + 1

        total_orbits += total_satellites
        return total_orbits, total_satellites

    def get_path_to_com(self, mass_index):
        current_mass = self
        path = []
        com = mass_index["COM"]
        while current_mass != com:
            current_mass = current_mass.orbiting
            path.append(current_mass)

        return path


def solve_part_1(puzzle_input):
    mass_index = defaultdict(Mass)

    for pair in puzzle_input:
        center = mass_index[pair[0]]
        satellite = mass_index[pair[1]]

        center.add_satellite(satellite)
        satellite.add_target_of_orbit(center)

    orbits, satellites = mass_index["COM"].get_orbits()
        
    return orbits, mass_index

def solve_part_2(mass_index):
    """
    Determine length of path between YOU and SAN by comparing the (easier to
    find) paths of both to the (root) center of mass. The length of the path
    between YOU and SAN then becomes the length of the paths to root that are
    unique to each.  At first expected an off-by-one error here, but the
    particulars of the puzzle work in our favor.
    """
    santa = mass_index["SAN"]
    you = mass_index["YOU"]

    santa_path_to_root = santa.get_path_to_com(mass_index)
    print(santa_path_to_root)
    you_path_to_root = you.get_path_to_com(mass_index)
    print(you_path_to_root)

    return len(set(santa_path_to_root).symmetric_difference(set(you_path_to_root)))

def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            puzzle_input.append(tuple(line.strip().split(")")))
    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1, mass_index = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(mass_index)
    print(f"Part 2: {answer_2}")