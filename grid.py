import math
from collections import defaultdict, deque
from enum import IntEnum, auto

from points import Cell, Position


class GridType(IntEnum):
    EMPTY = auto()
    RANDOM = auto()


class Grid:
    START_CELL = "S"
    EMPTY_CELL = " "
    OBSTACLE_CELL = "."
    SPECIAL_CELLS = set()
    GRID_SIZE = 5
    CELL_WRAPPER = r"[{}]"
    MASKS = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1),
    ]
    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

    VALID_MOVES = {
        LEFT: {
            ("-", "-"),
            ("-", "F"),
            ("-", "L"),
            ("J", "-"),
            ("J", "F"),
            ("J", "L"),
            ("7", "-"),
            ("7", "F"),
            ("7", "L"),
        },
        RIGHT: {
            ("-", "-"),
            ("-", "J"),
            ("-", "7"),
            ("L", "-"),
            ("L", "J"),
            ("L", "7"),
            ("F", "-"),
            ("F", "J"),
            ("F", "7"),
        },
        UP: {
            ("|", "|"),
            ("|", "F"),
            ("|", "7"),
            ("L", "|"),
            ("L", "F"),
            ("L", "7"),
            ("J", "|"),
            ("J", "F"),
            ("J", "7"),
        },
        DOWN: {
            ("|", "|"),
            ("|", "L"),
            ("|", "J"),
            ("F", "|"),
            ("F", "L"),
            ("F", "J"),
            ("7", "|"),
            ("7", "L"),
            ("7", "J"),
        },
    }

    @classmethod
    def get_start_cell(cls):
        return cls.START_CELL

    @classmethod
    def get_empty_cell(cls):
        return cls.EMPTY_CELL

    @classmethod
    def get_obstacle_cell(cls):
        return cls.OBSTACLE_CELL

    @classmethod
    def get_special_cells(cls):
        return cls.SPECIAL_CELLS

    @classmethod
    def get_grid_size(cls):
        return cls.GRID_SIZE

    def _get_empty_grid(self):
        size = self.get_grid_size()
        empty_cell = self.get_empty_cell()

        grid = [
            [empty_cell for col in range(size)]
            for row
            in range(size)
        ]

        return grid, size, size

    def _set_grid(self, which=GridType.EMPTY):
        if which == GridType.EMPTY:
            self.grid, self.rows, self.cols = self._get_empty_grid()

    def _get_random_grid(
        self,
        with_start_cell=False,
        with_empty_cells=False,
        with_obstacle_cells=False,
        with_special_cells=False,
        size=5,
    ):
        pass

    def __init__(self, grid=None):
        if grid is None:
            self._set_grid()
        else:
            self.grid = grid
            self.rows = self._get_n_rows(grid)
            self.cols = self._get_n_cols(grid)

    def _get_n_rows(self, grid):
        return len(grid)

    def _get_n_cols(self, grid):
        return len(grid[0])

    def is_valid_neighbour(self, origin, cell):
        return True

    def get_cell(self, row, col, strict=False):
        # if strict:
        #     assert 0 <= row < self.rows
        #     assert 0 <= col < self.cols
        # try:
        #     return self.grid[row][col]
        # except IndexError:
        #     return None
        try:
            return self.grid[row][col]
        except:
            return None

    def check_cell(self, row, col, what, strict=False):
        return self.get_cell(row, col, strict) == what

    def is_start_cell(self, row, col, strict=False):
        return self.check_cell(row, col, Grid.get_start_cell(), strict=strict)

    def _iterate_over_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                yield [Cell(row, col), self.get_cell(row, col)]

    def find_start_cell(self):
        for cell, sym in self._iterate_over_grid():
            if sym == self.get_start_cell():
                return cell

    def _get_mask_positions(self):
        return [
            Position.from_tuple(mask)
            for mask
            in self.MASKS
        ]

    def get_neighbours(self, r, c):
        origin = Cell(r, c)
        positions = self._get_mask_positions()
        neighbour_cells = [
            origin + pos
            for pos
            in positions
        ]
        return origin, neighbour_cells

    def get_valid_neighbours(self, r, c):
        origin, neighbour_cells = self.get_neighbours(r, c)
        return [
            (cell.as_tuple(), self.get_cell(*cell.as_tuple()))
            for cell
            in neighbour_cells
            if self.is_valid_neighbour(origin, cell)
        ]

    def is_inside_grid(self, row, col):
        if 0 <= row < self.rows:
            if 0 <= col < self.cols:
                return True
        return False

        # return (
        #     0 <= row < self.rows
        #     and
        #     0 <= col < self.cols
        # )

    def is_not_obstacle(self, row, col):
        return self.get_cell(row, col) != self.OBSTACLE_CELL

    def _is_valid_move(self, row, col):
        return all([
            self.is_inside_grid(row, col),
            self.is_not_obstacle(row, col),
        ])

    def dfs_grid(self, origin_cell):
        visited = set()

        def dfs(row, col):
            if not self._is_valid_move(row, col) or (row, col) in visited:
                return
            visited.add((row, col))

            dfs(row - 1, col)  # up
            dfs(row + 1, col)  # down
            dfs(row, col - 1)  # left
            dfs(row, col + 1)  # right

        dfs(*origin_cell.as_tuple())
        return visited

    def dfs_paths(self, origin_cell):
        paths = {}

        def dfs(row, col, path):
            if not self._is_valid_move(row, col) or (row, col) in set(path):
                return

            new_path = path + [(row, col)]

            paths[(row, col)] = (new_path, len(new_path) - 1)

            dfs(row - 1, col, new_path)
            dfs(row + 1, col, new_path)
            dfs(row, col - 1, new_path)
            dfs(row, col + 1, new_path)

        dfs(*origin_cell.as_tuple(), [])
        return paths

    def _can_move(self, current_value, next_value, direction):
        if current_value == self.START_CELL:
            return True
        return (current_value, next_value) in self.VALID_MOVES[direction]

    # def _can_move(self, current_value, next_value, direction):
    #     return (
    #         (
    #             direction == self.LEFT
    #             and current_value in {"-", "J", "7"}
    #             and next_value in {"-", "F", "L"}
    #         )
    #         or
    #         (
    #             direction == self.RIGHT
    #             and current_value in {"-", "L", "F"}
    #             and next_value in {"-", "J", "7"}
    #         )
    #         or
    #         (
    #             direction == self.UP
    #             and current_value in {"|", "L", "J"}
    #             and next_value in {"|", "F", "7"}
    #         )
    #         or
    #         (
    #             direction == self.DOWN
    #             and current_value in {"|", "F", "7"}
    #             and next_value in {"|", "L", "J"}
    #         )
    #     )

    # def _can_move(self, next_value, current_value, direction):
    #     if current_value == "S":
    #         return True
    #     elif direction == self.LEFT:
    #         return current_value in {"-", "J", "7"} and next_value in {"-", "F", "L"}
    #     elif direction == self.RIGHT:
    #         return current_value in {"-", "L", "F"} and next_value in {"-", "J", "7"}
    #     elif direction == self.UP:
    #         return current_value in {"|", "L", "J"} and next_value in {"|", "F", "7"}
    #     elif direction == self.DOWN:
    #         return current_value in {"|", "F", "7"} and next_value in {"|", "L", "J"}

    # def dfs_grid_with_comparison(self, origin_cell):
    #     paths = {}

    #     def dfs(row, col, path):
    #         if not self._is_valid_move(row, col) or (row, col) in set(path):
    #             return

    #         current_value = self.get_cell(row, col) if path else None
    #         if path and not self._can_move(current_value, self.get_cell(*path[-1])):
    #             return

    #         new_path = path + [(row, col)]

    #         paths[(row, col)] = (new_path, len(new_path))

    #         dfs(row - 1, col, new_path)
    #         dfs(row + 1, col, new_path)
    #         dfs(row, col - 1, new_path)
    #         dfs(row, col + 1, new_path)

    #     dfs(*origin_cell.as_tuple(), [])
    #     return paths

    # def dfs_grid_with_comparison(self, origin_cell):
    #     paths = {}
    #     stack = deque()
    #     stack.append((origin_cell.as_tuple(), []))  # (position, path)

    #     while stack:
    #         (row, col), path = stack.pop()
    #         if not self._is_valid_move(row, col) or (row, col) in set(path):
    #             continue

    #         current_value = self.get_cell(row, col) if path else None
    #         if path and not self._can_move(current_value, self.get_cell(*path[-1])):
    #             continue

    #         new_path = path + [(row, col)]
    #         paths[(row, col)] = (new_path, len(new_path) - 1)

    #         # Add neighbors to stack
    #         stack.extend([((row + dx, col + dy), new_path) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]])

    #     return paths

    def dfs_grid_with_comparison(self, origin_cell):
        paths = {}
        stack = deque()
        start_row, start_col = origin_cell.as_tuple()
        stack.append(((start_row, start_col), []))  # (position, path)

        while stack:
            (row, col), path = stack.pop()
            if not self._is_valid_move(row, col) or (row, col) in set(path):
                continue

            current_value = self.get_cell(row, col) if path else None

            for direction in self.DIRECTIONS:
                dx, dy = direction
                next_row, next_col = row + dx, col + dy
                next_value = self.get_cell(next_row, next_col)
                can_move = self._can_move(current_value, next_value, direction)
                if path and not can_move:
                    continue

                new_path = path + [(row, col)]
                paths[(row, col)] = (new_path, len(new_path))

                stack.append(((next_row, next_col), new_path))

        return paths

    def show_visited(self, visited):
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) in visited:
                    print("[x]", end="")
                else:
                    print("[ ]", end="")
            print()

    def __str__(self):
        flag = (
            hasattr(self, "CELL_WRAPPER")
            and isinstance(self.CELL_WRAPPER, str)
            and r"{}" in self.CELL_WRAPPER
        )

        s = ""
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                if flag:
                    s += self.CELL_WRAPPER.format(cell)
                else:
                    s += cell

            s += "\n"
        return s.strip()


