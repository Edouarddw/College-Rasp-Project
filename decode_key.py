from sense_hat import SenseHat
from subprocess import call
import module

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


f= open("key.txt","r") # on cherche le hash de la cle d'encodage
a = f.read() # on definit la premiere variable a comme premier hash a comparer
f.close()
#debut du code python qui va demander la cle permettant de dechiffrer le message

sense.show_message("Decode",scroll_speed = 0.05)
tourne = True
ok = True # Permet de reessayer si le code est errone
while ok :
    action = 0
    liste_action = [] #liste de stockage des positions dans l espace
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
            v = module.vx() #VX est le return du choix entre V ou X
            if v :
                b = hashing("".join(liste_action)) # Si V alors la clef est conservee/hashee
                tourne = False # sors de la boucle qui permet d'entrer da clef 
            else :
                liste_action = [] # Si X, remets la liste a 0 et relance la boucle de selection
                for event in sense.stick.get_events(): pass #reinitialise le compteur d actions

    if b == a: # Si les deux hash sont similaires, on remet le compteur d echec a 0 et on lance le decodage
        ok = False
        f= open("fail.txt","w") #ouvre le document fail.txt
        f.write("") #remets le conteur a 0
        f.close()
        call("python3 decode.py", shell=True) #lance decode.py
    else : #sinon on augmente le compteur de 1
        f= open("fail.txt","a") #ouvre le document fail.txt en mode .append
        f.write("I") #ajoute un strike
        f.close()
        tourne = True 
    f= open("fail.txt","r") #ouvre le document message.txt
    strike = f.read() #string strike = nombre d echecs
    f.close()
    if strike == "I": 
        sense.show_message("FAUX",scroll_speed = 0.05, text_colour = (255, 0, 0))
    if strike == "II":
        sense.show_message("Derniere chance",scroll_speed = 0.04, text_colour = (255, 0, 0))
    if strike == "III" : # Si le compteur atteint 3, suppression du message secret
        ok = False
        f= open("message.txt","w") #ouvre le document message.txt
        f.write("") #remplace par un message vide donc supprime
        f.close()
        print ("a")
        sense.clear(255,0 , 0)
        f= open("fail.txt","w") #ouvre le document fail.txt
        f.write("") #remets le conteur a 0
        f.close()
        call("sudo shutdown now", shell=True)