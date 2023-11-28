from GenerateGrid import GridGame
from GridSolver import GridSolver
from SentimentClassifier import SentimentClassifier
from Helpers import visualize_grid, gameRewards
import numpy as np


#initialize game
game = GridGame()
Grid,start_state,light_goal,dark_goal = game.grid_initialization()

#initialize obstacle map
Grid = game.obstacleMap()

#regenerate obstacles still there is a clear path from start to both light and dark
path = game.BFS(start_state)
while (light_goal not in path or dark_goal not in path):
    Grid,start_state,light_goal,dark_goal = game.grid_initialization()
    Grid = game.obstacleMap()
    path = game.BFS(start_state)

#get light path
light_path = game.lightPathASTAR(start_state,light_goal,dark_goal)

#initialize enemies
Grid = game.initialize_enemies(light_path)

#visualize grid
# visualize_grid(Grid,start_state, light_goal, dark_goal, light_path)

#get reward matrix
game_rewards_matrix = gameRewards(Grid)


#initial agent with a route to the light goal
agent = GridSolver(game_rewards_matrix,dark_goal,light_goal)
agent.calculate_values()



current_state = start_state

action = agent.policy[current_state]

senti = SentimentClassifier()

temp_rewards = game_rewards_matrix

while(agent.is_terminal_state(current_state[0],current_state[1])[1]==False):
    action = agent.policy[current_state]
    new_state = agent.get_next_cell(current_state[0],current_state[1],action)
    senti.feedData('you are the worst')
    senti.output()
    sentiment = senti.output()
    if sentiment[0]['label'] == 'NEGATIVE':
        for i in range(len(game_rewards_matrix)):
            for j in range(len(game_rewards_matrix)):
                if game_rewards_matrix[i,j] == -50:
                    change = 50 * 0.9
                    temp_rewards[i,j] += change
        agent.calculate_values()
        print(game_rewards_matrix)


    