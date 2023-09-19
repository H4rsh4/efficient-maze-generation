from Maze import Maze 

# Maze dimensions (ncols, nrows)
nx, ny = int(input("Maze Cols: ")), int(input("Maze Rows: "))
# Maze entry position
ix, iy = 0, 0

maze = Maze(nx, ny, ix, iy)
maze.generate_maze()
maze.find_shortest_path()
print("Generated maze:\n", maze.get_maze())

print("Path Directions : ", maze.get_maze_path_direction())

if input("press ENTER to print maze with path") =='' :
    print(maze.get_maze_path())  
