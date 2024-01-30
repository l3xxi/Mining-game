import tkinter
import math
import random
import worldbuilder
import time
import functools
import block_list


blocklist = block_list.blocklist
#print(blocklist)
inventory = ["grass","dirt","stone","ore","bedrock","redwool","orangewool",
             "yellowwool","greenwool","bluewool","purplewool","pinkwool"]
#print(inventory)
inventory_index = 0

screen_fov = 3

w_width =  800
w_height = 800

width =  20                                 
height = 100

player_x = 0
player_y = 0


world = worldbuilder.create_world(width, height)




class MenuButton:
    def __init__(self, x1, y1, x2, y2, text, callback=None):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.text = text
        self.callback = callback
    def draw(self, canvas):
        canvas.create_rectangle(self.x1,self.y1,self.x2,self.y2,fill="#ffffff")
        canvas.create_text(self.x1+((self.x2-self.x1)//2),self.y1+((self.y2-self.y1)//2),text=self.text)
    def click_check(self, event):
        if (self.x1 <= event.pos.x <= self.x2) and (self.y1 <= event.pos.y <= self.y2) and (self.callback is not None): 
            self.callback()


def world_draw(canvas, world,  width, height, x_offset, y_offset):
    global screen_fov
    canvas.delete("all")
    for i, layer in enumerate(world):
        for j, selection in enumerate(layer):
            if selection == "air"    : continue
            colour = block_list.blocklist[selection]
            canvas.create_rectangle(x_offset+(j*(w_width/width)*screen_fov), y_offset+(i*(w_width/width)*screen_fov), x_offset+((j+1)*(w_width/width)*screen_fov), y_offset+((i+1)*(w_width/width)*screen_fov), fill=colour)                                                                                                                
    game_container.create_rectangle(0,w_height,w_width,w_height-(w_height//8), fill="black")
    canvas.create_rectangle(w_width/2-w_width/64*screen_fov, w_width/2-w_width/64*screen_fov,w_width/2+w_width/64*screen_fov, w_width/2+w_width/64*screen_fov, fill="gray")
    for j, i in enumerate(inventory):      
        game_container.create_rectangle(j*w_width//len(inventory), w_height, (j*w_width/len(inventory))+w_width/len(inventory), w_height-(w_height//16), fill=block_list.blocklist[i])
        game_container.create_text(((j*w_width/len(inventory))+(w_width/len(inventory))/8), w_height-((w_height//16)/8), text=j)
    j = inventory_index
    game_container.create_rectangle(j*w_width//len(inventory)-5, w_height+5, (j*w_width/len(inventory)+w_width/len(inventory))+5, w_height-(w_height//16)-5, fill=block_list.blocklist[inventory[j]])
    #game_container.create_text()
    for i in buttons:
        i.draw(game_container)

buttons = []
help_button = MenuButton(2,2,200,40, "Help")
buttons.append(help_button)

root = tkinter.Tk()

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
        idx_y = math.ceil(((mouse_pos.y+(-player_y))/w_width)*width/screen_fov)-1
        idx_x = math.ceil(((mouse_pos.x+(-player_x))/w_width)*width/screen_fov)-1
        print(mouse_pos.x, mouse_pos.y)
        if not ((0 < idx_y < len(world)) or (0 < idx_x < len(world[0]))):
            return
            
        print(world[idx_y][idx_x])
        world[idx_y][idx_x] = "air"
    except IndexError:
        print("a")
        return
    world_draw(game_container, world, width, height, player_x, -(player_y))
    

def place_block(mouse_pos):
    global player_x
    global player_y
    global world
    global inventory
    if len(inventory) == 0:
        print("No blocks in inventory")
    try:
        idx_y = math.ceil(((mouse_pos.y+(-player_y))/w_width)*width/screen_fov)-1
        idx_x = math.ceil(((mouse_pos.x+(-player_x))/w_width)*width/screen_fov)-1
        if not ((0 < idx_y < len(world)) or (0 < idx_x < len(world[0]))):
            return
        world[idx_y][idx_x] = inventory[inventory_index]
        #inventory.remove(inventory[0])
    except IndexError:
        print("a")
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
 

def inventory_change(n, event):
    global inventory_index
    global inventory
    inventory_index += n
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
root.bind("q", functools.partial(inventory_change, -1))
root.bind("e", functools.partial(inventory_change,  1))
root.bind("<MouseWheel>", zoom)
root.bind("<Button-1>", break_block)
root.bind("<Button-3>", place_block)



if __name__ == "__main__":
    root.mainloop()
