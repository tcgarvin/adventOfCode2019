from itertools import cycle

#import numpy as np
#import pandas as pd

BASE_PATTERN = [0,1,0,-1]

def generate_patterns(length):
    patterns = []
    for signal_position in range(length):
        pattern_stretch = signal_position + 1
        pattern_cycle = cycle(BASE_PATTERN)
        sequence = []
        while len(sequence) <= length:
            sequence.extend([next(pattern_cycle)] * pattern_stretch)
            
        patterns.append(sequence[1:length+1])

    pattern_array = pd.DataFrame(patterns, dtype="int8")
    return pattern_array

def signal_segment(signal, offset=0, length=8):
    return "".join((str(x) for x in signal[offset:offset+length]))

#def process(input_signal, offset=0, length=8):
#    pattern_matrix = generate_patterns(len(input_signal))
#
#    signal = pd.Series(input_signal, dtype="int8")
#    for i in range(100):
#        signal = pattern_matrix.mul(signal).sum(axis=1).abs().mod(10)
#        print(i, signal_segment(signal))
#
#    return signal_segment(signal, offset, length)

def process_lowmem(signal, offset=0, length=8):
    signal_length = len(signal)
    next_signal = [0] * signal_length
    for phase in range(100):
        if (offset > signal_length / 2):
            # This solution only came from literally hours of reading hints and
            # trying to understand why other's solutions worked. Based on the
            # shape of the pattern matrix, you can see that digits of the
            # signal are only influenced by digits that come after them. If you
            # _also_ notice that the offset in the puzzle input is close to the
            # end of the signal, you can use this to shrink the amount of work
            # you need to do quadratically. Finally, if you notice that halfway
            # down the pattern matrix, all of the signal values are 1, you
            # realize that each new value is just the sum of all digits from it
            # to the end. Finally, you may realize that the difference between
            # any two new digits in the next phase is just the difference of
            # one digit, and then you can do a partial-sum kind of thing, just
            # adding one digit at a time, and dropping off the intermediate
            # values along the way. Way too many "Aha" moments for me to find
            # them all.
            total = 0
            for i in range(signal_length - 1, offset - 1, -1):
                total += signal[i]
                next_signal[i] = total % 10

        else:
            for pattern_iteration in range(offset, signal_length):
                skip = pattern_iteration
                pattern_stretch = pattern_iteration + 1
                cycle_size = 4 * pattern_stretch
                half_cycle = 2 * pattern_stretch
                total = 0
                for digit_index in range(skip,signal_length,cycle_size):
                    end_index = min(digit_index + pattern_stretch, signal_length)
                    total += sum(signal[digit_index:end_index])

                    sub_index = min(digit_index + half_cycle, signal_length)
                    sub_end_index = min(sub_index + pattern_stretch, signal_length)
                    total -= sum(signal[sub_index:sub_end_index])

                next_signal[pattern_iteration] = abs(total) % 10

        temp = signal
        signal = next_signal
        next_signal = temp
        print(phase, signal_segment(signal, offset, length))

    return signal_segment(signal, offset, length)

def solve_part_1(puzzle_input):
    #result = process(puzzle_input, 0, 8)
    result = process_lowmem(puzzle_input[:], 0, 8)
    return result

def solve_part_2(puzzle_input):
    signal = puzzle_input * 10000
    offset = int(signal_segment(signal,0,7))
    return process_lowmem(signal, offset, 8)

def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            puzzle_input = [int(c) for c in line.strip()]
    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")