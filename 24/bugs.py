from copy import deepcopy
from collections import defaultdict

def solve_part_1(puzzle_input):
    seen_biodiversity = set()

    state = deepcopy(puzzle_input)
    next_state = [[0] * 5 for x in range(5)]
    while True:
        next_bio_rating = 0
        for x in range(25):
            i = x % 5
            j = x // 5

            adjacent = 0
            if i > 0:
                adjacent += state[j][i-1]
            if i < 4:
                adjacent += state[j][i+1]
            if j > 0:
                adjacent += state[j-1][i]
            if j < 4:
                adjacent += state[j+1][i]

            if adjacent == 1 or (adjacent == 2 and state[j][i] == 0):
                next_state[j][i] = 1
                next_bio_rating += pow(2, x)
            else:
                next_state[j][i] = 0

        if next_bio_rating in seen_biodiversity:
            return next_bio_rating
        seen_biodiversity.add(next_bio_rating)

        temp = state
        state = next_state
        next_state = temp
            
    return "Uh oh"

def generate_empty_level():
    return [[0] * 5 for x in range(5)]

def solve_part_2(puzzle_input):
    state = {}
    next_state = {}
    for i in range(-101, 102):
        state[i] = generate_empty_level()
        next_state[i] = generate_empty_level()

    state[0] = deepcopy(puzzle_input)

    for minute in range(200):
        for l, level in state.items():
            if l > 100 or l < -100:
                continue
            inner_level = state[l+1]
            outer_level = state[l-1]
            next_level = next_state[l]
            for x in range(25):
                i = x % 5
                j = x // 5

                if i == 2 and j == 2:
                    continue

                adjacent = 0
                if i == 3 and j == 2:
                    adjacent += inner_level[0][4]
                    adjacent += inner_level[1][4]
                    adjacent += inner_level[2][4]
                    adjacent += inner_level[3][4]
                    adjacent += inner_level[4][4]
                elif i == 0:
                    adjacent += outer_level[2][1]
                elif i > 0:
                    adjacent += level[j][i-1]

                if i == 1 and j == 2:
                    adjacent += inner_level[0][0]
                    adjacent += inner_level[1][0]
                    adjacent += inner_level[2][0]
                    adjacent += inner_level[3][0]
                    adjacent += inner_level[4][0]
                elif i == 4:
                    adjacent += outer_level[2][3]
                elif i < 4:
                    adjacent += level[j][i+1]

                if j == 3 and i == 2:
                    adjacent += inner_level[4][0]
                    adjacent += inner_level[4][1]
                    adjacent += inner_level[4][2]
                    adjacent += inner_level[4][3]
                    adjacent += inner_level[4][4]
                elif j == 0:
                    adjacent += outer_level[1][2]
                elif j > 0:
                    adjacent += level[j-1][i]

                if j == 1 and i == 2:
                    adjacent += inner_level[0][0]
                    adjacent += inner_level[0][1]
                    adjacent += inner_level[0][2]
                    adjacent += inner_level[0][3]
                    adjacent += inner_level[0][4]
                elif j == 4:
                    adjacent += outer_level[3][2]
                elif j < 4:
                    adjacent += level[j+1][i]

                if adjacent == 1 or (adjacent == 2 and level[j][i] == 0):
                    next_level[j][i] = 1
                else:
                    next_level[j][i] = 0

        temp = state
        state = next_state
        next_state = temp

    bugs = 0
    for level in state.values():
        for line in level:
            for bug in line:
                bugs += bug

    return bugs


def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            puzzle_input.append([1 if c == "#" else 0 for c in line.strip()])
    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")