import unittest

from maze import Maze


class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        test_cases = [[1, 1], [1, 10], [10, 1], [10, 10]]
        for test in test_cases:
            num_cols = test[0]
            num_rows = test[1]
            m = Maze(0, 0, num_rows, num_cols, 10, 10)
            self.assertEqual(
                len(m._cells),
                num_cols,
            )
            self.assertEqual(
                len(m._cells[0]),
                num_rows,
            )

    def test_break_entrance_and_exit(self):
        test_cases = [[1, 1], [1, 10], [10, 1], [10, 10]]
        for test in test_cases:
            num_cols = test[0]
            num_rows = test[1]
            m = Maze(0, 0, num_rows, num_cols, 10, 10)
            self.assertFalse(m._cells[0][0].has_top_wall)
            self.assertFalse(m._cells[-1][-1].has_bottom_wall)

    def test_reset_cells_visited(self):
        test_cases = [[1, 1], [1, 10], [10, 1], [10, 10]]
        for test in test_cases:
            num_cols = test[0]
            num_rows = test[1]
            m = Maze(0, 0, num_rows, num_cols, 10, 10)
            for i in range(num_cols):
                for j in range(num_rows):
                    self.assertFalse(m._cells[i][j].visited)


if __name__ == "__main__":
    unittest.main()
