from sense_hat import SenseHat
from subprocess import call
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
tourne = True 
conserver = True
sup = True 
sense.show_message("Conserver?",scroll_speed = 0.05)
while tourne :
  while conserver :
    sense.show_letter("V",(0, 255, 0))
    for event in sense.stick.get_events(): # Si on valide en appuyant au milieu, le message sera conserve, une autre action proposera le x 
      if event.action == 'pressed' and event.direction == "middle":
        tourne = False
        conserver = False
        sense.clear()
        call("sudo shutdown now", shell=True) #stop le rasp
      if event.action == "pressed" and event.direction != "middle" :
        conserver = False
        delete = True
  while delete :
    sense.show_letter("X",(255, 0, 0))
    for event in sense.stick.get_events(): # Si on valide en appuyant au milieu, le message sera supprime, une autre action recommencera la bouche 
      if event.action == 'released' and event.direction == "middle":
          #permet de choisir entre enregistrer un a nouveau clef et message ou non si non, eteint le rasp
          sense.show_message("Nouveau?",scroll_speed = 0.05)
          while tourne :
                  while conserver :
                      sense.show_letter("V",(0, 255, 0))
                      for event in sense.stick.get_events(): # Si on valide en appuyant au milieu, le message sera conserve, une autre action proposera le x
                          if event.action == 'pressed' and event.direction == "middle":
                              tourne = False
                              conserver = False 
                              sense.clear()
                              call("python3 encode_key.py", shell=True) #lance l encodage d une nouvelle clef
                          if event.action == "pressed" and event.direction != "middle" :
                              conserver = False
                              sup = True
                  while sup :
                      sense.show_letter("X",(255, 0, 0))
                      for event in sense.stick.get_events(): # Si on valide en appuyant au milieu, le message sera supprime, une autre action recommencera la bouche
                          if event.action == 'pressed' and event.direction == "middle":
                              sup = False
                              delete = False
                              tourne = False
                              f= open("message.txt","w") #ouvre le document message.txt
                              f.write("") #remplace par un message vide donc supprime
                              f.close()
                              sense.clear()
                              call("sudo shutdown now", shell=True) #stop le rasp
                          if event.action == "pressed" and event.direction != "middle" :
                              sup = False
                              conserver = True
      if event.action == "pressed" and event.direction != "middle" :
        conserver = True
        delete = False