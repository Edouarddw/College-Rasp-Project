#!/usr/bin/env python3
from sense_hat import SenseHat
from subprocess import call
import module
import random

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
    while tourne :
        decode = module.key()
        sense.show_message("Valider?",scroll_speed = 0.05)
        v = module.vx() #VX est le return du choix entre V ou X
        if v :
            b = hashing("".join(decode)) # Si V alors la clef est conservee/hashee
            tourne = False # sors de la boucle qui permet d'entrer da clef 
        else :
            for event in sense.stick.get_events(): pass #reinitialise le compteur d actions
    f= open("secure.txt","r") #ouvre le document message.txt
    secure = f.read() #string strike = nombre d echecs
    f.close()
    if secure == "Y" or "y" :
        sequence = []
        matrix = module.secure_pixels()
        for liste in matrix :
            for number in liste :
                sequence.append(str(number)) #Ajoute tous les nombres de la matrice dans une liste en str
        sequence = "".join(sequence) #transforme la liste de string en chaine de carac
        b += hashing(sequence) #ajoute la sequence hasee a celle du gyroscopent
        testrandom = True
        testtemp = True
        rand = random.randint(9999,999999) #genere un chiffre aleatoire
        sense.show_message("message " + str(rand),scroll_speed = 0.05) #Montre un faux message genere aleatoirement avant test temp
        while testrandom : # test random : action a determiner en fonction de la parite du chiffre genere aleatoirement
            if rand % 2 == 0 : # si le chiffre genere aleatoirement est paire :
                testrandom = False
            else : # si le chiffre genere aleatoirement est impaire : 
                testrandom = False
        for event in sense.stick.get_events(): pass # reinitialise
        temp = sense.get_temperature() #Prend la temp.
        while testtemp : #test de la temperature : en fonction du nombre pixel dans le module de dessin, il faut augmenter ou diminuer la t.
            for event in sense.stick.get_events():
                if event.direction == "left" or event.direction == "right":
                    temp = sense.get_temperature() #Prend la temp.
                    
                if event.action == "held" and event.direction == "up": #si joystick maintenu vers le haut
                    tempb = sense.get_temperature() #Prend la temp une deuxieme fois
                    if tempb > temp + 0.3 and secure == "y": #Si la t augmente alors que le nombre de pixels colore dans l etape precedente etait paire
                        testtemp = False # la sequence est validee et le code continue
                    if secure =="Y": #Si n pixel etait impaire, vers le haut faux
                        b += "a" #rajoute un caractere errone a la sequence de hash
                        testtemp = False # la sequence continue de maniere erronee
                        
                if event.action == "held" and event.direction == "down": #si joystick maintenu vers le bas
                    tempb = sense.get_temperature() #Prend la temp une deuxieme fois
                    if tempb > temp + 0.3 and secure == "Y": #Si la t augmente alors que le nombre de pixels colore dans l etape precedente etait impaire
                        testtemp = False # la sequence continue de maniere erronee
                    if secure =="y": #Si n pixel etait paire vers le bas, faux
                        testtemp = False # la sequence est validee et le code continue
                        b += "a" #rajoute un caractere errone a la sequence de hash
                                        
    if b == a: # Si les deux hash sont similaires, on remet le compteur d echec a 0 et on lance le decodage
        ok = False
        f= open("fail.txt","w") #ouvre le document fail.txt
        f.write("") #remets le conteur a 0
        f.close()
        import decode.py #lance decode.py
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
        sense.clear(255,0 , 0)
        f= open("fail.txt","w") #ouvre le document fail.txt
        f.write("") #remets le conteur a 0
        f.close()
        call("sudo shutdown now", shell=True)