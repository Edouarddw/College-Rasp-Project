from sense_hat import SenseHat
from subprocess import call
import module
sense = SenseHat()
sense.clear()
key= "chocolat" #clef introduite lors de l encodage
tourne = True # defile jusqu a pression
sense.low_light = True

def decode(key, cipher_text): #Fonction dechiffrant le message selon le chiffrement vigenere
    
   
    dec = []
    for i, e in enumerate(cipher_text):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(e) - ord(key_c)) % 256)
        dec.append(dec_c)
    dec= str("".join(dec))
    return (dec)


f= open("message.txt","r") #ouvre le document message.txt
message = f.read() #string message = contenu du doc
f.close()
x= decode(key,message)
while tourne :
    sense.show_message(decode(key,message),scroll_speed = 0.05) #montre sur le rasp le message decode
    for event in sense.stick.get_events():
      if event.action == 'pressed':
        sense.clear()
        tourne = False

sense.show_message("Conserver?",scroll_speed = 0.05)
a = module.vx() #VX est le return du choix entre V ou X
if a :
    call("sudo shutdown now", shell=True) # V = stop le rasp
else : # X = message supprime, une autre action recommencera la boucle
    f= open("secure.txt","w") #ouvre le document secure
    f.write("") #remets a 0 le high secure
    f.close()
    #permet de choisir entre enregistrer un a nouveau clef et message ou non si non, eteint le rasp
    sense.show_message("Nouveau?",scroll_speed = 0.05)
    b = module.vx() #VX est le return du choix entre V ou X
    if b : import encode_key.py #lance l encodage d une nouvelle clef
    else :
        f= open("message.txt","w") #ouvre le document message.txt
        f.write("") #remplace par un message vide donc supprime
        f.close()
        call("sudo shutdown now", shell=True) #stop le rasp