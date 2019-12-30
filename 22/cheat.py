# This solution is taken wholesale from
# https://www.reddit.com/r/adventofcode/comments/ee0rqi/2019_day_22_solutions/fbnkaju/
# There is a fair amount of math here that is very nearly beyond me, and I did
# not perceive even the initial insight (the operations are a linear
# combination of offset and increment opperations) on my own.

# See shuffle.py for unsuccessful way I was trying to do it. (Looking for periodicity in the shuffling)

REVERSE = "deal into new"
CUT = "cut"
INCREMENT = "deal with increment"

def reverse(deck):
    return list(reversed(deck))

def cut(deck, index):
    return deck[index:] + deck[:index]

def increment(deck, offset):
    returnable = [None for x in range(10007)]
    i = 0
    for card in deck:
        returnable[i % 10007] = card
        i += offset
    
    return returnable

def solve_part_1(puzzle_input):
    deck = [x for x in range(10007)]
    for action, argument in puzzle_input:
        if action == REVERSE:
            deck = reverse(deck)
        if action == CUT:
            deck = cut(deck, argument)
        if action == INCREMENT:
            deck = increment(deck, argument)

    return deck.index(2019)

def solve_part_2(puzzle_input):
    deck_size = 119315717514047
    number_of_shuffles = 101741582076661
    initial_position = 2020
    position = initial_position

    # The initial deck can be described by saying "The first card is 0, and all
    # others increment by 1 from there". We take these numbers to be subject to
    # modulus.
    offset = 0 
    increment = 1
    for command, argument in puzzle_input:
        if command == REVERSE:
            # If reversing, we say "the increment needs to reverse and the
            # offset flips all the way to the other end". If coming from the
            # first deck (0,1), we know we want offset to be -1, so the first
            # card becomes the last. It's not clear to me why we can extend
            # this generally to be just `+increment`.
            increment *= -1
            increment %= deck_size
            offset += increment
            offset %= deck_size

        elif command == CUT:
            # If we think about the CUT command as a shift, all we have to do
            # is get the nth card, and move it to the front. The statement
            # about extending to use increment generally still applies.
            offset += increment * argument
            offset %= deck_size

        elif command == INCREMENT:
            # No idea how this works. Involves inverse modulus (which I did
            # figure out), Fermat's little theorem (which I did not know), and
            # exponentiation by squaring (never heard of it).
            increment *= pow(argument, deck_size-2, deck_size)
            increment %= deck_size

    # Now we need to perform this increment * offset many, many times. This
    # involves some intuition in math that I'm not familiar enough with to try
    # to describe, as well as a reduction of a gemetric series stemming from
    # that intuition.  #AdventOfMath

    # The increment is not too hard though, we're just multiplying it by itself for as many times as we shuffle, and use modulus
    total_increment = pow(increment, number_of_shuffles, deck_size)
    total_offset = offset * (1 - pow(increment, number_of_shuffles, deck_size)) * pow((1 - increment) % deck_size, deck_size - 2, deck_size)
    total_offset %= deck_size

    result = (total_offset + total_increment * 2020) % deck_size

    return result

def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
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