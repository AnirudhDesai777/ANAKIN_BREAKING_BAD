from GenerateGrid import GridGame
from Helpers import visualize_grid, RewardMatrix
import numpy as np

game = GridGame()
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

#reward matrix

rewards = RewardMatrix(Grid)
print(rewards)

class GridSolver:
    def __init__(self,game):
        self.game = game
        self.q_values = np.zeros((len(game), len(game), 4))
        self.actions = ['up', 'right', 'down', 'left']
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 1.0
        self.epsilon_decay = 0.995
    
    def next_action(self, row, col):
        if np.random.random() < self.epsilon:
            return np.random.choice(4)
        else:
            return np.argmax(self.q_values[row, col])
        
    def get_next_cell(self,current_row_index, current_column_index, action_index):
        new_row_index = current_row_index
        new_column_index = current_column_index
        if self.actions[action_index] == 'up' and current_row_index > 0:
            new_row_index -= 1
        elif self.actions[action_index] == 'right' and current_column_index < len(self.game) - 1:
            new_column_index += 1
        elif self.actions[action_index] == 'down' and current_row_index < len(self.game) - 1:
            new_row_index += 1
        elif self.actions[action_index] == 'left' and current_column_index > 0:
            new_column_index -= 1
        return new_row_index, new_column_index
    
    def is_obstacle_state(self,current_row,current_col):
        if(self.game[current_row,current_col]==-1):
            return False
        else:
            return True

agent  = GridSolver(rewards)


for episode in range(2000):
    row_index, column_index = start_state[0],start_state[1]
    steps = 0
    costs = 0
    while not agent.is_obstacle_state(row_index, column_index):
        action_index = agent.next_action(row_index, column_index)
        old_row_index, old_column_index = row_index, column_index 
        row_index, column_index = agent.get_next_cell(row_index, column_index, action_index)
        reward = agent.game[row_index, column_index]
        old_q_value = agent.q_values[old_row_index, old_column_index, action_index]
        temporal_difference = reward + (agent.discount_factor * np.max(agent.q_values[row_index, column_index])) - old_q_value
        new_q_value = old_q_value + (agent.learning_rate * temporal_difference)
        agent.q_values[old_row_index, old_column_index, action_index] = new_q_value
        steps+=1
        costs+=reward

print('Training complete!')

import pandas as pd
q = np.zeros((len(agent.game)*len(agent.game),6))
q_table = pd.DataFrame(q)
q_table.columns = ['state_row','state_col','up','right','down','left']
q_table['state_col'] = q_table['state_col'].astype(int)
q_table['state_row'] = q_table['state_row'].astype(int)
l=0
for i in range(len(agent.game)*len(agent.game)):
    for j in range(len(agent.game)*len(agent.game)):
        q_table['state_col'][l+j]= j
    for k in range(len(agent.game)):
        q_table['state_row'][l+k]=i
    l+=len(agent.game)

for i in range(len(agent.q_values[0])):
  for j in range(len(agent.q_values[1])):
    index = q_table[(q_table['state_row']==i) & (q_table['state_col']==j)].index
    index = int(index[0])
    for k in range(4):
       q_table.iloc[index,k+2] = agent.q_values[i][j][k]

print(q_table)