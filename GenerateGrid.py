import numpy as np
import random
import math
import heapq
from Helpers import validNeighbourBFS, validMovesASTAR
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

#Heuristic function for A*
def H_score(node, goal, n):  
    heuristic = (abs(node[0] - goal[0]) + abs(node[1] - goal[1])) / (n - 1)
    return heuristic

#finding shortest path from start state to light goal using A*
def lightPathASTAR(Grid, start,light_goal,dark_goal):

    g = {}
    f = {}
    openList = []
    closeList = []
    parent = {}

    for i in range(len(Grid)):
        for j in range(len(Grid)):
            g[(i, j)] = np.inf

    g[start] = 0
    f[start] = H_score(start, light_goal, len(Grid))
    heapq.heappush(openList, (f[start], start))

    while openList:
        currentNode = heapq.heappop(openList)[1]

        if currentNode in closeList:
            continue

        closeList.append(currentNode)

        if currentNode == light_goal:
            path = []
            while currentNode in parent:
                path.append(currentNode)
                currentNode = parent[currentNode]
            path.append(start)
            path.reverse()
            return len(path) - 1, path

        for neighbor in validMovesASTAR(Grid, currentNode,dark_goal):
            new_g = g[currentNode] + 1

            if new_g < g[neighbor]:
                parent[neighbor] = currentNode
                g[neighbor] = new_g
                f[neighbor] = g[neighbor] + H_score(neighbor, light_goal, len(Grid))
                heapq.heappush(openList, (f[neighbor], neighbor))
    return None, []

light_path = lightPathASTAR(Grid,start_state,light_goal,dark_goal)
print(light_path)

#initialize enemies in the path except for the path given by ASTAR to light.
def initalize_enemies(Grid,start_state,light_goal,dark_goal):
    pass