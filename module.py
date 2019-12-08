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