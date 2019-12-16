#!/usr/bin/env python3
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
sense = SenseHat()
from time import sleep

def vx() : #Module permettant de selectionner entre V et X retournant True si V 
    tourne = True
    conserver = True
    for event in sense.stick.get_events(): pass #reinitialise le compteur d actions
    while tourne : #tourne temps qu on a pas valide
        while conserver :
            sense.show_letter("V",(0, 255, 0))
            for event in sense.stick.get_events(): # Si on valide en appuyant au milieu, le message sera conserve, une autre action proposera le x
                if event.action == 'pressed' and event.direction == "middle": 
                    conserver = False
                    tourne = False
                    sense.clear()
                    return True
                if event.action == "pressed" and event.direction != "middle" : #Permet d'aller sur le X
                    conserver = False
                    delete = True
        while delete :
            sense.show_letter("X",(255, 0, 0))
            for event in sense.stick.get_events(): # Si on valide en appuyant au milieu, on peut remettre un message, une autre action recommencera la boucle
                if event.action == 'released' and event.direction == "middle":
                    delete = False
                    tourne = False
                    sense.clear()
                    return False
                if event.action == "pressed" and event.direction != "middle" : #Permet de retourner sur le V
                    conserver = True
                    delete = False
                    
def key() : #Permet d'encoder la clef composee de position dans l espace en utilisant l'accelerometre
    liste_action = [] #liste de stockage des positions dans l espace
    action = 0
    tourne = True
    while tourne :
        if len(liste_action) < 10 : #Affiche le nombre d actions effectuees
            sense.show_letter(str(len(liste_action)))
        else :
            sense.show_message(str(len(liste_action)))
        event = sense.stick.wait_for_event()
        if event.action == "pressed" and event.direction == "middle" : #pression sur le joystick pour ajouter une position
            x = round(sense.get_accelerometer_raw()["x"]) #Prends les donnees de chaques axes du Rasp
            y = round(sense.get_accelerometer_raw()["y"])
            z = round(sense.get_accelerometer_raw()["z"])
            if y == 0 and x == 0 and z == 1 : #Ajoute une action a la liste en fonction de la position validee
                action = "Nothing"
                liste_action.append(action)
            if y == 0 and x == -1 and z == 0 :
                action = "turnleft"
                liste_action.append(action)
            if y == 0 and x == -1 and z == -1 :
                action = "flipleft"
                liste_action.append(action)
            if y == 0 and x == 1 and z == 0 :
                action = "turnright"
                liste_action.append(action)
            if y == 0 and x == 1 and z == -1 :
                action = "flipright"
                liste_action.append(action)
            if y == 1 and x == 0 and z == 0 :
                action = "turnbackward"
                liste_action.append(action)
            if y == -1 and x == 0 and z == 0 :
                action = "turnforward"
                liste_action.append(action)
            if y == 0 and x == 0 and z == -1 :
                action = "flipbackward"
                liste_action.append(action) 
        if event.action == "held" and event.direction == "middle" : return liste_action #Validation de la cle
        
        
def secure_pixels() : #Permet de dessiner lors de l'utilisation du mode secure
    #Ajoute un dessin a effectuer en entrant la cle
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
            
        if event.direction == "up" and event.action == "pressed" : #Joystick vers le haut, pixel vers le haut
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
            sense.set_pixel(x,y,list_color[color])
            color +=1
            if color == 5 : #Verifie que le num ne depasse pas la longueur de la liste
                color = 0
            
        if sense.get_pixel(previous_x,previous_y) == [248, 252, 248] : #verifie si la position precedente est blanche,si oui, efface
            sense.set_pixel(previous_x,previous_y,0,0,0)
            
        if event.direction == "down" and event.action == "held" : # clean l'ecran
            sense.clear()
            
        if event.direction == "up" and event.action == "held" : #quand validation
            pixel = sense.get_pixel(x,y)
            if pixel == [248, 252, 248] : #La liste doit correspondre a blanc
                sense.set_pixel(x,y,nothing) #si c est blanc, efface le curseur 
            sleep(0.1)
            matrix = sense.get_pixels() #Prends le resultat du dessin
            validation = vx() #Demande la validation du dessin
            if validation == True : #Si valide
                pro = False #Arrete la boucle
                return matrix #Retourne la matrice 
                