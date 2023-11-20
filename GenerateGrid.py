import numpy as np
import random
import math

#initialize the grid
shape = (20,20)
Grid = np.zeros(shape=shape)

#set the goal rewards
lightReward = 100
darkReward = 10


#set the start state somewhere in the between
start_state = (math.floor((Grid.shape[0]-1)/2),0)


# randomly initialize cells as obstacles with a probability

prob = 0.2

def obstacleMap(Grid,start_state,light_goal,dark_goal):
    for i in range(len(Grid)):
        for j in range(len(Grid)):
            if (i,j)!= start_state and (i,j)!= light_goal and (i,j)!=dark_goal :
                r = random.uniform(0,100)
                r/=100
                if(r<=prob):
                    Grid[i][j] = -1
    return Grid



# we check all the valid neighbours of the current position
def validNeighbourBFS(Grid, node):
    neighbors = []
    
    if node[0]+1 >= 0 and node[0]+1 < len(Grid) and Grid[node] != -1:
        neighbors.append((node[0]+1, node[1]))
    if node[0]-1 >= 0 and node[0]-1 < len(Grid) and Grid[node] != -1:
        neighbors.append((node[0]-1, node[1]))    
    if node[1]+1 >= 0 and node[1]+1 < len(Grid) and Grid[node] != -1:
        neighbors.append((node[0], node[1]+1))
    if node[1]-1 >= 0 and node[1]-1 < len(Grid) and Grid[node] != -1:
        neighbors.append((node[0], node[1]-1))
    
    return neighbors



# running BFS to check for valid path from start to light
def BFS(graph, start):
    visited = set()
    queue = []  
    queue.append(start)
    visited.add(start)
    path = []
    while queue:
        current = queue.pop(0)
        path.append(current)
        
        # Add neighbors of the current node to the queue
        for neighbor in validNeighbourBFS(Grid,current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return path
    

#assign dark and light goal states
light_goal = (Grid.shape[0]-1,Grid.shape[1]-1)
dark_goal = (0,Grid.shape[0]-1)
Grid[light_goal] = 100
Grid[dark_goal] = 10

#initialize obstacle map
Grid = obstacleMap(Grid,start_state,light_goal,dark_goal)

#check if a path exists to the light goal otherwise regenerate obstacles
path = BFS(Grid,start_state)
while(light_goal not in path and dark_goal not in path):
    Grid = obstacleMap(Grid,start_state,light_goal,dark_goal)
    path_light = BFS(Grid,start_state)

#print grid
print(Grid)

#enemy placement in the grid
def enemy_placement(Grid,start_state,light_goal,dark_goal):
    pass