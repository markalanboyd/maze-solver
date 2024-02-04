from graphics import Point, Line


class Cell:
    def __init__(self, window=None):
        self.has_top_wall = True
        self.has_right_wall = True
        self.has_bottom_wall = True
        self.has_left_wall = True
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None
        self._win = window
        self.visited = False

    def __repr__(self):
        return f"Cell at {hex(id(self))}"

    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return

        def draw_conditionally(wall_lines):
            for _, wall_value in wall_lines.items():
                color = "black"
                if not wall_value["exists"]:
                    color = "white"
                self._win.draw_line(wall_value["line"], color)

        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2

        wall_lines = {
            "top": {
                "exists": self.has_top_wall,
                "line": Line(Point(x1, y1), Point(x2, y1)),
            },
            "right": {
                "exists": self.has_right_wall,
                "line": Line(Point(x2, y2), Point(x2, y1)),
            },
            "bottom": {
                "exists": self.has_bottom_wall,
                "line": Line(Point(x1, y2), Point(x2, y2)),
            },
            "left": {
                "exists": self.has_left_wall,
                "line": Line(Point(x1, y2), Point(x1, y1)),
            },
        }

        draw_conditionally(wall_lines)

    def draw_move(self, to_cell, undo=False):
        if self._win is None:
            return

        def get_center_point(x1, y1, x2, y2):
            x = x1 + ((x2 - x1) * 0.5)
            y = y1 + ((y2 - y1) * 0.5)
            return Point(x, y)

        color = "red"
        if undo:
            color = "white"

        self_center = get_center_point(self._x1, self._y1, self._x2, self._y2)
        to_cell_center = get_center_point(
            to_cell._x1, to_cell._y1, to_cell._x2, to_cell._y2
        )
        line = Line(self_center, to_cell_center)

        self._win.draw_line(line, color)
