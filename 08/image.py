def solve_part_1(puzzle_input):
    num_digits = len(puzzle_input)
    layers = []
    for l in range(num_digits // (25 * 6)):
        starting_position = l * 25 * 6
        layers.append(puzzle_input[starting_position : starting_position + 150])

    fewest_zeros = 150
    num_ones = 0
    num_twos = 0
    for layer in layers:
        zeros = layer.count(0)
        if zeros < fewest_zeros:
            fewest_zeros = zeros
            num_ones = layer.count(1)
            num_twos = layer.count(2)

    return num_ones * num_twos, layers

def solve_part_2(layers):
    rendering = layers[-1]
    for layer in reversed(layers[:-1]):
        for i in range(150):
            rendering[i] = layer[i] if layer[i] != 2 else rendering[i]

    assert rendering.count(2) == 0

    paint = "".join(["#" if p == 1 else " " for p in rendering])

    result = "\n"
    for i in range(6):
        result = result + paint[i * 25 : i * 25 + 25] + "\n"
    return result

def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            puzzle_input = list(map(int, line.strip()))
    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1, layers = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(layers)
    print(f"Part 2: {answer_2}")