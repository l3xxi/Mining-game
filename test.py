import tkinter
import math
import random
import worldbuilder
import time
import functools


screen_width = 600
screen_height = 600

width = 10
height = 1000

player_x = 0
player_y = -(screen_width-screen_height/width)

world = worldbuilder.create_world(width, height)

def world_draw(canvas, world,  width, height, offset):
    
    for i, layer in enumerate(world):
        for j, selection in enumerate(layer):
            if  selection == "grass":  colour = "#154009"
            elif selection == "dirt":  colour = "#9c5b33"
            elif selection == "stone": colour = "#4d4d4d"
            elif selection == "ore":   colour = "#74edd7"
            elif selection == "air": continue
            canvas.create_rectangle(j*(screen_width/width), offset+(i*(screen_width/width)), (j+1)*(screen_height/width), offset+((i+1)*(screen_height/width)), fill=colour)
    


root = tkinter.Tk()

game_container = tkinter.Canvas(root, width=screen_width, height=screen_height)

world_draw(game_container, world, width, height, -(player_y))

def move_up(*args):
    global player_y
    game_container.delete("all")
    print(*args)
    player_y -= 100
    world_draw(game_container, world, width, height, -(player_y))

def move_down(*args):
    global player_y
    game_container.delete("all")
    print(*args)
    player_y += 100
    world_draw(game_container, world, width, height, -(player_y))

def break_block(mouse_pos):
    print(mouse_pos.x, mouse_pos.y)
    global player_y
    global world
    print((mouse_pos.y+-(player_y))//(600*len(world)), mouse_pos.x//(600//len(world[0])))
    world[(mouse_pos.y+-(player_y))//(600*len(world))][mouse_pos.x//(600//len(world[0]))] = "air"

def game_loop():
    #world_draw(game_container, world, width, height, -(player_y))
    root.after(250, game_loop)

game_container.pack(pady=0, padx=0)


root.geometry("{}x{}".format(screen_width,screen_height))
root.resizable(False, False)

root.bind("s", move_down)
root.bind("w", move_up)
root.bind("<Button-1>", break_block)


game_loop()

if __name__ == "__main__":
    root.mainloop()
