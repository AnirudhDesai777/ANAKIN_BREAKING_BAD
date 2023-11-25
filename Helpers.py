'''Helper functions for the grid environment, Q-learning and NLP'''
import numpy as np
import matplotlib.pyplot as plt


# we check all the valid neighbours of the current position for BFS
def validNeighbourBFS(Grid, node):
    neighbors = []
    
    if node[0]+1 >= 0 and node[0]+1 < len(Grid) and Grid[node[0]+1][node[1]] != -1:
        neighbors.append((node[0]+1, node[1]))
    if node[0]-1 >= 0 and node[0]-1 < len(Grid) and Grid[node[0]-1][node[1]] != -1:
        neighbors.append((node[0]-1, node[1]))    
    if node[1]+1 >= 0 and node[1]+1 < len(Grid) and Grid[node[0]][node[1]+1] != -1:
        neighbors.append((node[0], node[1]+1))
    if node[1]-1 >= 0 and node[1]-1 < len(Grid) and Grid[node[0]][node[1]-1] != -1:
        neighbors.append((node[0], node[1]-1))
    
    return neighbors

def validMovesASTAR(Grid, node, goal):
    neighbors = []
    
    if node[0]+1 >= 0 and node[0]+1 < len(Grid) and Grid[node[0]+1][node[1]] != -1 and (node[0]+1,node[1])!=goal:
        neighbors.append((node[0]+1, node[1]))
    if node[0]-1 >= 0 and node[0]-1 < len(Grid) and Grid[node[0]-1][node[1]] != -1 and (node[0]-1,node[1])!=goal:
        neighbors.append((node[0]-1, node[1]))    
    if node[1]+1 >= 0 and node[1]+1 < len(Grid) and Grid[node[0]][node[1]+1] != -1 and (node[0],node[1]+1)!=goal:
        neighbors.append((node[0], node[1]+1))
    if node[1]-1 >= 0 and node[1]-1 < len(Grid) and Grid[node[0]][node[1]-1] != -1 and (node[0],node[1]-1)!=goal:
        neighbors.append((node[0], node[1]-1))
    
    return neighbors

def visualize_grid(grid, start_state, light_goal, dark_goal, light_path, dark_path=None):
    '''
    Helper function to visualize the grid
    For development purposes only
    need to do better visualization for final
    '''
    # Define different elements in the grid
    FREE_SPACE = 0
    OBSTACLE = 1
    ENEMY = 2
    START_STATE = 3
    LIGHT_GOAL = 4
    DARK_GOAL = 5
    LIGHT_PATH = 6
    DARK_PATH = 7

    # Create a numeric grid for visualization
    vis_grid = np.full(grid.shape, FREE_SPACE)
    vis_grid[grid == -1] = OBSTACLE  # Obstacles
    vis_grid[grid == -2] = ENEMY     # Enemies
    vis_grid[light_goal] = LIGHT_GOAL
    vis_grid[dark_goal] = DARK_GOAL
    vis_grid[start_state] = START_STATE
    for pos in light_path[1]:
        vis_grid[pos] = LIGHT_PATH
    if dark_path:
        for pos in dark_path:
            vis_grid[pos] = DARK_PATH

    # Define the color map
    cmap = plt.cm.colors.ListedColormap(['white', 'black', 'red', 'green', 'yellow', 'blue', 'lightgreen', 'lightblue'])
    bounds = [FREE_SPACE, OBSTACLE, ENEMY, START_STATE, LIGHT_GOAL, DARK_GOAL, LIGHT_PATH, DARK_PATH, DARK_PATH+1]
    norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)

    # Create the plot
    fig, ax = plt.subplots()
    ax.imshow(vis_grid, cmap=cmap, norm=norm)
    # Draw gridlines
    ax.set_xticks(np.arange(-.5, len(grid[0]), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(grid), 1), minor=True)
    ax.grid(which="minor", color="black", linestyle='-', linewidth=2)
    ax.tick_params(which="minor", size=0)

    # Remove major ticks and labels
    ax.tick_params(which="major", bottom=False, left=False, labelbottom=False, labelleft=False)

    plt.show()


def RewardMatrix(matrix):
    # Iterate over each element in the matrix
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i][j] == -2:
                matrix[i][j] = -50
            elif matrix[i][j] == -1:
                matrix[i][j] = -100
            elif matrix[i][j] == 0:
                matrix[i][j] = -1
            elif matrix[i][j] == 10:
                matrix[i][j] = -10
    return matrix