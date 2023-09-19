from collections import deque
import random
from Cell import Cell

DIRECTIONS = [("W", (-1, 0)), ("E", (1, 0)), ("S", (0, 1)), ("N", (0, -1))]

class Maze:
    def __init__(self, nx, ny, entry_x=0, entry_y=0):
        """Initialize a maze grid with nx * ny cells."""
        self.nx, self.ny = nx, ny
        self.ix, self.iy = entry_x, entry_y
        self.cells = []
        self.shortest_path = None

        # Create the maze grid
        for x in range(nx):
            column = []
            for y in range(ny):
                column.append(Cell(x, y))
            self.cells.append(column)

    def get_cell_at(self, x, y):
        """Get the cell at coordinates (x, y)."""
        return self.cells[x][y]

    def find_unvisited_neighbors(self, cell):
        """Find unvisited neighbors of a cell."""
        neighbors = []
        for direction, (dx, dy) in DIRECTIONS:
            new_x, new_y = cell.x + dx, cell.y + dy
            if (0 <= new_x < self.nx) and (0 <= new_y < self.ny):
                neighbor = self.get_cell_at(new_x, new_y)
                if neighbor.all_walls_intact():
                    neighbors.append((direction, neighbor))
        return neighbors

    def find_accessible_neighbors(self, cell):
        """Find accessible neighbors that can be moved to."""
        accessible_neighbors = []
        for direction, (dx, dy) in DIRECTIONS:
            new_x, new_y = cell.x + dx, cell.y + dy
            if (0 <= new_x < self.nx) and (0 <= new_y < self.ny):
                neighbor = self.get_cell_at(new_x, new_y)
                if not cell.walls[direction]:
                    accessible_neighbors.append((direction, neighbor))
        return accessible_neighbors

    def generate_maze(self):
        """Generate the maze."""
        n = self.nx * self.ny
        cell_stack = []
        current_cell = self.get_cell_at(self.ix, self.iy)
        # Total number of visited cells during maze construction.
        nv = 1

        while nv < n:
            neighbours = self.find_unvisited_neighbors(current_cell)
            if not neighbours:
                # back tracking due to deadend.
                current_cell = cell_stack.pop()
                continue

            # Choose a random neighbour and move to it.
            direction, next_cell = random.choice(neighbours)
            current_cell.break_wall(next_cell, direction)
            cell_stack.append(current_cell)
            current_cell = next_cell
            nv += 1

    def find_shortest_path(self):
        """Find the shortest path from (ix, iy) to (nx-1, ny-1) using BFS."""
        start = self.get_cell_at(self.ix, self.iy)
        end = self.get_cell_at(self.nx - 1, self.ny - 1)
        queue = deque([(start, [])])  # (cell, path up to this cell)
        visited = set()

        while queue:
            current_cell, path = queue.popleft()

            if current_cell == end:
                self.spath = path + [current_cell]
                return path + [current_cell]

            if current_cell in visited:
                continue

            visited.add(current_cell)

            for direction, neighbour in self.find_accessible_neighbors(current_cell):
                queue.append((neighbour, path + [current_cell]))

        return None

    def get_maze(self):
        """Print the maze in ASCII."""
        maze_rows = ["_" * self.nx * 4]
        for y in range(self.ny):
            maze_row = ["|"]
            for x in range(self.nx):
                if self.cells[x][y].walls["E"] and self.cells[x][y].walls["S"]:
                    maze_row.append("___|")
                elif self.cells[x][y].walls["E"] and not self.cells[x][y].walls["S"]:
                    maze_row.append("   |")
                elif not self.cells[x][y].walls["E"] and self.cells[x][y].walls["S"]:
                    maze_row.append("____")
                else:
                    maze_row.append("    ")
            maze_rows.append("".join(maze_row))
        return "\n".join(maze_rows)

    def get_maze_path(self):
        """Print the maze along with path in ASCII."""
        path = self.spath
        if path:
            maze_rows = ["_" * self.nx * 4]
            for y in range(self.ny):
                maze_row = ["|"]
                for x in range(self.nx):
                    if self.cells[x][y].walls["E"] and self.cells[x][y].walls["S"]:
                        maze_row.append("___|") if not self.cells[x][
                            y
                        ] in path else maze_row.append("_._|")
                    elif self.cells[x][y].walls["E"] and not self.cells[x][y].walls["S"]:
                        maze_row.append("   |") if not self.cells[x][
                            y
                        ] in path else maze_row.append(" . |")
                    elif not self.cells[x][y].walls["E"] and self.cells[x][y].walls["S"]:
                        maze_row.append("____") if not self.cells[x][
                            y
                        ] in path else maze_row.append("_.__")
                    else:
                        maze_row.append("    ") if not self.cells[x][
                            y
                        ] in path else maze_row.append("  . ")
                maze_rows.append("".join(maze_row))
        return ("\n".join(maze_rows))
    def get_maze_path_direction(self):
        path = self.spath
        res = ''
        prev = (0, 0)
        if path:
            for cell in path[1:]:
                if cell.x > prev[0]:
                    res+='E'
                elif cell.x < prev[0]:
                    res+='W'
                elif cell.y > prev[1]:
                    res+='S'
                elif cell.y < prev[1]:
                    res+='N'
                prev = (cell.x, cell.y)
        else:
            res="No path found"
        return res