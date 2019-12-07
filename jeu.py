#!/usr/bin/env python3
#deviendra demo.py
from sense_hat import SenseHat
import time
from subprocess import call

sense = SenseHat()
sense.low_light = True
sense.clear()
green = (0, 255, 0)
yellow = (255, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
white = (255,255,255)
nothing = (0,0,0)
list_color = [green,yellow,blue,red,nothing]

dessin = [[0, 0, 0], [0, 0, 248], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [248, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
[248, 252, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 252, 0], [248, 252, 0], \
[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

pro = True
color = 0
x = 0
y = 0
previous_x = 0
previous_y = 0
sense.set_pixel(x,y,white)

def set_color(x,y) :
    global color
    sense.set_pixel(x,y,list_color[color])
    color +=1
    if color == 5 :
        color = 0
        
while pro == True :
    event = sense.stick.wait_for_event()
    if event.direction == "right" and event.action == "pressed" :
        x += 1
        if x == 8 :
            x = 0
        color = 0
        col = sense.get_pixel(x,y)
        if col == [0,0,0] :
            sense.set_pixel(x,y,white)
        else :
            sense.set_pixel(x,y,white)
            time.sleep(0.1)
            sense.set_pixel(x,y,col)
        previous_x = x - 1
        if previous_x == -1 :
            previous_x = 7
        previous_y = y
        
    if event.direction == "left" and event.action == "pressed" :
        x -= 1
        if x == -1 :
            x = 7
        color = 0
        col = sense.get_pixel(x,y)
        if col == [0,0,0] :
            sense.set_pixel(x,y,white)
        else :
            sense.set_pixel(x,y,white)
            time.sleep(0.1)
            sense.set_pixel(x,y,col)
        previous_x = x + 1
        if previous_x == 8 :
            previous_x = 0
        previous_y = y
        
    if event.direction == "down" and event.action == "pressed" :
        y += 1
        if y == 8 :
            y = 0
        color = 0
        col = sense.get_pixel(x,y)
        if col == [0,0,0] :
            sense.set_pixel(x,y,white)
        else :
            sense.set_pixel(x,y,white)
            time.sleep(0.1)
            sense.set_pixel(x,y,col)
        previous_y = y - 1
        if previous_y == -1 :
            previous_y = 7
        previous_x = x
        
    if event.direction == "up" and event.action == "pressed" :
        y -= 1
        if y == -1 :
            y = 7
        color = 0
        col = sense.get_pixel(x,y)
        if col == [0,0,0] :
            sense.set_pixel(x,y,white) #affiche le curseur en blanc
        else : #permet de passer au dessus de couleur sans effacer
            sense.set_pixel(x,y,white)
            time.sleep(0.1)
            sense.set_pixel(x,y,col)
        previous_y = y+1
        if previous_y == 8 :
            previous_y = 0
        previous_x = x
        
    if event.direction == "middle" and event.action == "pressed" : #change la couleur
        set_color(x,y)
        
    if sense.get_pixel(previous_x,previous_y) == [248, 252, 248] : #verifie si la position precedente est blanche,si oui, efface
        sense.set_pixel(previous_x,previous_y,0,0,0)
        
    if event.direction == "up" and event.action == "held" : #quand validation
        sense.set_pixel(x,y,nothing) #efface le curseur
        
        if sense.get_pixels() == dessin : #verifie si correspond au dessin secret
            pro = False
            while True :
                ideal_temp = 30
                event = sense.stick.wait_for_event() #attends le pressed
                temp = sense.get_temperature() # quand pressed, prend la t.
                
                while event.action == "held" and event.direction == "middle" :
                    #temps que le joystick est pressé prend une deuxieme t.
                    tempb = sense.get_temperature()
                    
                    if tempb > temp + 0.3 : #si la t augmente, affiche du rouge 
                        sense.clear(255, 0, 0)
                        time.sleep(2)
                        sense.clear()
                        #Verifie s il y a un message enregistre, si oui lance le .py pour rentrer le mdp. S il n y en a pas lance message.py pour en rentrer un.
                        f= open("message.txt","r") #ouvre le document message.txt
                        message = f.read() #string message = contenu du doc
                        f.close()

                        if message == "" :
                            call("python3 encode_key.py", shell=True) # Permet de rentrer la clef
                        #else :
                            #call("python3 decode_key.py", shell=True) # Demande la clef
                            
                    if temp > tempb + 0.5 : #si la t diminue affiche du bleu
                        sense.clear(0,0,255)
                        time.sleep(2)
                        sense.clear()