from intcode import IntCodeRuntime, IntCodeStatus, get_program_input

from itertools import compress
from json import dump, load
from typing import List

def get_item_inventory(runtime : IntCodeRuntime):
    runtime.input_ascii("inv\n")
    runtime.run()
    output = runtime.get_ascii_output()
    print(output, end="")
    
    items = []
    for line in output.split("\n"):
        if line.startswith("- "):
            items.append(line.split(" ", 1)[1])
    return items

def hack_sensor(runtime : IntCodeRuntime):
    print("")
    print("Hacking sensor..")
    print("Checking inventory..")
    items = get_item_inventory(runtime)
    print(f"Found {len(items)} items.")

    combinations = pow(2,len(items))
    print(f"Checking against {combinations} possible combinations.")

    sucessful_combinations = []
    for i in range(combinations):
        for item in get_item_inventory(runtime):
            runtime.input_ascii(f"drop {item}\n")
            runtime.run()
            print(runtime.get_ascii_output(), end="")

        selectors = (1 if (1 << shift) & i else 0 for shift in range(len(items)))
        selections = list(compress(items, selectors))

        for item in selections:
            runtime.input_ascii(f"take {item}\n")
            runtime.run()
            print(runtime.get_ascii_output(), end="")

        runtime.input_ascii(f"south\n")
        runtime.run()
        output = runtime.get_ascii_output()
        print(output, end="")

        made_it = True
        for line in output.split("\n"):
            if "Alert!" in line:
                made_it = False

        if made_it:
            sucessful_combinations.append(selections)
            runtime.input_ascii(f"north\n") 
            runtime.run()
            print(runtime.get_ascii_output())

    for combination in sucessful_combinations:
        print("Successful combination: ", list(combination))
    
    print("")
    print("Command?")
        

def run_macro(runtime : IntCodeRuntime, macro : List[str]):
    for command in macro:
        runtime.input_ascii(command + "\n")
        runtime.run()
        print(runtime.get_ascii_output(), end="")

def solve_part_1(puzzle_input, macros):
    runtime = IntCodeRuntime()
    runtime.set_program(puzzle_input[:])
    recording = None
    while runtime.get_status() != IntCodeStatus.HALTED:
        runtime.run()
        print(runtime.get_ascii_output(), end="")

        command = input()
        if recording is not None:
            macros[recording].append(command)

        if command.startswith("record"):
            name = command.split()[-1]
            macros[name] = []
            recording = name
            print("")
            print(f"Recording macro `{name}`")
            print("")
            print("Command?")

        elif command.startswith("macro"):
            name = command.split()[-1]
            run_macro(runtime, macros[name])

        elif command.startswith("stop record"):
            print("")
            print(f"Stopping record of macro `{recording}`")
            print("")
            del macros[recording][-1]
            print("Macro saved with:")
            for item in macros[recording]:
                print(f"- {item}")
            recording = None
            print("")
            print("Command?")

        elif command.startswith("hack sensor"):
            hack_sensor(runtime)

        else:
            runtime.input_ascii(command + "\n")

    return ""

def solve_part_2(puzzle_input):
    return ""

if __name__ == "__main__":
    puzzle_input = get_program_input("input.txt")

    macros = {}
    with open("macros.json") as macros_file:
        macros = load(macros_file)
        print(f"Macros loaded: {list(macros.keys())}")

    try:
        answer_1 = solve_part_1(puzzle_input, macros)
        print(f"Part 1: {answer_1}")
    finally:
        with open("macros.json", "w") as macros_file:
            dump(macros, macros_file)

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")