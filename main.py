import time

from graphics import Window
from maze import Maze


def main():
    win = Window(800, 600)

    Maze(20, 20, 20, 20, 20, 20, win, time.time())

    win.wait_for_close()


main()
