import time
import random

from cell import Cell


class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None,
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._cells = []
        self._win = win
        self._done_breaking = False

        if seed is not None:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()
        self.solve()

    def _create_cells(self):
        # TODO Rewrite the list comprehension
        self._cells = [
            [Cell(self._win) for _ in range(self._num_rows)]
            for _ in range(self._num_cols)
        ]
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _cell_exists(self, i, j):
        return 0 <= i < self._num_cols and 0 <= j < self._num_rows

    def get_valid_moves(self, i, j):
        directions = [
            (i + 1, j, "right"),
            (i - 1, j, "left"),
            (i, j + 1, "down"),
            (i, j - 1, "up"),
        ]
        valid_moves = []

        for new_i, new_j, direction in directions:
            if self._cell_exists(new_i, new_j):
                cell = self._cells[i][j]
                target_cell = self._cells[new_i][new_j]
                if not target_cell.visited:
                    if direction == "right" and not cell.has_right_wall:
                        valid_moves.append([new_i, new_j])
                    elif direction == "left" and not cell.has_left_wall:
                        valid_moves.append([new_i, new_j])
                    elif direction == "down" and not cell.has_bottom_wall:
                        valid_moves.append([new_i, new_j])
                    elif direction == "up" and not cell.has_top_wall:
                        valid_moves.append([new_i, new_j])

        return valid_moves

    def _draw_cell(self, i, j):
        if self._win is None:
            return

        def get_coords():
            x1 = self._x1 + self._cell_size_x * i
            y1 = self._y1 + self._cell_size_y * j
            x2 = x1 + self._cell_size_x
            y2 = y1 + self._cell_size_y
            return x1, y1, x2, y2

        c = self._cells[i][j]
        c.draw(*get_coords())
        self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.01)
        pass

    def _break_entrance_and_exit(self):
        ent = self._cells[0][0]
        exit = self._cells[-1][-1]
        ent.has_top_wall = False
        exit.has_bottom_wall = False
        ent.draw(ent._x1, ent._y1, ent._x2, ent._y2)
        exit.draw(exit._x1, exit._y1, exit._x2, exit._y2)

    def _get_rand_direction(self, i, j):
        valid_dirs = {
            0: {
                "exists": self._cell_exists(i + 1, j),
                "direction": ["right", [i + 1, j]],
            },
            1: {
                "exists": self._cell_exists(i - 1, j),
                "direction": ["left", [i - 1, j]],
            },
            2: {
                "exists": self._cell_exists(i, j + 1),
                "direction": ["down", [i, j + 1]],
            },
            3: {
                "exists": self._cell_exists(i, j - 1),
                "direction": ["up", [i, j - 1]],
            },
        }

        unvisited_dirs = [
            dir["direction"]
            for dir in valid_dirs.values()
            if dir["exists"]
            and not self._cells[dir["direction"][1][0]][dir["direction"][1][1]].visited
        ]

        if not unvisited_dirs:
            return None

        return random.choice(unvisited_dirs)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            d = self._get_rand_direction(i, j)

            if d is None:
                self._draw_cell(i, j)
                break

            if d[0] == "right":
                self._cells[i][j].has_right_wall = False
                self._cells[i + 1][j].has_left_wall = False
                self._break_walls_r(i + 1, j)
            elif d[0] == "left":
                self._cells[i][j].has_left_wall = False
                self._cells[i - 1][j].has_right_wall = False
                self._break_walls_r(i - 1, j)
            elif d[0] == "down":
                self._cells[i][j].has_bottom_wall = False
                self._cells[i][j + 1].has_top_wall = False
                self._break_walls_r(i, j + 1)
            elif d[0] == "up":
                self._cells[i][j].has_top_wall = False
                self._cells[i][j - 1].has_bottom_wall = False
                self._break_walls_r(i, j - 1)

    def _reset_cells_visited(self):
        for i in range(len(self._cells)):
            for j in range(len(self._cells[i])):
                self._cells[i][j].visited = False

    def solve(self):
        self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        cell = self._cells[i][j]
        cells = self._cells
        cell.visited = True

        if cell == cells[-1][-1]:
            return True

        valid_moves = self.get_valid_moves(i, j)

        for move in valid_moves:
            new_i, new_j = move
            target_cell = cells[new_i][new_j]

            cell.draw_move(target_cell)

            if self._solve_r(new_i, new_j):
                return True
            else:
                cell.draw_move(target_cell, undo=True)
        cell.visited = False
        return False
