from sys import argv
from time import perf_counter_ns

def solve_part_1(range_start, range_end):
    digits_visited = 0
    viable_passwords = set()

    start_time = perf_counter_ns()
    for candidate in range(range_start, range_end+1):
        digits = map(int, str(candidate))
        double = False
        decreases = False
        prev = 0
        for digit in digits:
            digits_visited += 1
            if digit == prev:
                double = True
            elif digit < prev:
                decreases = True
                break
            prev = digit

        if double and not decreases:
            viable_passwords.add(candidate)
    end_time = perf_counter_ns()

    print(f"Digits visited: {digits_visited}")
    print(f"Time spent: {(end_time - start_time) // 1000000}ms")
    print(f"Time per digit: {(end_time - start_time) // digits_visited}ns/d")
    return len(viable_passwords), viable_passwords

def solve_part_2(candidates):
    viable_passwords = set()
    for candidate in range(range_start, range_end+1):
        digits = map(int, str(candidate))
        double = False
        decreases = False
        group_size = 1
        prev = 0
        for digit in digits:
            if digit < prev:
                decreases = True
                break

            if digit == prev:
                group_size += 1
            else:
                if group_size == 2:
                    double = True
                group_size = 1

            prev = digit

        if group_size == 2:
            double = True

        if double and not decreases:
            viable_passwords.add(candidate)

    return len(viable_passwords)

if __name__ == "__main__":
    range_start = int(argv[1])
    range_end = int(argv[2])

    answer_1, candidates = solve_part_1(range_start, range_end)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(candidates)
    print(f"Part 2: {answer_2}")