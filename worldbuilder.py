from random import *


def create_world(width, height):
    world = []
    for layer in range(height):
        world.append([])
        for selection in range(width):
            world[layer].append("air")
    return world

def randomise_world(world):
    height = len(world)
    width = len(world[0])
    for layer in range(height):
        for selection in range(width):
            if layer < 64:
                world[layer][selection] = "air"
                continue
            elif layer == 64:
                world[layer][selection]= "grass"
            elif layer == height-1:
                world[layer][selection]= "bedrock"
            else:
                while True:
                    if random()< 0.25:
                        world[layer][selection]= "dirt"
                        break
                    elif random() < 0.5:
                        world[layer][selection]= "stone"
                        break
                    elif random() < 0.001*(layer/height*100):
                        world[layer][selection]= "ore"
                        break
            
    return world


