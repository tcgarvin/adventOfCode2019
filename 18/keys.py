from dataclasses import dataclass, field
from heapq import heappushpop, heappush, heappop
from statistics import mean
from typing import List, Set, Tuple

LEFT = (-1,0)
RIGHT = (1,0)
UP = (0,1)
DOWN = (0,-1)

DIRECTIONS = (UP,LEFT,DOWN,RIGHT)

KEYS = "abcdefghijklmnopqrstuvwxyz"
DOORS = KEYS.upper()

AVERAGE_DISTANCE = 0

class Graph:
    def __init__(self):
        self.index = {}
        self.index_by_content = {}

    def add_node(self, node):
        assert node.coordinates not in self.index
        self.index[node.coordinates] = node
        self.index_by_content[node.content] = node

    def get_node(self, x,y):
        return self.index.get((x,y), None)

    def get_node_by_content(self, content):
        return self.index_by_content[content] 

class GraphNode:
    def __init__(self, content, coordinates):
        self.coordinates = coordinates
        self.neighbors = []
        self.content = content

    def add_neighbor(self, neighbor, distance:int):
        for n, d in self.neighbors:
            if neighbor is n:
                assert distance == d
                return
            
        self.neighbors.append((neighbor,distance))
        
@dataclass(order=True)
class PartialPath:
    distance_estimate : int
    distance : int = field(compare=False)
    path : List[GraphNode] = field(compare=False)
    keys : Set[str] = field(compare=False)

class PathCache:
    def __init__(self):
        self._cache = {}

    def _gen_cache_key(self, partial : PartialPath):
        return (partial.path[-1].content, tuple(sorted(list(partial.keys))))

    def add(self, partial : PartialPath):
        self._cache[self._gen_cache_key(partial)] = partial.distance

    def get(self, partial : PartialPath):
        return self._cache.get(self._gen_cache_key(partial), 100000)


def explore_grid(grid, x : int, y : int, prev_x : int, prev_y : int, 
                 source_node : GraphNode, graph : Graph, leg_distance : int):

    # First, see if we are at a terminus/interesting node, and return if so
    content = grid[y][x]
    if content == "#":
        return set()

    if content in KEYS or content in DOORS:
        node = graph.get_node(x,y)
        if node is None:
            node = GraphNode(content, (x,y))
            graph.add_node(node)

        node.add_neighbor(source_node, leg_distance)
        source_node.add_neighbor(node, leg_distance)
        return set((node,))

    adjacent_openings = []
    for dir_x, dir_y in DIRECTIONS:
        next_x = x + dir_x
        next_y = y + dir_y
        if grid[next_y][next_x] != "#":
            adjacent_openings.append((next_x,next_y))

    #center_cross = abs(40-x) + abs(40-y) == 1 #special case to reduce complexity at center
    center_cross = False
    if len(adjacent_openings) > 2 and not center_cross:
        node = graph.get_node(x,y)
        if node is None:
            node = GraphNode(content, (x,y))
            graph.add_node(node)

        node.add_neighbor(source_node, leg_distance)
        source_node.add_neighbor(node, leg_distance)
        return set((node,))

    # if we're not at an interesting node, explore adjacent
    neighbor_nodes = set()
    for next_x, next_y in adjacent_openings:
        if next_x == prev_x and next_y == prev_y:
            continue

        neighbor_nodes.update(explore_grid(grid, next_x, next_y, x, y, source_node, graph, leg_distance + 1))

    return neighbor_nodes


def generate_graph(puzzle_input):
    graph = Graph()
    unexplored = set()
    for j, line in enumerate(puzzle_input):
        for i, char in enumerate(line):
            if char == "@":
                start_node = GraphNode("@", (i,j))
                graph.add_node(start_node)
                unexplored.add(start_node)
                
    explored = set()
    while len(unexplored) > 0:
        to_explore = unexplored.pop()
        if to_explore in explored:
            continue
        explored.add(to_explore)
        start_x, start_y = to_explore.coordinates
        for direction in DIRECTIONS:
            dir_x, dir_y = direction
            x = start_x + dir_x
            y = start_y + dir_y
            unexplored.update(explore_grid(puzzle_input, x, y, start_x, start_y, to_explore, graph, 1))

    return graph

def expand_path(partial_path : PartialPath, cache):
    if cache.get(partial_path) <= partial_path.distance:
        return []
    cache.add(partial_path)

    keys = partial_path.keys
    seen = set()
    seen.add(partial_path.path[-1])
    to_explore = set(partial_path.path[-1].neighbors)
    new_partial_paths = []
    while len(to_explore) > 0:
        neighbor, leg_distance = to_explore.pop()

        content = neighbor.content
        if content == "@":
            continue

        if neighbor in seen:
            continue
        seen.add(neighbor)

        if content in DOORS and content.lower() not in keys:
            continue

        if content in KEYS and content not in keys:
            new_distance_estimate = partial_path.distance_estimate - AVERAGE_DISTANCE + leg_distance
            new_distance = partial_path.distance + leg_distance
            new_path = partial_path.path[:] + [neighbor]
            new_keys = partial_path.keys.copy()
            new_keys.add(content)
            new_partial_paths.append(PartialPath(new_distance_estimate, new_distance, new_path, new_keys))
        else:
            for next_neighbor, next_leg_distance in neighbor.neighbors:
                to_explore.add((next_neighbor, leg_distance+next_leg_distance))

    return new_partial_paths

