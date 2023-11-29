from GenerateGrid import GridGame
from Helpers import visualize_grid, RewardMatrix
import numpy as np

game = GridGame(size=10, obstacle_prob=0.2, enemy_prob=0.2)
Grid,start_state,light_goal,dark_goal = game.grid_initialization()

#initialize obstacle map
Grid = game.obstacleMap()


path = game.BFS(start_state)
while (light_goal not in path or dark_goal not in path):
    Grid,start_state,light_goal,dark_goal = game.grid_initialization()
    Grid = game.obstacleMap()
    path = game.BFS(start_state)

light_path = game.lightPathASTAR(start_state,light_goal,dark_goal)

Grid = game.initialize_enemies(light_path)

visualize_grid(Grid,start_state, light_goal, dark_goal, light_path)

rewards = RewardMatrix(Grid)
print(rewards)

print ("start state ",start_state)

print ("light state ",light_goal)

print ("dark goal ",dark_goal)

print ("light path ",light_path)