class CustomGrid(Grid):
    SPECIAL_CELLS = {"|", "-", "J", "L", "F", "7"}
    ALLOWED_CELLS = SPECIAL_CELLS ^ {Grid.START_CELL}

    def is_valid_neighbour(self, origin, cell):
        cell = self.get_cell(*cell.as_tuple())
        return cell in grid.SPECIAL_CELLS

    @classmethod
    def _iterate_over_file(cls, filename):
        with open(filename) as f:
            for line in f:
                line = line.strip()
                yield line

    @classmethod
    def from_file(cls, filename):
        return [
            list(line)
            for line
            in cls._iterate_over_file(filename)
        ]


def manhattan_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return abs(x2 - x1) + abs(y2 - y1)


def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# EXAMPLE_GRID = [
#     [".", ".", "F", "7", "."],
#     [".", "F", "J", "|", "."],
#     ["S", "J", ".", "L", "7"],
#     ["|", "F", "-", "-", "J"],
#     ["L", "J", ".", ".", "."],
# ]
# grid = CustomGrid(EXAMPLE_GRID)
_input = CustomGrid.from_file("input/10.txt")
# print(_input[0])
grid = CustomGrid(_input)
# print(grid)
# print("=" * 15)
# print(grid.get_valid_neighbours(1, 1))
# print(grid.find_start_cell())
start_cell = grid.find_start_cell()
# print(start_cell)
# visited = grid.dfs_grid(start_cell)
# print(visited)
# print()
# grid.show_visited(visited)
# paths = grid.dfs_paths(start_cell)
# print(paths)
# for origin, (path, steps) in paths.items():
#     grid.show_visited(path)
#     print("Number of steps:", steps)

# max_so_far = 0
paths = grid.dfs_grid_with_comparison(start_cell)
# print([
#     grid.manhattan_distance(p[0][0], p[0][-1])
#     for p
#     in paths.values()
# ])

saved_paths = defaultdict(list)
for origin, (path, steps) in paths.items():
    # grid.show_visited(path)
    beg, end = path[0], path[-1]
    md = manhattan_distance(beg, end)
    saved_paths[md].append((path, steps))
    # if max_so_far < steps:
        # max_so_far = steps
    # print("Number of steps:", steps)
# print(max_so_far)

# paths = [p[0] for p in paths.values()]
# path = max(paths, key=lambda p: manhattan_distance(p[0], p[-1]))
# print(path)

best_path = None
max_ed = 0
max_steps = 0
for path, steps in saved_paths.get(max(saved_paths)):
    # grid.show_visited(path)
    ed = euclidean_distance(path[0], path[-1])
    if ed > max_ed:
        best_path = path
        max_ed = ed
        max_steps = steps
    # print("Number of steps:", steps)

grid.show_visited(best_path)
print(max_steps)

