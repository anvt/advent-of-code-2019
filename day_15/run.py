from intcode import Computer


WALL = 0
SUCCESSFUL_MOVE = 1
OXYGEN = 2

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4


def read(file):
    with open(file, "r") as f:
        return [int(i) for i in f.readline().split(",")]


def get_opposite(move):
    return {NORTH: SOUTH, SOUTH: NORTH, WEST: EAST, EAST: WEST}.get(move)


def make_move(position, direction):
    moves = {NORTH: (0, 1), SOUTH: (0, -1), WEST: (-1, 0), EAST: (1, 0)}
    return tuple(map(sum, zip(position, moves.get(direction))))


def get_neighbours(pos):
    return [make_move(pos, direction) for direction in range(1, 5)]


def get_ship_map():
    robot = Computer(read("input.txt"))
    pos = (0, 0)
    ship_map = {}
    moves = []

    # contains directions (value) we haven't attempted for each
    # coordinate (key)
    unexplored = {}

    while True:
        ship_map[pos] = SUCCESSFUL_MOVE

        if pos not in unexplored:
            unexplored[pos] = [1, 2, 3, 4]

        if unexplored[pos]:
            back_tracking = False
            move = unexplored[pos].pop()
        else:
            back_tracking = True
            prev = moves.pop()
            move = get_opposite(prev)

        robot.add_input(move)
        status = robot.run()

        if status == SUCCESSFUL_MOVE:
            pos = make_move(pos, move)

            if not back_tracking:
                moves.append(move)

        elif status == OXYGEN:
            ship_map[pos] = OXYGEN
            return ship_map


def bfs(graph, start, target):
    queue = [[start]]
    visited = set()

    while queue:
        path = queue.pop(0)
        vertex = path[-1]

        if graph.get(vertex) == target or vertex == target:
            return len(path)

        if vertex in visited:
            continue

        visited.add(vertex)
        for neighbour in get_neighbours(vertex):
            if graph.get(vertex, 0) == 1:
                new_path = path.copy()
                new_path.append(neighbour)
                queue.append(new_path)


def part_one():
    ship = get_ship_map()
    return bfs(ship, start=(0, 0), target=OXYGEN)


def part_two():
    ship = get_ship_map()
    oxygen_location = None

    for coordinate in ship:
        if ship[coordinate] == OXYGEN:
            oxygen_location = coordinate

    return max(bfs(ship, coordinate, oxygen_location) for coordinate in ship)
