from sense_hat import SenseHat
from subprocess import call

sense = SenseHat()
sense.low_light = True


def hashing(string):

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


f= open("key.txt","r") # on cherche le hash de la clé d'encodage
a = f.read() # on definit la premiere variable a comme premier hash à comparer

#debut du code python qui va demander la clé permettant de dechiffrer le message

liste_action = [] #liste de stockage des positions dans l espace
action = 0
sense.show_message("Decode",scroll_speed = 0.05)
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
        conserver = True
        validation = True
        delete = False
        while validation :
            while conserver :
                sense.show_letter("V",(0, 255, 0))
                for event in sense.stick.get_events(): # Si on valide en appuyant au milieu, le message sera conserve, une autre action proposera le x
                    if event.action == 'pressed' and event.direction == "middle":
                        tourne = False
                        conserver = False
                        validation = False
                        sense.clear()
                        f= open("key.txt","a") #ouvre le document message.txt
                        f.write(hashing("".join(liste_action))) #ecrit la clef hashee
                        f.close()
                        call("python3 message.py", shell=True) #lance message.py
                    if event.action == "pressed" and event.direction != "middle" :
                        conserver = False
                        delete = True
            while delete :
                sense.show_letter("X",(255, 0, 0))
                for event in sense.stick.get_events(): # Si on valide en appuyant au milieu, le message sera supprime, une autre action recommencera la bouche
                    if event.action == 'pressed' and event.direction == "middle":
                        delete = False
                        validation = False
                        sense.clear()
                        liste_action = []
                    if event.action == "pressed" and event.direction != "middle" :
                        conserver = True
                        delete = False


f= open("key.txt","r") # on cherche le hash de la clé d'encodage
b = f.read() # on definit la deuxieme variable b comme deuxieme hash à comparer


if b == a: #on compare les deux hash, si ils sont egaux(clé la meme) alors on ouvre le 'message.txt' et on l'affiche
    with open("message.txt", 'r') as f:
        print(f.read()) #affiche le message sur la console
        sense.show_message(f.read()) #affiche le message sur le senseHat

