from sense_hat import SenseHat
import time

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