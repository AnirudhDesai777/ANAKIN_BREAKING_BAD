from GenerateGrid import GridGame
from Helpers import visualize_grid, gameRewards
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

game_rewards = gameRewards(Grid)


class GridSolver:
    def __init__(self,game,discount_factor=0.9):
        self.game = game
        self.values = np.zeros((len(game),len(game)))
        self.discount_factor = discount_factor
        self.actions = ['up','right','down','left']
        self.policy = np.zeros_like(game,dtype=np.object_)
    
    def calculate_values(self):
        
        threshold = 0.01
        while True:
            delta = 0
            for i in range(len(self.game)):
                for j in range(len(self.game)):
                    old_value = self.values[i,j]
                    new_value = self.get_max_value(i,j) 
                    self.values[i,j] = new_value
            delta = max(delta, np.abs(old_value - new_value))
            if delta < threshold:
                break
    
    def get_max_value(self,row,col):
        max_value = float('-inf')
        for action in self.actions:
            next_row, next_col = self.get_next_cell(row, col, action)
            reward = self.game[next_row, next_col]
            value = reward + self.discount_factor * self.values[next_row, next_col]
            if value > max_value:
                max_value = value
                self.policy[row, col] = action
        return max_value

    def get_next_cell(self,current_row_index, current_column_index, action):
        new_row_index = current_row_index
        new_column_index = current_column_index
        if action == 'up' and current_row_index > 0:
            new_row_index -= 1
        elif action == 'right' and current_column_index < len(self.game) - 1:
            new_column_index += 1
        elif action == 'down' and current_row_index < len(self.game) - 1:
            new_row_index += 1
        elif action == 'left' and current_column_index > 0:
            new_column_index -= 1
        return new_row_index, new_column_index


agent = GridSolver(game_rewards)
agent.calculate_values()
print("Values:", agent.values)
print("Policy:", agent.policy)
    

