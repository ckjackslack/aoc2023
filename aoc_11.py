import heapq
from collections import defaultdict, deque
from dataclasses import dataclass
from io import StringIO
from itertools import combinations

import numpy as np

from utils import (
    get_lines,
    get_lines_from_file,
)


@dataclass
class Point:
    x: int
    y: int

    @classmethod
    def from_tuple(cls, tup):
        assert len(tup) == 2
        assert all(type(e) == int for e in tup)
        return cls(*tup)

    def as_tuple(self):
        return (self.x, self.y)


EMPTY_SPACE = "."
EXAMPLE_GALAXY = StringIO("""
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
""".strip())
GALAXY = "#"


def iterate_over(grid):
    for row, line in enumerate(grid):
        for col, char in enumerate(line):
            yield (row, col), char


def get_empty_columns(grid):
    cols = {}
    for row, line in enumerate(grid):
        for col, char in enumerate(line):
            flag = char == EMPTY_SPACE
            if col not in cols:
                cols[col] = flag
            else:
                cols[col] &= flag
    return sorted(col for col in cols if cols[col])


def get_empty_rows(grid):
    rows = {}
    for row, line in enumerate(grid):
        flag = all(char == EMPTY_SPACE for char in line)
        if flag:
            rows[row] = flag
    return sorted(rows)


def get_galaxy_positions(grid, wrapper=None):
    return [
        (
            wrapper(pos)
            if wrapper is not None
            else pos
        )
        for pos, char
        in iterate_over(grid)
        if char == GALAXY
    ]


def make_empty_row(row_size):
    return "".join(EMPTY_SPACE for _ in range(row_size))


def gravitational_expand(galaxy):
    to_expand_rows = get_empty_rows(galaxy)
    to_expand_columns = get_empty_columns(galaxy)

    empty_row = make_empty_row(len(galaxy[0]))

    for offset, row in enumerate(to_expand_rows):
        galaxy.insert(row + offset, empty_row)

    for i, _ in enumerate(galaxy):
        for offset, col in enumerate(to_expand_columns):
            col += offset
            extended_row = galaxy[i][:col] + EMPTY_SPACE + galaxy[i][col:]
            galaxy[i] = extended_row

    return galaxy


def bfs_shortest_path(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    queue = deque([(start, [start])])
    visited = set([start])

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == goal:
            return path

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_x, next_y = x + dx, y + dy
            if 0 <= next_x < rows and 0 <= next_y < cols and (next_x, next_y) not in visited:
                queue.append(((next_x, next_y), path + [(next_x, next_y)]))
                visited.add((next_x, next_y))

    return None


def heuristic(a, b):
    # AKA Manhattan distance
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def a_star(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            tentative_g_score = g_score[current] + 1
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    if neighbor not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None


def dijkstra(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    cost_so_far = {start: 0}

    while open_set:
        current_cost, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            new_cost = current_cost + 1
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    came_from[neighbor] = current
                    cost_so_far[neighbor] = new_cost
                    heapq.heappush(open_set, (new_cost, neighbor))

    return None


def display(grid):
    for line in grid:
        for char in line:
            print(char, end="")
        print()


def get_sum_of_shortest_path_between_galaxies(it, strategy='bfs'):
    expanded_galaxy = gravitational_expand(it)
    galaxy_positions = get_galaxy_positions(
        expanded_galaxy,
        wrapper=Point.from_tuple,
    )

    s = 0
    combs = combinations(galaxy_positions, r=2)  # 91806
    for p1, p2 in combs:
        args = expanded_galaxy, p1.as_tuple(), p2.as_tuple()
        if strategy == 'bfs':
            result = len(bfs_shortest_path(*args)) - 1
        elif strategy == 'astar':
            result = len(a_star(*args))
        elif strategy == 'dijkstra':
            result = len(dijkstra(*args))
        else:
            # unknown
            result = 0
        s += result
    return s


def calculate_distance(grid, cell1, cell2):
    return heuristic(cell1, cell2)


def floyd_warshall(grid, occupied_cells):
    num_cells = len(occupied_cells)
    dist_matrix = np.full((num_cells, num_cells), np.inf)

    np.fill_diagonal(dist_matrix, 0)

    for i, cell1 in enumerate(occupied_cells):
        for j, cell2 in enumerate(occupied_cells):
            if i != j:
                dist_matrix[i][j] = calculate_distance(grid, cell1, cell2)

    for k in range(num_cells):
        for i in range(num_cells):
            for j in range(num_cells):
                if dist_matrix[i][k] + dist_matrix[k][j] < dist_matrix[i][j]:
                    dist_matrix[i][j] = dist_matrix[i][k] + dist_matrix[k][j]

    return dist_matrix


def sum_of_all_shortest_paths(grid, occupied_cells):
    dist_matrix = floyd_warshall(grid, occupied_cells)

    cell_to_index = {cell: index for index, cell in enumerate(occupied_cells)}

    total_distance = 0
    for i, cell1 in enumerate(occupied_cells):
        for j, cell2 in enumerate(occupied_cells):
            if i != j:
                idx1 = cell_to_index[cell1]
                idx2 = cell_to_index[cell2]
                total_distance += dist_matrix[idx1][idx2]

    return total_distance


def calculate(grid):
    positions = get_galaxy_positions(grid)
    return sum_of_all_shortest_paths(grid, positions)


def main():
    # it = list(get_lines("input/11.txt"))
    it = list(get_lines_from_file(EXAMPLE_GALAXY))
    # print(get_sum_of_shortest_path_between_galaxies(it))

    print(int(calculate(gravitational_expand(it)) // 2))


if __name__ == "__main__":
    main()
