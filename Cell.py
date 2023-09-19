
class Cell:
    """
    Represents a cell in the maze.
    Attributes:
        x, y: coordinates
        walls: dictionary of walls
    """

    OPPOSITE_WALLS = {"N": "S", "S": "N", "E": "W", "W": "E"}

    def __init__(self, x, y):
        """Initialize the cell at (x,y) with all walls up."""
        self.x, self.y = x, y
        self.walls = {"N": True, "S": True, "E": True, "W": True}

    def all_walls_intact(self):
        """Check if all walls in the cell are intact."""
        return all(self.walls.values())

    def break_wall(self, adjacent_cell, wall_direction):
        """Break the wall between this cell and the adjacent cell."""
        self.walls[wall_direction] = False
        adjacent_cell.walls[Cell.OPPOSITE_WALLS[wall_direction]] = False