def collect_all_keys(graph):
    start_node = graph.get_node_by_content("@")
    initial_path = PartialPath(AVERAGE_DISTANCE * 26, 0, [start_node], set())

    candidates : List[PartialPath] = []
    heappush(candidates, initial_path)
    cache = PathCache()

    i = 0
    best_distance = 100000
    best_path = None
    while len(candidates) > 0:
        path_to_extend = heappop(candidates)
        if path_to_extend.distance > best_distance:
            continue
        paths_to_add = expand_path(path_to_extend, cache)
        for path in paths_to_add:
            if len(path.keys) == 26 and path.distance < best_distance:
                best_distance = path.distance
                best_path = path
            else:
                heappush(candidates, path)

        if i % 50000 == 0:
            print(candidates[0].distance_estimate, len(candidates), len(cache._cache), len(candidates[0].path), "".join(map(lambda x: x.content, candidates[0].path)))
        i += 1

    best_path_str = ",".join(map(lambda x: x.content, best_path.path))

    return best_distance


def solve_part_1(puzzle_input):
    graph = generate_graph(puzzle_input)
    return collect_all_keys(graph)


@dataclass(order=True)
class Part2State:
    distance : int
    bots : List[Tuple[int]] = field(compare=False)
    keys : Set[str] = field(compare=False)

class Part2Cache:
    def __init__(self):
        self._cache = {}

    def _gen_cache_key(self, state : Part2State):
        return (tuple(state.bots), tuple(sorted(list(state.keys))))

    def add(self, state : Part2State):
        self._cache[self._gen_cache_key(state)] = state.distance

    def get(self, state : Part2State):
        return self._cache.get(self._gen_cache_key(state), 100000)

def expand_path_2(graphs : List[Graph], state : Part2State, cache : Part2Cache):
    if cache.get(state) <= state.distance:
        return []
    cache.add(state)

    keys = state.keys
    bots = state.bots
    new_states = []

    for i, graph in enumerate(graphs):
        bot = bots[i]
        seen = set()
        start_node = graph.get_node(bot[0], bot[1])
        seen.add(start_node)
        to_explore = set(start_node.neighbors)
        while len(to_explore) > 0:
            neighbor, leg_distance = to_explore.pop()

            if neighbor in seen:
                continue
            seen.add(neighbor)

            content = neighbor.content
            if content in DOORS and content.lower() not in keys:
                continue

            if content in KEYS and content not in keys:
                new_distance = state.distance + leg_distance
                new_keys = state.keys.copy()
                new_keys.add(content)
                new_bots = bots.copy()
                new_bots[i] = neighbor.coordinates
                new_states.append(Part2State(new_distance, new_bots, new_keys))
            else:
                for next_neighbor, next_leg_distance in neighbor.neighbors:
                    to_explore.add((next_neighbor, leg_distance+next_leg_distance))

    return new_states

def collect_all_keys_2(graphs):
    start_bots = [(39,39), (1,39), (39,1), (1,1)]
    start_state = Part2State(0, start_bots, set())

    candidates = []
    heappush(candidates, start_state)
    cache = Part2Cache()

    i = 0
    best_distance = 100000
    best_path = None
    while len(candidates) > 0:
        path_to_extend = heappop(candidates)
        if path_to_extend.distance > best_distance:
            continue
        paths_to_add = expand_path_2(graphs, path_to_extend, cache)
        for path in paths_to_add:
            if len(path.keys) == 26 and path.distance < best_distance:
                best_distance = path.distance
                best_path = path
            else:
                heappush(candidates, path)

        if i % 10000 == 0:
            print(candidates[0].distance, len(candidates), len(cache._cache), len(candidates[0].keys))
        i += 1

    return best_distance

def slice_2d(puzzle_input, x0, x1, y0, y1):
    result = []
    for j in range(y0, y1):
        result.append(puzzle_input[j][x0:x1])
    return result

def solve_part_2(puzzle_input):
    puzzle_input[39] = puzzle_input[39][0:39] + "@#@" + puzzle_input[39][42:]
    puzzle_input[40] = puzzle_input[40][0:39] + "###" + puzzle_input[40][42:]
    puzzle_input[41] = puzzle_input[41][0:39] + "@#@" + puzzle_input[41][42:]

    graphs = []
    grid0 = slice_2d(puzzle_input, 0, 41, 0, 41)
    graphs.append(generate_graph(grid0))
    grid1 = slice_2d(puzzle_input, 40, 81, 0, 41)
    graphs.append(generate_graph(grid1))
    grid2 = slice_2d(puzzle_input, 0, 41, 40, 81)
    graphs.append(generate_graph(grid2))
    grid3 = slice_2d(puzzle_input, 40, 81, 40, 81)
    graphs.append(generate_graph(grid3))

    return collect_all_keys_2(graphs)

def get_puzzle_input():
    puzzle_input = []
    with open("input.txt") as input_txt:
        for line in input_txt:
            puzzle_input.append(line.strip())
    return puzzle_input

if __name__ == "__main__":
    puzzle_input = get_puzzle_input()

    answer_1 = solve_part_1(puzzle_input)
    print(f"Part 1: {answer_1}")

    answer_2 = solve_part_2(puzzle_input)
    print(f"Part 2: {answer_2}")