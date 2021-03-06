#!/usr/bin/env python3
from sense_hat import SenseHat
import time
from subprocess import call
#Se lance au demarage du rasp, interface de dessin dissimulant le sense-lock
#Permet soit de lancer l'encodage de la clef si aucun message n'est enregistre et le decodage dans le cas contraire
#Permet egalement de supprimer l'intergralite des fichiers de notre logiciel sur le rasp

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
#Dessin pour acceder a l encode
dessin = [[0, 0, 0], [0, 0, 248], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
 [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
 [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
 [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [248, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
 [248, 252, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
 [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 252, 0], [248, 252, 0], \
 [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
 [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
#Dessin pour l autodestruction
dessin2 = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
 [0, 0, 0], [248, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [248, 0, 0], [0, 0, 0], \
 [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
 [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
 [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
 [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], \
 [0, 0, 0], [248, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [248, 0, 0], [0, 0, 0], \
 [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]

pro = True #Permet de faire tourner la boucle permettant de dessiner jusqu'a ce que pro = False
color = 0 #couleur du pixel
x = 0 #Position sur l'axe des x du pixel
y = 0 #Position sur l'axe des y du pixel

#position precedente du point
previous_x = 0
previous_y = 0
sense.set_pixel(x,y,white)

def set_color(x,y) :
    global color #Utilise la variable globale color defini en dehors de la fonction
    sense.set_pixel(x,y,list_color[color]) #Colore le pixel grace a la liste de couleurs
    color +=1
    if color == 5 :
        color = 0
        
while pro == True : # Boucle permettant de dessiner
    event = sense.stick.wait_for_event() #Attend pour une action
    if event.direction == "right" and event.action == "pressed" : # Joystick vers la droite, pixel bouge vers la droite
        x += 1
        if x == 8 : #Si on est a l'extremite droite de l'ecran, le pixel apparait du cote gauche
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
        
    if event.direction == "left" and event.action == "pressed" : #Joystick vers la gauche, le pixel vers la gauche
        x -= 1
        if x == -1 : # Si on est au bout de l'ecran, le pixel apparait du cote droit a la meme hauteur
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
        
    if event.direction == "down" and event.action == "pressed" : #Joystick vers le bas, le pixel vers le bas
        y += 1
        if y == 8 : #Si le pixel est en bas de l'ecran, il apparait en haut
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
        
    if event.direction == "up" and event.action == "pressed" : #Joystick vers le haut, pixel vers le haut et prend la temperature 
        temp = sense.get_temperature() #Prend la temp.
        y -= 1
        if y == -1 : #Si le pixel est tout au dessus de l'ecran, il apparait tout en bas
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
     
        if sense.get_pixels() == dessin and event.action == "held" and event.direction == "up" : #Tant que corresond au dessin secret et que le joystick est maintenu vers le haut
            tempb = sense.get_temperature() #Prend une deuxieme temperature
            tempc = sense.get_temperature_from_pressure()
            if tempb > temp + 0.3 or tempc > temp + 0.3: #si la t augmente, affiche du vert et lance le .py correspondant a la situation
                print ("b")
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
                        
                            
        if sense.get_pixels() == dessin2 and event.action == "held" and event.direction == "up" : #Tant que corresond au dessin secret et que le joystick est maintenu vers le haut
            tempb = sense.get_temperature() #Prend une deuxieme temperature
            event = sense.stick.wait_for_event() #attends le pressed
            if temp > tempb + 0.6 : #si la t diminue supprime l'integralite des fichiers du programme
                pro = False
                sense.clear(255,0,0)
                call("rm demo.py encode_key.py message.py message.txt decode.py decode_key.py key.txt fail.txt module.py secure.txt fmessage.txt ", shell=True) # supprime l integralite des fichiers
                call("rm demo.pyc encode_key.pyc message.pyc decode.pyc decode_key.pyc module.pyc", shell=True) # supprime des fichiers pouvant toujours etre present apres suppression des .py
                time.sleep(2)
                call("sudo shutdown now", shell=True) #eteint le rasp
                
