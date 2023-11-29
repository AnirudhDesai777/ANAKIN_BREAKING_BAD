from GenerateGrid import GridGame
from GridSolver import GridSolver
from SentimentClassifier import SentimentClassifier
from Helpers import visualize_grid, gameRewards
import numpy as np
import os
from Rewards import get_reward_killing_enemy,get_reward_dark_side,get_reward_light_side


#initialize game
compassion = 100
decaying_factor = 0.2
scaling_factor = 10
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

temp_rewards = np.copy(game_rewards_matrix)
senti_input = None
while(agent.is_terminal_state(current_state[0],current_state[1])[1]==False or senti_input!= 'ENDGAME'):
    action = agent.policy[current_state]
    new_state = agent.get_next_cell(current_state[0],current_state[1],action)
    senti_input = input("Player input: ")
    
    senti.feedData(senti_input)
    og_comp = senti.get_compassion()
    print("compassion :",og_comp)
    senti.modify_compassion()
    print("modified compassion :",senti.get_compassion())

    # senti.output()
    # sentiment = senti.output()
    # compassion += sentiment['compound']* decaying_factor*scaling_factor
    # compassion = max(100,compassion)

    # if sentiment[0]['label'] == 'NEGATIVE':
    count = 1
    for i in range(len(game_rewards_matrix)):
        for j in range(len(game_rewards_matrix)):
            
            if game_rewards_matrix[i,j] == -50: # enemies
                # print('chaning enemy rewar')
                temp_rewards[i,j] = get_reward_killing_enemy(senti.get_compassion())
                if(count == 1):
                    print("enemy",temp_rewards[i,j])
                    count +=1
            elif game_rewards_matrix[i,j] == 150: # light state
                #logic to change light state reward
                temp_rewards[i,j] = get_reward_light_side(senti.get_compassion())
                print("light goal",temp_rewards[i,j])
            elif game_rewards_matrix[i,j] == -200: # dark state
                #logic to change dark state
                temp_rewards[i,j] = get_reward_dark_side(senti.get_compassion())
                print("dark goal",temp_rewards[i,j])
    agent.calculate_values()
    print()
    # print(game_rewards_matrix)
    # print(temp_rewards)
    
