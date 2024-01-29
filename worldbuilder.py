import math
import random


def dice_roll(n):
    if n < 1: return True
    if random.randint(0,n) == 1: return True
    else: return False


def create_world(width, height):
    world = []
    height += 64
    for layer in range(height):
        world.append([])
        for selection in range(width):
            if layer < 64:
                world[layer].append("air")
                continue
            elif layer == 64:
                world[layer].append("grass")
            elif layer == height-1:
                world[layer].append("bedrock")
            else:
                while True:
                    if dice_roll(layer-64):
                        world[layer].append("dirt")
                        break
                    elif dice_roll(5):
                        world[layer].append("stone")
                        break
                    elif dice_roll(5000//(layer-64)):
                        world[layer].append("ore")
                        break
            
    return world


