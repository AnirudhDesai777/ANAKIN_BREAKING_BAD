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
count = 50
while (light_goal not in path or dark_goal not in path):
    Grid,start_state,light_goal,dark_goal = game.grid_initialization()
    Grid = game.obstacleMap()
    path = game.BFS(start_state)
    count -= 1
    if count ==0:  # quit game if no path found after 50 tries
        quit()

#get light path
light_path = game.lightPathASTAR(start_state,light_goal,dark_goal)

#initialize enemies
Grid = game.initialize_enemies(light_path)

#get reward matrix
game_rewards_matrix = gameRewards(Grid)

#initialize agent with a route to the light goal
agent = GridSolver(game_rewards_matrix,dark_goal,light_goal)
agent.calculate_values(game_rewards_matrix)

current_state = start_state

current_state = start_state

action = agent.policy[current_state]

senti = SentimentClassifier()

temp_rewards = np.copy(game_rewards_matrix)

print(Grid)


pygame.init() # Initialize pygame

# Screen dimensions
screen_width, screen_height = 800, 600

# Set up the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Grid and Text Input Game")

# Define the grid and text input area
grid_height = int(screen_height * (2/3))
input_height = screen_height - grid_height - 150

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

import pygame.image

def draw_grid(grid,compassion):
    obstacle_image = pygame.image.load('images/waall.jpg')  # Load the obstacle image
    obstacle_image = pygame.transform.scale(obstacle_image, (cell_width, cell_height))  # Scale the image to match cell size

    yoda_image = pygame.image.load('images/yoda.png')  # Load the yoda image
    yoda_image = pygame.transform.scale(yoda_image, (cell_width, cell_height))  # Scale the image to match cell size

    anakin_image = pygame.image.load('images/anakin_good.png')  # Load the anakin image
    anakin_image = pygame.transform.scale(anakin_image, (cell_width, cell_height))  # Scale the image to match cell size

    anakin_red = pygame.image.load('images/anakin_red.png')  # Load the anakin image
    anakin_red = pygame.transform.scale(anakin_red, (cell_width, cell_height))  # Scale the image to match cell size

    anakin_red_bright = pygame.image.load('images/anakin_red_brighter.png')  # Load the anakin image
    anakin_red_bright = pygame.transform.scale(anakin_red_bright, (cell_width, cell_height))  # Scale the image to match cell size

    palpatine_image = pygame.image.load('images/palpa.jpg')  # Load the palpatine image
    palpatine_image = pygame.transform.scale(palpatine_image, (cell_width, cell_height))  # Scale the image to match cell size

    younglings_image = pygame.image.load('images/youngling.png')  # Load the younglings image
    younglings_image = pygame.transform.scale(younglings_image, (cell_width, cell_height))  # Scale the image to match cell size

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            cell_value = grid[row, col]
            if cell_value == -np.inf:  # obstacle
                screen.blit(obstacle_image, (col * cell_width, row * cell_height))
            elif cell_value == -50:  # enemy
                screen.blit(younglings_image, (col * cell_width, row * cell_height))
            elif cell_value == -200:  # dark goal
                screen.blit(palpatine_image, (col * cell_width, row * cell_height))
            elif cell_value == 150:  # light goal
                screen.blit(yoda_image, (col * cell_width, row * cell_height))
            elif cell_value == 69:  # current_state
                if compassion <28.2:
                    screen.blit(anakin_red_bright, (col * cell_width, row * cell_height))
                elif compassion <50:
                    screen.blit(anakin_red, (col * cell_width, row * cell_height))
                else:
                    screen.blit(anakin_image, (col * cell_width, row * cell_height))
            elif cell_value == -1:  # normal path
                pygame.draw.rect(screen, WHITE, (col * cell_width, row * cell_height, cell_width, cell_height))
            # else:
                # pygame.draw.rect(screen, GRAY, (col * cell_width, row * cell_height, cell_width, cell_height))
            pygame.draw.rect(screen, GRAY, (col * cell_width, row * cell_height, cell_width, cell_height), 1)  # Add mesh-like grid

def draw_text_input(health, compassion,killed):
    # Render the text
    txt_surface = font.render(text, True, BLACK)
    # Resize the box width if the text is too long.
    width = max(200, txt_surface.get_width() + 10)
    input_box.w = width
    # Blit the text
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    # Draw the input box
    pygame.draw.rect(screen, BLACK, input_box, 2)
    
    # Display health and compassion
    health_text = font.render(f"  Health: {health}", True, BLACK)
    compassion_text = font.render(f"  Dark Pull: {100-compassion}", True, BLACK)
    killed_text = font.render(f"  People Killed: {killed}", True, BLACK)
    game_score = font.render(f"  Game_score: {killed*10}", True, BLACK)

    screen.blit(health_text, (input_box.x + input_box.w + 10, input_box.y))
    screen.blit(compassion_text, (input_box.x + input_box.w + 10, input_box.y + 30))
    screen.blit(killed_text, (input_box.x + input_box.w + 10, input_box.y + 60))
    screen.blit(game_score, (input_box.x + input_box.w + 10, input_box.y + 90))



