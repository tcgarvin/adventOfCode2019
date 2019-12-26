from collections import deque
from heapq import heappush, heappop

WALL = "#"
HALL = "."
SPACE = " "

COMMON_PARTS = set((WALL, HALL, SPACE))

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

DIRECTIONS = (LEFT, UP, RIGHT, DOWN)

START_PORTAL = ("A","A")
END_PORTAL = ("Z","Z")

def get_portals(grid): 
    portal_endpoints = {}
    portals = {}
    start = None
    end = None
    for j in range(1, len(grid) - 1):
        line = grid[j]
        for i in range(1, len(line) - 1):
            char = line[i]
            if char not in COMMON_PARTS:
                other = None
                portal_endpoint = None
                for di, dj in DIRECTIONS:
                    neighbor = grid[j + dj][i + di]
                    if neighbor == HALL:
                        portal_endpoint = (i + di, j + dj)

                    elif neighbor not in COMMON_PARTS:
                        other = neighbor
                
                if portal_endpoint is None:
                    continue

                portal_name = tuple(sorted((char,other)))
                if portal_name == START_PORTAL:
                    start = portal_endpoint

                elif portal_name == END_PORTAL:
                    end = portal_endpoint

                elif portal_name in portal_endpoints:
                    other_endpoint = portal_endpoints[portal_name]
                    portals[portal_endpoint] = other_endpoint
                    portals[other_endpoint] = portal_endpoint

                else:
                    portal_endpoints[portal_name] = portal_endpoint

    return portals, start, end

def navigate_maze(grid, portals, start, end):
    explore_queue = deque()
    start_i, start_j = start
    end_i, end_j = end
    seen = {}
    explore_queue.appendleft((start_i, start_j, 0))
    while len(explore_queue) > 0:
        i, j, distance = explore_queue.pop()

        if i == end_i and j == end_j:
            return distance

        char = grid[j][i]
        assert char == HALL

        if seen.get((i,j), 100000) < distance:
            continue
        seen[(i,j)] = distance

        for di, dj in DIRECTIONS:
            ni = i + di
            nj = j + dj
            neighbor_char = grid[nj][ni]
            if neighbor_char == HALL:
                explore_queue.appendleft((ni, nj, distance + 1))
            if neighbor_char not in COMMON_PARTS and neighbor_char != "A":
                pi,pj = portals[(i, j)]
                explore_queue.appendleft((pi, pj, distance + 1))

def get_outer_portal_distances(grid): 
    portal_endpoints = {}
    portals = {}
    start = None
    end = None
    for j in range(1, len(grid) - 1):
        line = grid[j]
        for i in range(1, len(line) - 1):
            char = line[i]
            if char not in COMMON_PARTS:
                other = None
                portal_endpoint = None
                for di, dj in DIRECTIONS:
                    neighbor = grid[j + dj][i + di]
                    if neighbor == HALL:
                        portal_endpoint = (i + di, j + dj)

                    elif neighbor not in COMMON_PARTS:
                        other = neighbor
                
                if portal_endpoint is None:
                    continue

                portal_name = tuple(sorted((char,other)))
                if portal_name == START_PORTAL:
                    start = portal_endpoint

                elif portal_name == END_PORTAL:
                    end = portal_endpoint

                elif portal_name in portal_endpoints:
                    other_endpoint = portal_endpoints[portal_name]
                    portals[portal_endpoint] = other_endpoint
                    portals[other_endpoint] = portal_endpoint

                else:
                    portal_endpoints[portal_name] = portal_endpoint

    return portals, start, end

def navigate_recursive_maze(grid, portals, start, end, outer_box):
    explore_queue = []
    start_i, start_j = start
    end_i, end_j = end
    seen = {}
    heappush(explore_queue, (0, 0, start_i, start_j))
    iteration = 0
    while len(explore_queue) > 0:
        level, distance, i, j = heappop(explore_queue)

        iteration += 1
        if iteration % 100000 == 0:
            print(iteration, level, distance, len(seen))

        if i == end_i and j == end_j and level == 0:
            return distance

        char = grid[j][i]
        assert char == HALL

        for di, dj in DIRECTIONS:
            ni = i + di
            nj = j + dj
            neighbor_char = grid[nj][ni]

            if neighbor_char == HALL:
                if seen.get((ni,nj,level), 1000000000) < distance:
                    continue
                seen[(ni,nj,level)] = distance + 1
                heappush(explore_queue, (level, distance + 1, ni, nj))
            if neighbor_char not in COMMON_PARTS and (i,j) != start and (i,j) != end:
                pi,pj = portals[(i, j)]
                new_level = level + 1
                if i == outer_box[0] or i == outer_box[1] or j == outer_box[2] or j == outer_box[3]:
                    new_level = level - 1
                if new_level >= 0:
                    if seen.get((pi,pj,new_level), 1000000000) < distance:
                        continue
                    seen[(pi,pj,new_level)] = distance + 1
                    heappush(explore_queue, (new_level, distance + 1, pi, pj))

    return "Uh oh"

def outer_portal_box(puzzle_input):
    return (2,len(puzzle_input[0])-3,2,len(puzzle_input)-3)

def solve_part_1(puzzle_input):
    portals, start, end = get_portals(puzzle_input)
    shortest_distance = navigate_maze(puzzle_input, portals, start, end)
    return shortest_distance

def solve_part_2(puzzle_input):
    portals, start, end = get_portals(puzzle_input)
    shortest_distance = navigate_recursive_maze(puzzle_input, portals, start, end, outer_portal_box(puzzle_input))
    return shortest_distance

def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            puzzle_input.append(list(line[:-1]))
    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")