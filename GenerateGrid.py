import numpy as np
import random
import math
import heapq
from Helpers import validNeighbourBFS, validMovesASTAR

class GridGame:
    def __init__(self, size=20, obstacle_prob=0.2, enemy_prob=0.2):
        self.size = size
        self.obstacle_prob = obstacle_prob
        self.enemy_prob = enemy_prob
        self.grid, self.start_state, self.light_goal, self.dark_goal = self.grid_initialization()

    def grid_initialization(self):
        grid = np.zeros((self.size, self.size))
        light_goal = (grid.shape[0] - 1, grid.shape[1] - 1)
        dark_goal = (0, grid.shape[0] - 1)
        grid[light_goal] = 150
        grid[dark_goal] = 10
        start_state = (math.floor((grid.shape[0] - 1) / 2), 0)
        grid[start_state] = 100
        return grid, start_state, light_goal, dark_goal

    def obstacleMap(self):
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) not in [self.start_state, self.light_goal, self.dark_goal]:
                    if random.random() <= self.obstacle_prob:
                        self.grid[i][j] = -1

    def BFS(self, start):
        visited = set()
        queue = [start]
        visited.add(start)
        path = []

        while queue:
            current = queue.pop(0)
            path.append(current)

            for neighbor in validNeighbourBFS(self.grid, current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return path

    def BFS_to_goal(self, start, goal):
        visited = set()
        queue = [(start, [start])]
        visited.add(start)

        while queue:
            current, path = queue.pop(0)
            if current == goal:
                return path
            
            for neighbor in validNeighbourBFS(self.grid, current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None

    def H_score(self, node, goal):  
        heuristic = (abs(node[0] - goal[0]) + abs(node[1] - goal[1])) / (self.size - 1)
        return heuristic

    def lightPathASTAR(self, start, light_goal, dark_goal):
        g = {node: np.inf for node in np.ndindex(self.grid.shape)}
        f = {}
        openList = []
        closeList = []
        parent = {}

        g[start] = 0
        f[start] = self.H_score(start, light_goal)
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

            for neighbor in validMovesASTAR(self.grid, currentNode, dark_goal):
                new_g = g[currentNode] + 1

                if new_g < g[neighbor]:
                    parent[neighbor] = currentNode
                    g[neighbor] = new_g
                    f[neighbor] = g[neighbor] + self.H_score(neighbor, light_goal)
                    heapq.heappush(openList, (f[neighbor], neighbor))

        return None, []

    def initialize_enemies(self, light_path):
        enemy_probability = 0.2
        path_to_light = set(light_path[1])  # Convert path to a set for faster lookup
        path_to_dark = self.BFS_to_goal(self.start_state,self.dark_goal)
    
        # for i in range(len(Grid)):
        #     for j in range(len(Grid[0])):
        #         if Grid[i][j] != -1:  # If the cell is not an obstacle
        #             path = BFS_to_goal(Grid, (i, j), dark_goal)  # Perform BFS to dark goal
        #             for cell in path:
        #                 path_to_dark.add(cell)

        def place_enemies():
            for i in range(len(self.grid)):
                for j in range(len(self.grid[0])):
                    if (i, j) not in [self.start_state, self.light_goal, self.dark_goal] and self.grid[i][j] != -1 and (i, j) not in path_to_light:
                        if random.random() < enemy_probability:
                            self.grid[i][j] = -2  #  -2 represents an enemy


        # def path_exists_without_enemies(): #TODO
        #     path = BFS(Grid, start_state)  
        #     for node in path:
        #         if Grid[node[0]][node[1]] == -2:  # Check if the path contains an enemy
        #             return False
        #     return True
    
        # Function to ensure enemies on paths to dark goal
        def place_enemies_on_dark_paths():
            for cell in path_to_dark:
                if cell not in [self.start_state, self.light_goal, self.dark_goal] and self.grid[cell[0]][cell[1]] != -1 and cell not in path_to_light:
                    if random.random() < 0.1: #enemy_probability:
                        self.grid[cell[0]][cell[1]] = -2  # Place an enemy

        # while True:
        place_enemies()
        place_enemies_on_dark_paths()
        # if not path_exists_without_enemies():
        #     break
        # else:
        #     # Reset enemy positions if an enemy-free path to dark goal exists
        #     for i in range(len(Grid)):
        #         for j in range(len(Grid[0])):
        #             if Grid[i][j] == -2:
        #                 Grid[i][j] = 0  # Reset the cell to empty

        return self.grid





