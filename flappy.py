from tkinter import *
from math import *
import random

class Pipe:
    def __init__(self, start_pos, gap):
        self.gap = gap
        self.x = start_pos
    def move(self, increment):
        self.x -= increment
        if self.x < -10:
            self.x = 600
            self.gap = random.randint(50,100)
            
    def draw(self, canvas):
        canvas.create_rectangle(self.x-10, -10, self.x+10, 300-self.gap, fill="green")
        canvas.create_rectangle(self.x-10, 610, self.x+10, 300+self.gap, fill="green")

    def collisions(self, bird_y):
        if (self.x-10 < 60 < self.x +10) and ((0 < bird_y < 300-self.gap ) or (600 > bird_y > 300+self.gap)):
            
            return True
pipes = []

bird_colour = "yellow"
bird_height = 300
bird_velocity = 0

root = Tk()
root.geometry("600x600")

canv = Canvas(root, width=600, height=600)
canv.pack()

for i in range(6):
    x = 600+(i*100)
    pipes.append(Pipe(x, random.randint(50,100)))

def move_bird():
    global bird_velocity
    global bird_height
    bird_height += bird_velocity

def gravity():
    global bird_velocity
    if bird_velocity > 10:
        return
    else:
        bird_velocity += 9.81/60

def jump(*args):
    global bird_velocity
    print(bird_velocity)
    if bird_velocity < -10:
        return
    else:
        bird_velocity -= 3

def loop():
    global bird_colour
    canv.delete("all")
    gravity()
    move_bird()
    canv.create_rectangle(40, bird_height-10, 60, bird_height+10, fill=bird_colour)
    for pipe in pipes:
        if pipe.collisions:
            print("collision")
            bird_colour = "red"
        pipe.move(2)
        pipe.draw(canv)
    root.after(16, loop)

root.bind("<Button-1>", jump)

loop()
root.mainloop()
