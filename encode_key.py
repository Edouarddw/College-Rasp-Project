#!/usr/bin/env python3
from sense_hat import SenseHat
import module 

sense = SenseHat()
sense.low_light = True
tourne = True 

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
sense.show_message("High Security?", scroll_speed = 0.05) #Demande si on veut le mode secure ou rapide
security = module.vx() #module permettant de choisir V ou X si V, on lance le mode secure sinon rapide
sense.show_message("Encode:",scroll_speed = 0.05)
while tourne : #Permet d'encoder la partie de la cle utilisant l'accelerometre
    encode = module.key()
    sense.show_message("Valider?",scroll_speed = 0.05)
    a = module.vx() #VX est le return du choix entre V ou X
    if a :
        tourne = False 
        f= open("key.txt","w") #ouvre le document message.txt
        f.write(hashing("".join(encode))) #ecrit la clef hashee
        f.close()
    else :
        for event in sense.stick.get_events(): pass #reinitialise le compteur d actions

if security == True : #Si le mode secure avait ete enregistre 
    f= open("secure.txt","w") #ouvre le document secure.txt
    f.write("Y") #enregistre que c est high secure
    f.close()
    sequence = []
    colore = 0
    matrix = module.secure_pixels() #lance le module secue_pixels permettant de rentrer un code sous forme de dessin, renvoie une liste de rgb
    for liste in matrix :
        if liste != [0, 0, 0] : #Compte le nbr de pixels colore
            colore += 1
        for number in liste :
            sequence.append(str(number)) #Ajoute tous les nombres de la matrice dans une liste en str
    sequence = "".join(sequence) #transforme la liste de string en chaine de carac
    if colore % 2 == 0 : #si le nombre de pixel colore est paire, enregistre un y minuscule a la place de la majuscule dans secure.txt, sera recupere dans decode_key
        f= open("secure.txt","w") #ouvre le document secure.txt
        f.write("y") #enregistre que c est high secure
        f.close()
    f= open("key.txt","a") #ouvre le document message.txt
    f.write(hashing(sequence)) #ecrit la clef hashee
    f.close()
else :
    f= open("secure.txt","w") #ouvre le document secure
    f.write("") #remets a 0 le high secure
    f.close()
import message.py #lance message.py