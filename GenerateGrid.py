import numpy as np
import random
import math
import heapq
from Helpers import validNeighbourBFS, validMovesASTAR, visualize_grid

class GridGame:
    def __init__(self, size=10, obstacle_prob=0.2, enemy_prob=0.2):
        self.size = size
        self.obstacle_prob = obstacle_prob
        self.enemy_prob = enemy_prob
        self.grid, self.start_state, self.light_goal, self.dark_goal = self.grid_initialization()

    def grid_initialization(self):
        grid = np.zeros((self.size, self.size))
        light_goal = (grid.shape[0] - 1, grid.shape[1] - 1)
        dark_goal = (0, grid.shape[0] - 1)
        grid[light_goal] = 100
        grid[dark_goal] = 10
        start_state = (math.floor((grid.shape[0] - 1) / 2), 0)
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
        path_to_light = set(light_path[1])
        path_to_dark = self.BFS_to_goal(self.start_state, self.dark_goal)

        for i, j in np.ndindex(self.grid.shape):
            if (i, j) not in [self.start_state, self.light_goal, self.dark_goal, *path_to_light] and self.grid[i][j] != -1:
                if random.random() < self.enemy_prob:
                    self.grid[i][j] = -2  # Enemy represented by -2

        for cell in path_to_dark:
            if cell not in [self.start_state, self.light_goal, self.dark_goal, *path_to_light] and self.grid[cell[0]][cell[1]] != -1:
                if random.random() < self.enemy_prob:
                     self.grid[cell[0]][cell[1]] = -2


