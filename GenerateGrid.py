import numpy as np
import random

#initialize the grid
shape = (20,20)
Grid = np.zeros(shape=shape)

#set the goal rewards
lightReward = 100
darkReward = 10


#set the start state

start_state = tuple((np.random.randint(len(Grid[0])),np.random.randint(len(Grid[1]))))



# randomly initialize cells as obstacles with a probability

prob = 0.2

def obstacleMap(Grid):
    for i in range(len(Grid)):
        for j in range(len(Grid)):
            if (i,j)!= start_state:
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
    

Grid = obstacleMap(Grid)

valid_states = BFS(Grid,start_state)

#set light goal
light_goal = np.random.randint(len(valid_states))
while(valid_states[light_goal] == start_state):
    light_goal = np.random.randint(len(valid_states))

Grid[valid_states[light_goal]] = 10


#We define manhattan distance function to keep the dark and light goal wide apart
def manhattanDistance(x,y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


#set dark goal
dark_goal = np.random.randint(len(valid_states))
M = manhattanDistance(valid_states[dark_goal],valid_states[light_goal])
print(M)
while M<1.5*len(Grid):
    dark_goal = np.random.randint(len(valid_states))

Grid[valid_states[dark_goal]] = 100

    

print(Grid)
print(start_state)






