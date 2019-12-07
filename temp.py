from sense_hat import SenseHat
import time

sense = SenseHat()
sense.low_light = True
while True :
    event = sense.stick.wait_for_event() #attends le pressed
    temp = sense.get_temperature() # quand pressed, prend la t. 
    while event.action == "held" and event.direction == "middle" :
        #temps que le joystick est pressé prend une deuxieme t.
        tempb = sense.get_temperature()
        if tempb > temp + 0.3 : #si la t augmente, affiche du vert 
            sense.clear(0, 255, 0)
            time.sleep(2)
            sense.clear()
        if temp > tempb + 0.5 : #si la t diminue affiche du rouge
            sense.clear(255,0 , 0)
            time.sleep(2)
            sense.clear()