import random


class Line:
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

# Esta clase representa una fila.


class Row(Line):
    def __init__(self, values):
        super().__init__(values)

# Esta clase representa una columna.


class Col(Line):
    def __init__(self, values):
        super().__init__(values)

# Esta clase representa una subcuadrícula, hecha de filas y columnas.


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

    def is_valid(self, num, pos):
        # Verifica si un número dado puede ser colocado en la columna, fila y subgrid
        for i in range(3):
            if self.grid[pos[0]][i] == num and pos[1] != i:
                return False

        for i in range(3):
            if self.grid[i][pos[1]] == num and pos[0] != i:
                return False

        subgrid_x = pos[1] // 3
        subgrid_y = pos[0] // 3

        for i in range(subgrid_y * 3, subgrid_y * 3 + 3):
            for j in range(subgrid_x * 3, subgrid_x * 3 + 3):
                if self.grid[i][j] == num and (i, j) != pos:
                    return False

        return True

    def find_empty(self):
        # Encuentra una celda vacía en la subcuadrícula
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == 0:
                    return (i, j)  # row, col
        return None

# Esta clase representa un Sudoku, que es una subcuadrícula.


class Sudoku(Subgrid):
    def __init__(self, grid=None):
        if grid:
            if len(grid) != 9 or any(len(row) != 9 for row in grid):
                raise ValueError("Sudoku grid must be a 9x9 grid.")
            self._grid = grid
        else:
            # Crea una cuadrícula vacía
            self._grid = [[0 for _ in range(9)] for _ in range(9)]
        self.size = 9
        self.subgrids = [[Subgrid([self._grid[r + i][c:c + 3] for i in range(3)])
                          for c in range(0, 9, 3)] for r in range(0, 9, 3)]

    @property
    def grid(self):
        return self._grid

    @grid.setter
    def grid(self, new_grid):
        if len(new_grid) != 9 or any(len(row) != 9 for row in new_grid):
            raise ValueError("Grid must be a 9x9 grid.")
        self._grid = new_grid

    def is_valid(self, num, pos):
        # Verifica si un número dado puede ser colocado en la columna, fila y subgrid
        for i in range(9):
            if self.grid[pos[0]][i] == num and pos[1] != i:
                return False

        for i in range(9):
            if self.grid[i][pos[1]] == num and pos[0] != i:
                return False

        subgrid_x = pos[1] // 3
        subgrid_y = pos[0] // 3

        for i in range(subgrid_y * 3, subgrid_y * 3 + 3):
            for j in range(subgrid_x * 3, subgrid_x * 3 + 3):
                if self.grid[i][j] == num and (i, j) != pos:
                    return False

        return True

    def find_empty(self):
        # Encuentra una celda vacía en la cuadrícula
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return (i, j)  # row, col
        return None

    def solve(self):
        # Usa backtracking para resolver el Sudoku
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

    def generate_sudoku(self, clues=20):
        # Rellena la cuadrícula completamente
        self._fill_grid()

        # Elimina valores de la cuadrícula para crear un puzzle
        self._remove_numbers(clues)

    def _fill_grid(self):
        # Rellena la cuadrícula de Sudoku usando backtracking
        find = self.find_empty()
        if not find:
            return True  # La cuadrícula está completamente llena
        else:
            row, col = find

        # Intenta insertar números del 1 al 9 de forma aleatoria
        nums = list(range(1, 10))
        random.shuffle(nums)
        for num in nums:
            if self.is_valid(num, (row, col)):
                self.grid[row][col] = num

                if self._fill_grid():
                    return True

                # Resetea la celda si no es válida más adelante
                self.grid[row][col] = 0

        return False  # Triggera backtracking

    def _remove_numbers(self, clues):
        # Remueve números de la cuadrícula para dejar solo las pistas dadas
        total_cells = 81
        cells_to_remove = total_cells - clues

        while cells_to_remove > 0:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.grid[row][col] != 0:
                # Verifica que eliminar este número no haga el Sudoku irresoluble
                backup = self.grid[row][col]
                self.grid[row][col] = 0

                # Si no es solucionable, vuelve a colocar el número
                grid_copy = [row.copy() for row in self.grid]
                if not Sudoku(grid_copy).solve():
                    self.grid[row][col] = backup
                else:
                    cells_to_remove -= 1
