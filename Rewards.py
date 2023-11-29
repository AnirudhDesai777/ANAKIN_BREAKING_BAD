import math
import numpy as np
def get_reward_killing_enemy(compassion):
    if compassion < 0 or compassion > 100:
        raise Exception("Compassion factor must be between [0,100].") 
    if compassion > 50:
        return -50
    elif compassion < 50:
        return np.power((compassion - 75)/(-34.5) , 1/0.13)

def get_reward_dark_side(compassion):
    if compassion < 0 or compassion > 100:
        raise Exception("Compassion factor must be between [0,100].")     
    return 50-compassion            

def get_reward_light_side(compassion):
    if compassion < 0 or compassion > 100:
        raise Exception("Compassion factor must be between [0,100].")     
    return compassion-50          