#!/usr/bin/env python3
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
tourne = True 

dessin = [[0, 0, 0], [0, 0, 248], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \ #Dessin pour acceder a encode
[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [248, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
[248, 252, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 252, 0], [248, 252, 0], \
[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

dessin2 = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \ #Dessin pour l auto destruction
[0, 0, 0], [248, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [248, 0, 0], [0, 0, 0], \
[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
[0, 0, 0], [248, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [248, 0, 0], [0, 0, 0], \
[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

pro = True
color = 0
x = 0
y = 0
previous_x = 0
previous_y = 0
sense.set_pixel(x,y,white)

def set_color(x,y) :
    global color #Utilise la variable globale color defini en dehors de la fonction
    sense.set_pixel(x,y,list_color[color]) #Colore le pixel grace a la liste de couleurs
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
        if col == [0,0,0] : #Si non colore affiche un point blanc
            sense.set_pixel(x,y,white)
        else :
            sense.set_pixel(x,y,white) #Fait clignoter le curseur sur les couleurs
            time.sleep(0.1)
            sense.set_pixel(x,y,col)
        previous_x = x - 1 #Prend les coordonnees de la position precedente du curseur
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
        else : #permet de passer au dessus de couleur sans effacer, fait clignoter le curseur une fois sur les couleurs
            sense.set_pixel(x,y,white)
            time.sleep(0.1)
            sense.set_pixel(x,y,col)
        previous_y = y + 1 #Prend les coordonnees de la position precedente
        if previous_y == 8 : #Verfifie si ne depasse pas les bords
            previous_y = 0
        previous_x = x
        
    if event.direction == "middle" and event.action == "pressed" : #change la couleur
        set_color(x,y)
        
    if sense.get_pixel(previous_x,previous_y) == [248, 252, 248] : #verifie si la position precedente est blanche,si oui, efface
        sense.set_pixel(previous_x,previous_y,0,0,0)
        
    if event.direction == "down" and event.action == "held" : # clean l'ecran
        sense.clear()
        
    if event.direction == "up" and event.action == "held" : #quand validation
        pixel = sense.get_pixel(x,y) #Prend la couleur du pixel
        if pixel == [248, 252, 248] : #Si le pixel est blanc, efface le curseur
            sense.set_pixel(x,y,nothing)
        temp = sense.get_temperature() #Prend la temp.
     
        if sense.get_pixels() == dessin and event.action == "held" and event.direction == "up" : #Tant que corresond au dessin secret et que le joystick est maintenu vers le haut
            tempb = sense.get_temperature() #Prend une deuxieme temperature
            tempc = sense.get_temperature_from_pressure()
            if tempb > temp + 0.2 or tempc > temp + 0.2: #si la t augmente, affiche du rouge
                pro = False #Arrete la boucle permettant de dessiner
                sense.clear(0, 255, 0)
                time.sleep(2)
                sense.clear()
                #Verifie s il y a un message enregistre, si oui lance le .py pour rentrer le mdp. S il n y en a pas lance message.py pour en rentrer un.
                f= open("message.txt","r") #ouvre le document message.txt
                message = f.read() #string message = contenu du doc
                f.close()
                if message == "" :
                    import encode_key.py # Permet de rentrer la clef
                else :
                    import decode_key.py # Demande la clef
                        
                            
        elif sense.get_pixels() == dessin2 : #verifie si correspond au dessin secret /!\ kill switch
            pro = False
            while True :
                event = sense.stick.wait_for_event() #attends le pressed
                temp = sense.get_temperature() # quand pressed, prend la t.
                
                while event.action == "held" and event.direction == "up" : 
                    #temps que le joystick est presse prend une deuxieme t.
                    tempb = sense.get_temperature()
                    if temp > tempb + 0.8 : #si la t diminue supprime l'integralite des fichiers du programme
                        sense.clear(255,0,0)
                        call("rm demo.py encode_key.py message.py message.txt decode.py decode_key.py key.txt fail.txt module.py", shell=True) # supprime l integralite des fichiers
                        call("sudo shutdown now", shell=True) #eteint le rasp
                        