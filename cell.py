from graphics import Point, Line


class Cell:
    def __init__(self, window):
        self.has_top_wall = True
        self.has_right_wall = True
        self.has_bottom_wall = True
        self.has_left_wall = True
        self._x1 = None
        self._y1 = None
        self._x2 = None
        self._y2 = None
        self._win = window

    def draw(self, x1, y1, x2, y2):
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2

        walls = []
        if self.has_top_wall:
            walls.append(Line(Point(x1, y2), Point(x2, y2)))
        if self.has_right_wall:
            walls.append(Line(Point(x2, y2), Point(x2, y1)))
        if self.has_bottom_wall:
            walls.append(Line(Point(x1, y1), Point(x2, y1)))
        if self.has_left_wall:
            walls.append(Line(Point(x1, y2), Point(x1, y1)))
        for wall in walls:
            self._win.draw_line(wall, "black")
