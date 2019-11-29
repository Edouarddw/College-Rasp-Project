from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from signal import pause
from time import sleep

x = 0 #Valeur initial du compteur = 0
sense = SenseHat()
Message = [] # Liste de stockage des caractère du message
key= "chocolat" # Clé du chiffrement vigenere
sense.low_light = True

def encode(key, plain_text ): #Fonction chiffrant le message selon le chiffrement vigenere
    
    enc = []
    for i, e in enumerate(plain_text):
        key_c = key[i % len(key)]
        enc_c = chr((ord(e) + ord(key_c)) % 256)
        enc.append(enc_c)
    return ("".join(enc))#.encode()).decode()
    
def decode(key, cipher_text): #Fonction déchiffrant le message selon le chiffrement vigenere
    
   
    dec = []
    for i, e in enumerate(cipher_text):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(e) - ord(key_c)) % 256)
        dec.append(dec_c)
    dec= str("".join(dec))
    print(dec)
    return (dec)


def value(value, min_value=0, max_value=9): #Fonction limitant la valeur des caractère du message à des chiffres
    # Permet de défiler en continu dans les chiffres
    if value > 9 : value=0
    if value < 0 : value=9
    return min(max_value, max(min_value, value))


def pushed_up(event): #Fonction augmentant la valeur
    global x
    if event.action != ACTION_RELEASED:
        x = value(x + 1)
        sense.show_letter(str(x))
        

def pushed_down(event): #Fonction diminuant la valeur
    global x
    if event.action != ACTION_RELEASED:
        x = value(x - 1)
        sense.show_letter(str(x))

        
def pushed_left(event): #Fonction faisant appel à la fonction "encode" pour écrire le message chiffré dans .txt
    global Message
    global key
    if event.action != ACTION_HELD:
        f = open("message.txt", "w")
        f.write(encode(key,"".join(Message)))
        f.close()
        sense.clear()
        
#Enlever les # pour test. la fonction devrait renvoyer le message en clair dans la console        
#    if event.action != ACTION_RELEASED:
#      print (decode(key,encode(key,Message)))
#      sense.clear()

def pushed_right(event): #Fonction ajoutant un caractère au message
  global x
  global Message
  if event.action != ACTION_RELEASED:
      sense.show_letter(str(x),(0, 255, 0)) #le caractère devient vert ( confirmation )
      Message.append(str(x)) #ajout du caractère à la string Message
      sleep(0.2)
      sense.show_letter(str(x)) #le caractère redevient blanc
      
#Objectif : Pression Joystick pour ajouter un caractère, longue pression pour finir le message.
        #   Remplacerait donc le Joystick vers la gauche et droite
#Problème : incapacité de définir une longue pression.
#def confirm(event):
#    global Message
#    if event.action != ACTION_HELD:
#      f = open("message.txt", "w")
#      f.write(encode(key,"".join(Message)))
#      f.close()
#    if event.action != ACTION_RELEASED:
#        Message.append[str(x)]
    

sense.stick.direction_up = pushed_up #Joystick vers le haut : valeur +1
sense.stick.direction_down = pushed_down #Joystick vers le bas : valeur -1
sense.stick.direction_left = pushed_left #Joystick vers la gauche : chiffrement et .txt
sense.stick.direction_right = pushed_right #Joystick vers la droite : ajout d'un caractère au message
#sense.stick.direction_middle = confirm
pause()

