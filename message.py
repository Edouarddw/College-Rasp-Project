#!/usr/bin/env python3
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from signal import pause
from time import sleep
from subprocess import call
x = 0 #Valeur initial du compteur = 0
sense = SenseHat()
Message = [] # Liste de stockage des caracteres du message
key= "chocolat" # Clef du chiffrement vigenere
sense.low_light = True 
lock = True #False si un message est deja enregistre
sense.show_letter(str(x)) #affiche le caractere des le debut 
def encode(key, plain_text ): #Fonction chiffrant le message selon le chiffrement vigenere
    
    enc = []
    for i, e in enumerate(plain_text):
        key_c = key[i % len(key)]
        enc_c = chr((ord(e) + ord(key_c)) % 256)
        enc.append(enc_c)
    return ("".join(enc).encode()).decode()
    
def decode(key, cipher_text): #Fonction dechiffrant le message selon le chiffrement vigenere
    
   
    dec = []
    for i, e in enumerate(cipher_text):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(e) - ord(key_c)) % 256)
        dec.append(dec_c)
    dec= str("".join(dec))
    return (dec)


def value(value, min_value=0, max_value=9): #Fonction limitant la valeur des caractere du message a des chiffres
    # Permet de defiler en continu dans les chiffres
    if value > 9 : value=0
    if value < 0 : value=9
    return min(max_value, max(min_value, value))


def Plus(event): #Fonction augmentant la valeur
    global x
    if event.action != ACTION_RELEASED:
        x = value(x + 1)
        sense.show_letter(str(x))
        

def Moins(event): #Fonction diminuant la valeur
    global x
    if event.action != ACTION_RELEASED:
        x = value(x - 1)
        sense.show_letter(str(x))

def Confirm(event): #Press ajoute la lettre. Hold confirme le message 
    global Message
    global lock
    tourne = True
    conserver = True
    if event.action != ACTION_PRESSED:
        if lock :
            if event.action == ACTION_RELEASED:
                sense.show_letter(str(x),(0, 255, 0)) #le caractere devient vert ( confirmation )
                Message.append(str(x)) #ajout du caractere a la string Message
                sleep(0.2)
                sense.show_letter(str(x)) #le caractere redevient blanc
            else: #Longue pression 
                f = open("message.txt", "w") #ouvre un .txt
                f.write(encode(key,"".join(Message))) #ecrit le message chiffre 
                f.close()
                sense.clear()
                lock = False #Permet d enregistrer qu une fois
                
        elif event.action != ACTION_HELD:
            sense.show_message("".join(Message),scroll_speed = 0.05) #Montre le message valide
            sense.show_message("Confirmer?",scroll_speed = 0.05) 
            while tourne : #tourne temps qu on a pas valide
                while conserver :
                    sense.show_letter("V",(0, 255, 0))
                    for event in sense.stick.get_events(): # Si on valide en appuyant au milieu, le message sera conserve, une autre action proposera le x 
                        if event.action == 'pressed' and event.direction == "middle":
                           tourne = False
                           sense.clear()
                           call("sudo shutdown now", shell=True) #stop le rasp
                        if event.action == "pressed" and event.direction != "middle" :
                           conserver = False
                           delete = True
                while delete :
                    sense.show_letter("X",(255, 0, 0))
                    for event in sense.stick.get_events(): # Si on valide en appuyant au milieu, on peut remettre un message, une autre action recommencera la boucle 
                        if event.action == 'pressed' and event.direction == "middle":
                           lock = True
                           delete = False
                           tourne = False
                           Message = [] #supprime les caracteres enregistre
                           sense.show_letter(str(x))
                        if event.action == "pressed" and event.direction != "middle" :
                           conserver = True
                           delete = False

sense.stick.direction_up = Plus #Joystick vers le haut : valeur +1
sense.stick.direction_down = Moins #Joystick vers le bas : valeur -1
sense.stick.direction_left = Moins #Joystick vers la gauche : chiffrement et .txt
sense.stick.direction_right = Plus #Joystick vers la droite : valeur +1
sense.stick.direction_middle = Confirm #press ajout au message hold confirmer
pause() 