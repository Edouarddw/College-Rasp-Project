from sense_hat import SenseHat
from subprocess import call
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
while tourne :
    encode = module.key()
    sense.show_message("Valider?",scroll_speed = 0.05)
    a = module.vx() #VX est le return du choix entre V ou X
    if a :
        tourne = False 
        f= open("key.txt","w") #ouvre le document message.txt
        f.write(hashing("".join(encode))) #ecrit la clef hashee
        f.close()
        call("python3 message.py", shell=True) #lance message.py
            
    else :
        for event in sense.stick.get_events(): pass #reinitialise le compteur d actions
    