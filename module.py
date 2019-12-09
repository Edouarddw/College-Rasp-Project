from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
sense = SenseHat()
from time import sleep

def vx() :
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
                if event.action == "pressed" and event.direction != "middle" :
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
                if event.action == "pressed" and event.direction != "middle" :
                    conserver = True
                    delete = False
def key() :
    liste_action = [] #liste de stockage des positions dans l espace
    action = 0
    tourne = True
    while tourne :
        if len(liste_action) < 10 :
            sense.show_letter(str(len(liste_action)))
        else :
            sense.show_message(str(len(liste_action)))
        event = sense.stick.wait_for_event()
        if event.action == "pressed" and event.direction == "middle" : #pression sur le joystick pour ajouter une position
            x = round(sense.get_accelerometer_raw()["x"])
            y = round(sense.get_accelerometer_raw()["y"])
            z = round(sense.get_accelerometer_raw()["z"])
            if y == 0 and x == 0 and z == 1 :
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
        if event.action == "held" and event.direction == "middle" : return liste_action
        
        
def secure_pixels() :
    """Ajoute un dessin a effectuer en entrant la cle"""
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
            
        if event.direction == "down" and event.action == "held" : # clean l'ecran
            sense.clear()
            
        if event.direction == "up" and event.action == "held" : #quand validation
            sense.set_pixel(x,y,nothing) #efface le curseur
            validation = vx() #Demande la validation du dessin
            if validation == True : #Si valide
                pro = False #Arrete la boucle
                matrix = sense.get_pixels() #Prends le resultat du dessin
                sequence = []
                for liste in matrix :
                    for number in liste :
                        sequence.append(str(number)) #Ajoute tous les nombres de la matrice dans une liste en str
                "".join(sequence) #transforme la liste de string en chaine de carac
                return sequence