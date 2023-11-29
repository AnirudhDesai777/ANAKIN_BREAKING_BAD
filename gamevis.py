import pygame
import sys
from GenerateGrid import GridGame
from GridSolver import GridSolver
from SentimentClassifier import SentimentClassifier
from Helpers import visualize_grid, gameRewards
import numpy as np
import os
from Rewards import get_reward_killing_enemy,get_reward_dark_side,get_reward_light_side


# Generate the grid
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

print(Grid)


pygame.init()

# Screen dimensions
screen_width, screen_height = 800, 600

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Grid and Text Input Game")

# Define the grid and text input area
grid_height = int(screen_height * (2/3))
input_height = screen_height - grid_height

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Grid cell size
cell_width = screen_width // Grid.shape[1]
cell_height = grid_height // Grid.shape[0]

# Text input
font = pygame.font.Font(None, 36)
text = ''
input_box = pygame.Rect(0, grid_height, screen_width, input_height)

def draw_grid():
    for row in range(Grid.shape[0]):
        for col in range(Grid.shape[1]):
            cell_value = Grid[row, col]
            color = GRAY
            if cell_value == -1: #obstacle
                color = BLACK
            elif cell_value == -2: #enemy
                color = RED
            elif cell_value == 10: # dark goal
                color = BLUE
            elif cell_value == 150: # light goal
                color = GREEN
            elif cell_value == 100: # current_state
                color = WHITE
                # # Move the white state randomly
                # if np.random.rand() < 0.25 and cell_value != -1:  # Adjust the probability as needed and exclude obstacle state
                #     Grid[row, col] = 0  # Clear the current state
                #     new_row = np.random.randint(Grid.shape[0])
                #     new_col = np.random.randint(Grid.shape[1])
                #     Grid[new_row, new_col] = 100  # Set the new random state
                #     row, col = new_row, new_col  # Update the row and col variables
            pygame.draw.rect(screen, color, (col * cell_width, row * cell_height, cell_width, cell_height))
            pygame.draw.rect(screen, WHITE, (col * cell_width, row * cell_height, cell_width, cell_height), 1)  # Add mesh-like grid

def draw_text_input():
    # Render the text
    txt_surface = font.render(text, True, BLACK)
    # Resize the box width if the text is too long.
    width = max(200, txt_surface.get_width() + 10)
    input_box.w = width
    # Blit the text
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    # Draw the input box
    pygame.draw.rect(screen, BLACK, input_box, 2)

# Main game loop
running = True
active = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if input_box.collidepoint(event.pos):
                # Toggle the active variable.
                active = not active
            else:
                active = False
        elif event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_RETURN:
                    print(text)  # You might want to handle the entered text here
                    text = ''  # Clear the text
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

    screen.fill(WHITE)
    draw_grid()
    draw_text_input()
    pygame.display.flip()

pygame.quit()

# def draw_text_input():
#     txt_surface = font.render(text, True, BLACK)
#     screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
#     pygame.draw.rect(screen, BLACK, input_box, 2)

# # Main game loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_BACKSPACE:
#                 text = text[:-1]
#             else:
#                 text += event.unicode

#     screen.fill(WHITE)

#     draw_grid()
#     draw_text_input()

#     pygame.display.flip()

# pygame.quit()
