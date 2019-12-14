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
tourne = True # permet de rentrer a nouveau la suite de mouvements dans l espace si on choisit X lors de module.vx
c = "" # String s'ajoutant au hash contenant "a" si une erreur a ete comise au sein de testparite ( apd ligne 69 ) 
ok = True # Permet de reessayer si le code est errone
while ok :
    if c!= "" : # Si aucune erreur n'a ete comise dans le mode "secure" au sein du module testparite
                # l'objectif est de ne pas montrer qu une erreur a ete comise lors du dernier testt car cela indiquerait que le message etait un faux
        while tourne : 
            decode = module.key()
            sense.show_message("Valider?",scroll_speed = 0.05)
            v = module.vx() #VX est le return du choix entre V ou X
            if v :
                b = hashing("".join(decode)) # Si V alors la clef est conservee/hashee
                tourne = False # sors de la boucle qui permet d'entrer da clef 
            else :
                for event in sense.stick.get_events(): pass #reinitialise le compteur d actions
        f= open("secure.txt","r") #ouvre le document secure.txt
        secure = f.read()
        f.close()
        if secure == "Y" or secure == "y" : # Si le mode secure a ete enregistre
            sequence = []
            matrix = module.secure_pixels()
            for liste in matrix :
                for number in liste :
                    sequence.append(str(number)) #Ajoute tous les nombres de la matrice dans une liste en str
            sequence = "".join(sequence) #transforme la liste de string en chaine de carac
            b += hashing(sequence) #ajoute la sequence hasee a celle du gyroscopent
            testparite = True
            rand = random.randint(9999,999999) #genere un chiffre aleatoire
            sense.show_message("message " + str(rand),scroll_speed = 0.05) #Montre un faux message genere aleatoirement avant test temp
            for event in sense.stick.get_events(): pass # reinitialise
        
    if secure == "Y" or secure == "y" : # ne peut pas etre compris dans le if ligne 58 pour ne pas repeter toute la sequence en cas d erreur au seins de testparite
        testparite = True # permet de faire tourner le test de direction du joystick et de temperature temps qu'il n'a pas ete valide
        temp = sense.get_temperature() #Prend la temp.
        while testparite : #test de parités : on doit valider la bonne sequence en fonction de la parite du message secret et du nombre de pixels contenu dans le dessin
            for event in sense.stick.get_events():
                if event.direction == "left" or event.direction == "right": #Les joysticks vers la gauche ou la droite permettent de reprendre la t de comparaison
                    temp = sense.get_temperature() #Prend la temp.
                # Si le message est paire, le joystick doit etre orriente vers le haut et vice-versa
                # Si le nombre de pixels dans le dessin valide est pair, il faut creer une augmentation de temperature et vice-versa 
                
                  if event.action == "held" and event.direction == "up": #si joystick maintenu vers le haut
                    tempb = sense.get_temperature() #Prend la temp une deuxieme fois
                    if rand % 2 == 0 : # Si le message genere aleatoirement est paire
                        #On est oblige de mettre toutes les possibilites car un esle: omettrait les imperfections des capteurs qui font que parfois rien n est detecte
                        if tempb > temp + 0.3 and secure == "y" : # si la t augmente et que le nombre de pixel enregistré dans encode_key est pair
                            testparite = False # la sequence est validee et le code continue
                        if temp > tempb + 0.5 and secure == "y" : # Si la t diminue alors qu'on etait cense l'augmenter
                            c = "a" #rajoute un caractere errone a la sequence de hash
                            testparite = False # la sequence est validee avec le hash errone
                                
                        if tempb < temp + 0.5 and secure == "Y" : # si la t diminue et que le nombre de pixel enregistré dans encode_key est impair
                            testparite = False # la sequence est validee et le code continue
                        if temp < tempb + 0.3 and secure == "Y" : # Si la t augmente alors qu'on etait cense diminuer
                            c = "a" #rajoute un caractere errone a la sequence de hash
                            testparite = False # la sequence est validee avec le hash errone                        
                    else : 
                        c = "a" #rajoute un caractere errone a la sequence de hash
                        testparite = False # la sequence continue de maniere erronee
                        
                            
                if event.action == "held" and event.direction == "down": #si joystick maintenu vers le bas
                    tempb = sense.get_temperature() #Prend la temp une deuxieme fois
                    if rand % 2 != 0 : # SI le message genere aleatoirement est impaire
                        #On est oblige de mettre toutes les possibilites car un esle: omettrait les imperfections des capteurs qui font que parfois rien n est detecte
                        if tempb > temp + 0.3 and secure == "y" : # si la t augmente et que le nombre de pixel enregistré dans encode_key est pair
                            testparite = False # la sequence est validee et le code continue
                        if temp > tempb + 0.5 and secure == "y" : # Si la t diminue alors qu'on etait cense l'augmenter
                            c = "a" #rajoute un caractere errone a la sequence de hash
                            testparite = False # la sequence est validee avec le hash errone
                                                    
                        if tempb < temp + 0.5 and secure == "Y" : # si la t diminue et que le nombre de pixel enregistré dans encode_key est impair
                            testparite = False # la sequence est validee et le code continue
                        if temp < tempb + 0.3 and secure == "Y" : # Si la t augmente alors qu'on etait cense diminuer
                            c = "a" #rajoute un caractere errone a la sequence de hash
                            testparite = False # la sequence est validee avec le hash errone                        
                    else : 
                        c = "a" #rajoute un caractere errone a la sequence de hash
                        testparite = False # la sequence continue de maniere erronee
                
                if event.action == "held" and event.direction == "middle": #si joystick maintenu vers le centre
                    sense.show_message("recommencer?",scroll_speed = 0.05)
                    b += "a" #ajoute un caractere errone a b pour que la sequence ne soit pas validee mais que c reste "" pour pouvoir recommencer depuis le debut
                    testparite = False 
    if b + c == a: # Si les deux hash sont similaires, on remet le compteur d echec a 0 et on lance le decodage
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
    if secure == "" : # ne previens pas si le mode secure etait selectionne et qu une erreur a ete comise. Objectif : faire croire que le message a bien ete donne
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