from math import ceil

REVERSE = "deal into new"
CUT = "cut"
INCREMENT = "deal with increment"

def reverse(deck):
    return list(reversed(deck))

def cut(deck, index):
    return deck[index:] + deck[:index]

def increment(deck, offset):
    returnable = [None for x in range(10)]
    i = 0
    for card in deck:
        returnable[i % 10] = card
        i += offset
    
    return returnable

def solve_part_1(puzzle_input):
    deck = [x for x in range(10)]
    for action, argument in puzzle_input:
        if action == REVERSE:
            deck = reverse(deck)
        if action == CUT:
            deck = cut(deck, argument)
        if action == INCREMENT:
            deck = increment(deck, argument)

    return deck.index(0)

def solve_part_2(puzzle_input):
    deck_size = 10

    for position in range(10):
        print(position, ":", end = "")

        for action, argument in reversed(puzzle_input):
            if action == REVERSE:
                position = deck_size - position - 1

            elif action == CUT:
                if argument < 0:
                    argument = deck_size + argument

                argument_in_reverse = deck_size - argument
                
                if position < argument_in_reverse:
                    position += deck_size - argument_in_reverse
                else:
                    position -= argument_in_reverse

            elif action == INCREMENT:
                inc = argument
                reverse_remainder = 0 if (position % inc) == 0 else inc - (position % inc)
                slots = (position - 1) // inc + 1
                index = deck_size - reverse_remainder
                while reverse_remainder != 0:
                    reverse_remainder = 0 if (index % inc) == 0 else inc - (index % inc)
                    slots += (index - 1) // inc + 1
                    index = deck_size - reverse_remainder

                position = slots

        print(position)

    return position

def get_puzzle_input():
    puzzle_input = []
    with open("mini.txt") as input_txt:
        for line in input_txt:
            action = line.strip().rsplit(" ", maxsplit=1)
            if action[1] != "stack":
                action[1] = int(action[1])
            puzzle_input.append(action)
    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")