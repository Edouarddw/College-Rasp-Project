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
        sense.show_letter(str(len(liste_action)))
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