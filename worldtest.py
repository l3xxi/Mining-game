import tkinter
import math
import random
import worldbuilder
import time
import functools
import block_list
import sys


blocklist = block_list.blocklist
#print(blocklist)
inventory = ["grass","dirt","stone","ore","bedrock","redwool","orangewool",
             "yellowwool","greenwool","bluewool","purplewool","pinkwool"]
#print(inventory)
inventory_index = 0

screen_fov = 1

w_width =  400
w_height = 400

width =  20                                 
height = 100

player_x = 0
player_y = 64*w_width/width-(w_height-w_height/4)


world = worldbuilder.create_world(width, height)

root = tkinter.Tk()


class MenuButton:
    def __init__(self, x1p, y1p, x2p, y2p, text, callback=None):
        self.x1 = x1p*w_width
        self.x2 = x2p*w_width
        self.y1 = y1p*w_height
        self.y2 = y2p*w_height
        self.text = text
        self.callback = callback
    def draw(self, canvas):
        canvas.create_rectangle(self.x1,self.y1,self.x2,self.y2,fill="#ffffff")
        canvas.create_text(self.x1+((self.x2-self.x1)//2),self.y1+((self.y2-self.y1)//2),text=self.text)
    def click_check(self, event):
        if (self.x1 <= event.x <= self.x2) and (self.y1 <= event.y <= self.y2) and (self.callback is not None): 
            self.callback()
            return True
        return False



def world_draw(canvas, world,  width, height, x_offset, y_offset):
    global screen_fov
    canvas.delete("all")
    for i, layer in enumerate(world):
        for j, selection in enumerate(layer):
            if selection == "air"    : continue
            colour = block_list.blocklist[selection]
            canvas.create_rectangle(x_offset+(j*(w_width/width)*screen_fov), y_offset+(i*(w_width/width)*screen_fov), x_offset+((j+1)*(w_width/width)*screen_fov), y_offset+((i+1)*(w_width/width)*screen_fov), fill=colour)                                                                                                                
    game_container.create_rectangle(0,w_height,w_width,w_height-(w_height//8), fill="black")
    for j, i in enumerate(inventory):      
        game_container.create_rectangle(j*w_width//len(inventory), w_height, (j*w_width/len(inventory))+w_width/len(inventory), w_height-(w_height//16), fill=block_list.blocklist[i])
        game_container.create_text(((j*w_width/len(inventory))+(w_width/len(inventory))/8), w_height-((w_height//16)/8), text=j)
    j = inventory_index
    game_container.create_rectangle(j*w_width//len(inventory)-5, w_height+5, (j*w_width/len(inventory)+w_width/len(inventory))+5, w_height-(w_height//16)-5, fill=block_list.blocklist[inventory[j]])
    for i in buttons:
        i.draw(game_container)

def write_saved_file():
    with open("mainsave.txt", "w") as f:
        for i in world:
            f.write(str(i))
def read_saved_file():
    with open("mainsave.txt", "r") as f:
        global world
        new_world = []
        for i in f.readlines():
            #print(i)
            new_world.append(i)
        print(new_world)
        world = new_world#.split("]")

buttons = []
help_button = MenuButton(0,0,0.2,0.05, "Help")
settings_button = MenuButton(0.2,0,0.4,0.05, "Settings")
save_button = MenuButton(0.4,0,0.6,0.05, "Save", callback=write_saved_file)
load_button = MenuButton(0.6,0,0.8,0.05, "Load", callback=read_saved_file)
exit_button = MenuButton(0.8,0,1,0.05, "Exit", callback=root.destroy)
buttons.append(help_button)
buttons.append(settings_button)
buttons.append(save_button)
buttons.append(load_button)
buttons.append(exit_button)



game_container = tkinter.Canvas(root, width=w_width, height=w_height)
world_draw(game_container, world, width, height, player_x, -(player_y))


def move_up(*args):
    global player_x
    global player_y
    player_y -= w_width/width
    world_draw(game_container, world, width, height, player_x, -(player_y))
    

def move_down(*args):
    global player_x
    global player_y
    player_y += w_width/width
    world_draw(game_container, world, width, height, player_x, -(player_y))
    

def move_left(*args):
    global player_x
    global player_y
    player_x += w_width/width
    world_draw(game_container, world, width, height, player_x, -(player_y))
    

def move_right(*args):
    global player_x
    global player_y
    player_x -= w_width/width
    world_draw(game_container, world, width, height, player_x, -(player_y))
    

def break_block(mouse_pos):
    global inventory
    global player_x
    global player_y
    global world
    try:
        idx_y = math.ceil(((mouse_pos.y+(player_y))/w_width)*width/screen_fov)-1
        idx_x = math.ceil(((mouse_pos.x+(-player_x))/w_width)*width/screen_fov)-1
        print(mouse_pos.x, mouse_pos.y)
        if not ((0 < idx_y < len(world)) or (0 < idx_x < len(world[0]))):
            return
            
        world[idx_y][idx_x] = "air"
        if check_button_collides(mouse_pos): return
    except IndexError:
        return
    world_draw(game_container, world, width, height, player_x, -(player_y))

def check_button_collides(mouse_pos):
    a = []
    for i in buttons:
        b = i.click_check(mouse_pos)
        a.append(b)
    if any(a):
        return True
    return False
    

def place_block(mouse_pos):
    global player_x
    global player_y
    global world
    global inventory
    if len(inventory) == 0:
        print("No blocks in inventory")
    try:
        idx_y = math.ceil(((mouse_pos.y+(player_y))/w_width)*width/screen_fov)-1
        idx_x = math.ceil(((mouse_pos.x+(-player_x))/w_width)*width/screen_fov)-1
        if not ((0 < idx_y < len(world)) or (0 < idx_x < len(world[0]))):
            return
        world[idx_y][idx_x] = inventory[inventory_index]
        #inventory.remove(inventory[0])
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

def gravity(event):
    for i, a in enumerate(world):
        for j, b in enumerate(a):
            try:
                k = -(i+2)
                #print(world[k][m], world[k][m])
                if world[k+1][j] == "air":
                    world[k][j] = "air"
                    world[k+1][j] = b
            except IndexError:
                continue
    world_draw(game_container, world, width, height, player_x, -(player_y))



    

game_container.pack(pady=0, padx=0)


root.geometry("{}x{}".format(w_width, w_height))
root.resizable(False, False)

#def main():
    #gravity()
    #world_draw(game_container, world, width, height, player_x, -(player_y))
    #root.after(32, main)


root.bind("s", move_down)
root.bind("w", move_up)
root.bind("a", move_left)
root.bind("d", move_right)
root.bind("g", gravity)
#root.bind("q", functools.partial(inventory_change, -1))
#root.bind("e", functools.partial(inventory_change,  1))
root.bind("<MouseWheel>", inventory_change)
root.bind("<Button-1>", break_block)
root.bind("<Button-3>", place_block)



if __name__ == "__main__":
    root.mainloop()
