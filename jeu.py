#!/usr/bin/env python3
#deviendra demo.py
from sense_hat import SenseHat

sense = SenseHat()
sense.low_light = True
sense.clear()
green = (0, 255, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
white = (255,255,255)
nothing = (0,0,0)
pink = (255,105, 180)
color = [green,yellow,blue,red,white,pink,nothing]

c = 0
x = 0
y = 0

def set_color(x,y) :
    global c
    change = True
    sense.set_pixel(x,y,color[c])
    c +=1
    if c == 7 :
        c = 0
        
while True :
    event = sense.stick.wait_for_event()
    if event.direction == "right" and event.action == "pressed" :
        x += 1
        if x == 8 :
            x = 0
    if event.direction == "left" and event.action == "pressed" :
        x -= 1
        if x == -1 :
            x = 7
    if event.direction == "down" and event.action == "pressed" :
        y += 1
        if y == 8 :
            y = 0
    if event.direction == "up" and event.action == "pressed" :
        y -= 1
        if y == -1 :
            y = 7
    if event.direction == "middle" and event.action == "pressed" :
      set_color(x,y)
    
    
    
# boucle while, joystick permet de naviguer x+1(-1) y+1(-1), pression millieu changer la couleur jusqu a eteindre. Hold : sense.clear()
# si une certaine sequence est enregistree et qu'on augmente la temp ( souffle chaud ), lance la suite