import tkinter
import math
import random
import worldbuilder
import time
import functools
import block_list
import sys


blocklist = block_list.blocklist

inventory = ["grass","dirt","stone","ore","bedrock","redwool","orangewool",
             "yellowwool","greenwool","bluewool","purplewool","pinkwool"]

inventory_index = 0

screen_fov = 1

w_width =  800
w_height = 800

width =  20                           
height = 500

player_x = 0
player_y = 64*w_width/width-(w_height-w_height/4)
player_angle = 0
player_velocity = 0
player_acceleration = 0
player_terminal_velocity = 25


world = worldbuilder.create_world(width, height+64)
world = worldbuilder.randomise_world(world)

root = tkinter.Tk()


def world_draw(canvas, world,  width, height, x_offset, y_offset):
    global screen_fov
    canvas.delete("all")
    for i, layer in enumerate(world):
        for j, selection in enumerate(layer):
            if selection == "air"    : continue
            if i*(w_width/width) < abs(y_offset): continue
            if i*(w_width/width) > abs(y_offset)+w_height: continue
            x1 = (j*(w_width/width)*screen_fov)
            y1 = y_offset+(i*(w_width/width)*screen_fov)
            x2 = ((j+1)*(w_width/width)*screen_fov)
            y2 =  y_offset+((i+1)*(w_width/width)*screen_fov)
            colour = block_list.blocklist[selection]
            colour2 = (hex(colour)[2:])
            canvas.create_rectangle(x1,y1,x2,y2,fill=("#"+"0"*(6-len(colour2))+colour2))                                                                                                            
    canvas.create_rectangle(0,w_height,w_width,w_height-(w_height//8), fill="black")
    canvas.create_text(w_width//2,500, text="{}x, {}y".format(abs(x_offset), abs(y_offset)), fill="black")
    for j, i in enumerate(inventory):
        colour = block_list.blocklist[i]
        colour2 = (hex(colour)[2:])
        canvas.create_rectangle(j*w_width//len(inventory), w_height, (j*w_width/len(inventory))+w_width/len(inventory), w_height-(w_height//16), fill=("#"+"0"*(6-len(colour2))+colour2))
        inv_colour2 = (hex(colour^0xffffff)[2:])
        canvas.create_text(((j*w_width/len(inventory))+(w_width/len(inventory))/8), w_height-((w_height//16)/8), text=j, fill=("#"+"0"*(6-len(inv_colour2))+inv_colour2))
    colour = block_list.blocklist[inventory[inventory_index]]
    colour2 = (hex(colour)[2:])
    canvas.create_rectangle(inventory_index*w_width//len(inventory)-5, w_height+5, (inventory_index*w_width/len(inventory)+w_width/len(inventory))+5, w_height-(w_height//16)-5, fill=("#"+"0"*(6-len(colour2))+colour2))
    #player
    canvas.create_rectangle(x_offset, 400, x_offset+(w_width//20), 400+(w_width//20), fill="#ffffff")

def write_saved_file():
    with open("mainsave.txt", "w") as f:
        for i in world:
            f.write(str(i))
def read_saved_file():
    with open("mainsave.txt", "r") as f:
        global world
        new_world = []
        for i in f.readlines():
            new_world.append(i)
        print(new_world)
        world = new_world



game_container = tkinter.Canvas(root, width=w_width, height=w_height)
world_draw(game_container, world, width, height, player_x, -(player_y))


def jump(*args):
    global player_x
    global player_y
    global player_acceleration
    if player_velocity < player_terminal_velocity:
        player_acceleration -= 9.81/3
    world_draw(game_container, world, width, height, player_x, -(player_y))

def move_up(event):
    global player_y
    player_y -= w_width/width
    world_draw(game_container, world, width, height, player_x, -(player_y))


def move_down(event):
    global player_y
    player_y += w_width/width
    world_draw(game_container, world, width, height, player_x, -(player_y))
    
    
def move_left(*args):
    global player_x
    global player_y
    player_x -= w_width/width
    world_draw(game_container, world, width, height, player_x, -(player_y))
    

def move_right(*args):
    global player_x
    global player_y
    player_x += w_width/width
    world_draw(game_container, world, width, height, player_x, -(player_y))
    

def break_block(mouse_pos):
    global inventory
    global player_x
    global player_y
    global world
    try:
        idx_y = math.ceil(((mouse_pos.y+(player_y))/w_width)*width/screen_fov)-1
        idx_x = math.ceil(((mouse_pos.x)/w_width)*width/screen_fov)-1
        if not ((0 < idx_y < len(world)) or (0 < idx_x < len(world[0]))):
            return
            
        world[idx_y][idx_x] = "air"
    except IndexError:
        return
    world_draw(game_container, world, width, height, player_x, -(player_y))


def place_block(mouse_pos):
    global player_x
    global player_y
    global world
    global inventory
    try:
        idx_y = math.ceil(((mouse_pos.y+(player_y))/w_width)*width/screen_fov)-1
        idx_x = math.ceil(((mouse_pos.x)/w_width)*width/screen_fov)-1
        if not ((0 < idx_y < len(world)) or (0 < idx_x < len(world[0]))):
            return
        world[idx_y][idx_x] = inventory[inventory_index]
    except IndexError:
        return
    world_draw(game_container, world, width, height, player_x, -(player_y))
    
    
def zoom(event):
    global screen_fov
    screen_fov += event.delta/480
    if screen_fov > 5:
        screen_fov = 5

    if screen_fov < 1:
        screen_fov = 1
        
    global player_x
    global player_y
    world_draw(game_container, world, width, height, player_x, -(player_y))
 

def inventory_change(event):
    global inventory_index
    global inventory
    inventory_index += int(event.delta/90)
    inventory_index %= len(inventory)
    world_draw(game_container, world, width, height, player_x, -(player_y))


def gravity(*args):
    global world
    global player_acceleration
    global player_y
    global player_x
    global player_velocity


    
    # world_copy = worldbuilder.create_world(len(world), len(world[0]))
    # for i, a in enumerate(world):
    #     for j, b in enumerate(a):
    #         try:
    #             if world[i+1][j] == "air":
    #                 world_copy[i][j] = "air"
    #                 world_copy[i+1][j] = b
                    
    #             else:
    #                 world_copy[i][j] = b
                
    #         except IndexError:
    #             time.sleep(0.5)
    #             print(i+1,j, i,j, b)
    #             continue
    #world = world_copy
    player_y += player_velocity
    if abs(player_velocity) < player_terminal_velocity:
        player_velocity += player_acceleration
        player_acceleration += 9.81/120   
    world_draw(game_container, world, width, height, player_x, -(player_y))

def resize(event):
    global w_width
    global w_height
    global game_container
    w_width = event.width
    w_height = event.height
    game_container.config(width=w_width, height=w_height)
    world_draw(game_container, world, width, height, player_x, -(player_y))

def main():
    gravity()
    root.after(16, main)


a = tkinter.Button(root, text="test", state="active")

a.pack()

game_container.pack(pady=0, padx=0, fill="both", expand=True)


root.geometry("{}x{}".format(w_width, w_height))
root.resizable(True, True)
game_container.bind("<Configure>", resize)

root.bind("<space>", jump)
root.bind("w", move_up)
root.bind("s", move_down)
root.bind("a", move_left)
root.bind("d", move_right)
root.bind("g", gravity)
root.bind("<MouseWheel>", inventory_change)
root.bind("<Button-1>", break_block)
root.bind("<Button-3>", place_block)



if __name__ == "__main__":
    #main()
    root.mainloop()
    
