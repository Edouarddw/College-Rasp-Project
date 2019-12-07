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

x = 0
y = 0
sense.set_pixel(x, y, white)

# boucle while, joystick permet de naviguer x+1(-1) y+1(-1), pression millieu changer la couleur jusqu a eteindre. Hold : sense.clear()
# si une certaine sequence est enregistree et qu'on augmente la temp ( souffle chaud ), lance la suite