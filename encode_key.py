from sense_hat import SenseHat
from subprocess import call
import module 

sense = SenseHat()
sense.low_light = True

def hashing(string): #fonction hachant la clef
    
    def to_32(value):
        value = value % (2 ** 32)
        if value >= 2**31:
            value = value - 2 ** 32
        value = int(value)
        return value

    if string:
        x = ord(string[0]) << 7
        m = 1000003
        for c in string:
            x = to_32((x*m) ^ ord(c))
        x ^= len(string)
        if x == -1:
            x = -2
        return str(x)
    return ""

liste_action = [] #liste de stockage des positions dans l espace
action = 0
sense.show_message("Encode",scroll_speed = 0.05)
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
    if event.action == "held" and event.direction == "middle" :
        sense.show_message("Valider?",scroll_speed = 0.05)
        a = module.vx() #VX est le return du choix entre V ou X
        if a :
            tourne = False 
            f= open("key.txt","w") #ouvre le document message.txt
            f.write(hashing("".join(liste_action))) #ecrit la clef hashee
            f.close()
            call("python3 message.py", shell=True) #lance message.py
            
        else :
            liste_action = []
            for event in sense.stick.get_events(): pass #reinitialise le compteur d actions