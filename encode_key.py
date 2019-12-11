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
sense.show_message("High Security?", scroll_speed = 0.04)
security = module.vx()
sense.show_message("Encode:",scroll_speed = 0.05)
while tourne :
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

if security == True :
    f= open("secure.txt","w") #ouvre le document secure.txt
    f.write("Y") #enregistre que c est high secure
    f.close()
    sequence = module.secure_pixels()
    f= open("key.txt","a") #ouvre le document message.txt
    f.write(hashing(sequence)) #ecrit la clef hashee
    f.close()
else :
    f= open("secure.txt","w") #ouvre le document secure
    f.write("") #remets a 0 le high secure
    f.close()
import message.py #lance message.py