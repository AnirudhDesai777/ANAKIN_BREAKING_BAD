from GenerateGrid import GridGame
from Helpers import visualize_grid, gameRewards, validMoves
import numpy as np


class GridSolver:
    def __init__(self,game,dark_goal,light_goal,discount_factor=0.9):
        self.game = game
        self.values = np.zeros((len(game),len(game)))
        self.discount_factor = discount_factor
        self.actions = ['up','right','down','left']
        self.policy = np.zeros_like(game,dtype=np.object_)
        self.dark_goal = dark_goal
        self.light_goal = light_goal
        self.health = 100
    
    def reduce_health(self):
        self.health = self.health - 4

    def get_health(self):
        return self.health

    def calculate_values(self,game):
        self.game = game
        threshold = 0.1
        while True:
            # print('stuck in loop')
            delta = 0
            for i in range(len(self.game)):
                for j in range(len(self.game)):
                    old_value = self.values[i,j]
                    new_value = self.get_max_value(i,j) 
                    self.values[i,j] = new_value
            delta = max(delta, np.abs(old_value - new_value))
            if delta < threshold: # to break the loop
                break
    
    def get_max_value(self,row,col):
        max_value = float('-inf')
        val_list = []
        valid_moves = validMoves(self.game,(row,col))

        for action in self.actions:
            next_row, next_col = self.get_next_cell(row, col, action)
            if (next_row,next_col) not in valid_moves:
                val_list.append(-1* (np.inf))
                continue
            reward = self.game[next_row, next_col]
            value = reward + self.discount_factor * self.values[next_row, next_col]
            val_list.append(value)
        val_list = np.array(val_list)
        max_value = max(val_list)
        self.policy[row, col] = self.actions[np.argmax(val_list)]
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
    
    def is_terminal_state(self,row,col):
        if (row,col) == self.light_goal:
            return True
        if (row,col) == self.dark_goal:
            return True
        else:
            return False