# Main game loop
running = True
active = True

temp1 = np.copy(game_rewards_matrix)
temp1[start_state] = 69
kill_count = 0
flag = False
while not agent.is_terminal_state(current_state[0],current_state[1]) :
    if(not flag):
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN: # User clicked somewhere
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos): 
                    # Toggle the active variable.
                    active = not active
                else: # User clicked somewhere else
                    active = False
            elif event.type == pygame.KEYDOWN: # User pressed a key
                if active:
                    if event.key == pygame.K_RETURN:
                        count = 1
                        print(text)  # You might want to handle the entered text here
                        senti_input = text # input("Player input: ")
                        senti.feedData(senti_input)
                        og_comp = senti.get_compassion()
                        print("compassion :",og_comp)
                        senti.modify_compassion()
                        if(senti_input!=''):
                            for i in range(len(game_rewards_matrix)):
                                for j in range(len(game_rewards_matrix)):
                                    if game_rewards_matrix[i,j] == -50: # enemies
                                        temp_rewards[i,j] = get_reward_killing_enemy(senti.get_compassion())
                                        if(count == 1):
                                            print("enemy",temp_rewards[i,j])
                                            count +=1
                                    elif game_rewards_matrix[i,j] == 150: # light state
                                        temp_rewards[i,j] = get_reward_light_side(senti.get_compassion())
                                        print("light goal",temp_rewards[i,j])
                                    elif game_rewards_matrix[i,j] == -200: # dark state
                                        temp_rewards[i,j] = get_reward_dark_side(senti.get_compassion())
                                        print("dark goal",temp_rewards[i,j])
                        action = agent.policy[current_state]

                        new_state = agent.get_next_cell(current_state[0],current_state[1],action)
                        current_state = new_state
                        if(game_rewards_matrix[current_state]==-50):
                            game_rewards_matrix[current_state] = -1
                            temp_rewards[current_state] = -1
                            senti.modify_kill_compassion()
                            kill_count +=1
                            print('compassion after killing',senti.get_compassion())
                            print(senti.get_compassion())
                        agent.calculate_values(temp_rewards)
                        agent.reduce_health()

                        print ("Anakin health :",agent.get_health())
                        print("modified compassion :",senti.get_compassion())
                        print('decay factor: ',senti.decay_factor)
                        print('old state',current_state)
                        print('new state',new_state)
                        print(np.round(agent.values,1))
                        temp1 = np.copy(game_rewards_matrix)
                        temp2 = np.copy(temp_rewards)
                        temp2[current_state] = 69
                        temp1[current_state] = 69
                        print(np.round(temp2,2))
                        
                        if agent.get_health() <= 0:
                            flag = True
                            break


                        text = ''  # Clear the text
                    elif event.key == pygame.K_BACKSPACE:

                        text = text[:-1]
                    else:
                        text += event.unicode
        
        screen.fill(WHITE)
        draw_grid(temp1,senti.get_compassion())
        draw_text_input(health=agent.get_health(), compassion=senti.get_compassion(),killed=kill_count)
        pygame.display.flip()
    else:
        break
icon = None

if (current_state[0], current_state[1]) == agent.dark_goal:
    message = "Welcome to the DARK SIDE!"
    image_path = 'images/palpa.jpg'  # Replace with the actual path to your image
    icon = pygame.image.load(image_path)
    icon = pygame.transform.scale(icon, (375, 175))
elif (current_state[0], current_state[1]) == agent.light_goal:
    message = "You are Soft !!"
    image_path = 'images/sadpalpa.jpg' 
    icon = pygame.image.load(image_path)
    icon = pygame.transform.scale(icon, (400, 175)) # Replace with the actual path to your image

else:
    message = "Wasted! You lose!"

# Load the image
  # Adjust the size as needed

blur_surface = pygame.Surface((screen_width, screen_height))
blur_surface.set_alpha(230) 
screen.blit(blur_surface, (0, 0))

if icon is not None:
    screen.blit(icon, (200, 100)) 

font_large = pygame.font.Font(None, 72)
text_large = font_large.render(message, True, WHITE)
text_rect = text_large.get_rect(center=(screen_width // 2, screen_height // 2))
screen.blit(text_large, text_rect)

pygame.display.flip()


waiting_for_key = True
while waiting_for_key:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            waiting_for_key = False
        elif event.type == pygame.KEYDOWN:
            waiting_for_key = False

pygame.quit()

