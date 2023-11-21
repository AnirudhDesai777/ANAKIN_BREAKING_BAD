import numpy as np
import random
import math
import heapq
from Helpers import validNeighbourBFS, validMovesASTAR, visualize_grid

import matplotlib.pyplot as plt
import numpy as np


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
def BFS(Grid, start):
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
    
def grid_initialization(size=10):
    shape = (size,size)
    Grid = np.zeros(shape=shape)
    #assign dark and light goal states
    light_goal = (Grid.shape[0]-1,Grid.shape[1]-1)
    dark_goal = (0,Grid.shape[0]-1)
    Grid[light_goal] = 100
    Grid[dark_goal] = 10
    start_state = (math.floor((Grid.shape[0]-1)/2),0)
    return Grid, start_state,light_goal,dark_goal

Grid,start_state,light_goal,dark_goal = grid_initialization()

#initialize obstacle map
Grid = obstacleMap(Grid,start_state,light_goal,dark_goal)

#check if a path exists to the light goal otherwise regenerate obstacles
path = BFS(Grid,start_state)
while(light_goal not in path and dark_goal not in path):
    Grid,start_state,light_goal,dark_goal = grid_initialization()
    Grid = obstacleMap(Grid,start_state,light_goal,dark_goal)
    path = BFS(Grid,start_state)

#print grid
# print(Grid)

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
print('light_path is')
print(light_path)

#initialize enemies in the path except for the path given by ASTAR to light.
# def initalize_enemies(Grid,start_state,light_goal,dark_goal):
#     pass

import random

def initialize_enemies(Grid, start_state, light_goal, dark_goal, light_path):
    enemy_probability = 0.2
    path_to_light = set(light_path[1])  # Convert path to a set for faster lookup

    def place_enemies():
        for i in range(len(Grid)):
            for j in range(len(Grid[0])):
                if (i, j) not in [start_state, light_goal, dark_goal] and Grid[i][j] != -1 and (i, j) not in path_to_light:
                    if random.random() < enemy_probability:
                        Grid[i][j] = -2  #  -2 represents an enemy

    def path_exists_without_enemies():
        path = BFS(Grid, start_state)  
        for node in path:
            if Grid[node[0]][node[1]] == -2:  # Check if the path contains an enemy
                return False
        return True

    while True:
        print('no enemies in path , replacing enemies')
        place_enemies()
        if not path_exists_without_enemies():
            break
        else:
            # Reset enemy positions if an enemy-free path to dark goal exists
            for i in range(len(Grid)):
                for j in range(len(Grid[0])):
                    if Grid[i][j] == -2:
                        Grid[i][j] = 0  # Reset the cell to empty

    return Grid


Grid = initialize_enemies(Grid, start_state, light_goal, dark_goal, light_path)
print(Grid)

visualize_grid(Grid, start_state, light_goal, dark_goal, light_path)
