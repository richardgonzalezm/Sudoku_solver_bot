class Grid:
    def __init__(self, values):
        self._values = values

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, new_values):
        if len(new_values) != len(self._values):
            raise ValueError(
                "New values must have the same length as the original values.")
        self._values = new_values


class Row(Grid):
    def __init__(self, values):
        super().__init__(values)


class Col(Grid):
    def __init__(self, values):
        super().__init__(values)


class Subgrid:
    def __init__(self, grid):
        self._grid = grid
        self.rows = [Row(row) for row in grid]
        self.cols = [Col([grid[r][c] for r in range(3)]) for c in range(3)]

    @property
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self, new_grid):
        if len(new_grid) != 3 or any(len(row) != 3 for row in new_grid):
            raise ValueError("Subgrid must be a 3x3 grid.")
        self._grid = new_grid


class Sudoku(Subgrid):
    def __init__(self, grid):
        if len(grid) != 9 or any(len(row) != 9 for row in grid):
            raise ValueError("Sudoku grid must be a 9x9 grid.")
        super().__init__(grid)
        self.size = 9

    def is_valid(self, num, pos):
        # Check row
        for i in range(self.size):
            if self.grid[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(self.size):
            if self.grid[i][pos[1]] == num and pos[0] != i:
                return False

        # Check subgrid
        subgrid_x = pos[1] // 3
        subgrid_y = pos[0] // 3

        for i in range(subgrid_y * 3, subgrid_y * 3 + 3):
            for j in range(subgrid_x * 3, subgrid_x * 3 + 3):
                if self.grid[i][j] == num and (i, j) != pos:
                    return False

        return True

    def find_empty(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == 0:
                    return (i, j)  # row, col
        return None

    def solve(self):
        find = self.find_empty()
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.is_valid(i, (row, col)):
                self.grid[row][col] = i

                if self.solve():
                    return True

                self.grid[row][col] = 0

        return False

    def print_grid(self):
        for i in range(self.size):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - - -")

            for j in range(self.size):
                if j % 3 == 0 and j != 0:
                    print(" | ", end="")

                if j == 8:
                    print(self.grid[i][j])
                else:
                    print(str(self.grid[i][j]) + " ", end="")


if __name__ == "__main__":
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    sudoku = Sudoku(board)
    sudoku.print_grid()
    print("\nSolving...\n")
    sudoku.solve()
    sudoku.print_grid()
