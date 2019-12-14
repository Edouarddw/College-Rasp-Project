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


#Regarde si un faux message a deja ete encode pour une ouverture precedente du message. Si l on ouvre le vrai message, c est aussi remis a 0 p
#Pour que voir quelqu'un rentrer la clef de deverouillage complete ne suffise pas.
f = open ("fmessage.txt","r")
rand = f.read()
f.close ()
# S'il n'y en avait pas, on en cree un nouveau et on l'enregistre dans le .txt
if rand == "" :
    rand = random.randint(9999,999999) #genere un faux message aleatoirement, affiche en mode secure si le test de gyro et dessin sont passes
    f = open ("fmessage.txt","w")
    f.write(str(rand))
    f.close ()
    
    

sense.show_message("Decode",scroll_speed = 0.05)
tourne = True # permet de rentrer a nouveau la suite de mouvements dans l espace si on choisit X lors de module.vx
c = "" # String ajoutee au hash. Dans le mode secure, elle contient "a" si les parties gyroscope et dessin ont ete validees. 
ok = True # Permet de reessayer si le code est errone (enregistre une erreur dans "strike" à chaque itération) 
while ok :
    if c== "" : # Si dans le mode secure on a pas encore accede a la partie test de parite 
                # l'objectif est de ne pas montrer qu une erreur a ete comise lors du dernier test car cela indiquerait que le message etait un faux
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
            
            if b == a : # si les sequences du gyroscope et du dessin sont correctes
                c = "a" # ajout d'un caractere errone au hash (cfr:ligne 118) passes la partie dessin et gyro
                sense.show_message("message", scroll_speed = 0.05 ) # deux show message differents pour que le mot soit plus rapide que les chiffres
                sense.show_message(str(rand),scroll_speed = 0.08) #Montre un faux message genere aleatoirement avant le test de parite
        
    if secure == "Y" or secure == "y" and c != "" : # ne peut pas etre compris dans le if ligne 58 pour ne pas repeter toute la sequence en cas d erreur au seins de testparite
        testparite = True # permet de faire tourner le test de direction du joystick et de temperature temps qu'il n'a pas ete valide
        temp = sense.get_temperature() #Prend la temp.
        while testparite : #test de parités : on doit valider la bonne sequence en fonction de la parite du message secret et du nombre de pixels contenu dans le dessin
            for event in sense.stick.get_events():
                if event.direction == "left" or event.direction == "right": #Les joysticks vers la gauche ou la droite permettent de reprendre la t de comparaison
                    temp = sense.get_temperature() #Prend la temp.
                # Si le message est paire, le joystick doit etre orriente vers le haut et vice-versa
                # Si le nombre de pixels dans le dessin valide est pair, il faut creer une augmentation de temperature et vice-versa 
                
                if event.action == "held" and event.direction == "up" and rand % 2 == 0: #si joystick maintenu vers le haut et que le message aleatoire est paire
                    tempb = sense.get_temperature() #Prend la temp une deuxieme fois
                    #On est oblige de mettre toutes les possibilites car un esle: omettrait les imperfections des capteurs qui font que parfois rien n est detecte
                    if tempb > temp + 0.3 and secure == "y" : # si la t augmente et que le nombre de pixel enregistré dans encode_key est pair
                        testparite = False # la sequence est validee et le code continue
                        c = "" # remets le compteur a 0 pour que a == b 
                    if temp > tempb + 0.5 and secure == "y" : # Si la t diminue alors qu'on etait cense l'augmenter
                        testparite = False # la sequence est validee avec le hash errone
                                
                    if tempb < temp + 0.5 and secure == "Y" : # si la t diminue et que le nombre de pixel enregistré dans encode_key est impair
                        testparite = False # la sequence est validee et le code continue
                        c = "" # remets le compteur a 0 pour que a == b
                    if temp < tempb + 0.3 and secure == "Y" : # Si la t augmente alors qu'on etait cense diminuer
                        testparite = False # la sequence est validee avec le hash errone                        
                if event.action == "released" and event.direction == "up" and rand % 2 != 0 : # si le message aleatoire est impaire, continue avec hash errone
                        testparite = False # la sequence continue de maniere erronee
                        
                            
                if event.action == "held" and event.direction == "down" and rand % 2 != 0: #si joystick maintenu vers le bas et que le message aleatoire est impaire
                    tempb = sense.get_temperature() #Prend la temp une deuxieme fois
                    #On est oblige de mettre toutes les possibilites car un esle: omettrait les imperfections des capteurs qui font que parfois rien n est detecte
                    if tempb > temp + 0.3 and secure == "y" : # si la t augmente et que le nombre de pixel enregistré dans encode_key est pair
                        testparite = False # la sequence est validee et le code continue
                        c = "" # remets le compteur a 0 pour que a == b 
                    if temp > tempb + 0.5 and secure == "y" : # Si la t diminue alors qu'on etait cense l'augmenter
                        testparite = False # la sequence est validee avec le hash errone
                                                    
                    if tempb < temp + 0.5 and secure == "Y" : # si la t diminue et que le nombre de pixel enregistré dans encode_key est impair
                        testparite = False # la sequence est validee et le code continu
                        c = "" # remets le compteur a 0 pour que a == b e
                    if temp < tempb + 0.3 and secure == "Y" : # Si la t augmente alors qu'on etait cense diminuer
                        testparite = False # la sequence est validee avec le hash errone                        
                if event.action == "released" and event.direction == "down" and rand % 2 == 0 : # si le message aleatoire est paire, continue avec hash errone
                        testparite = False # la sequence continue de maniere erronee
                
    if b + c == a: # Si les deux hash sont similaires, on remet le compteur d echec a 0, le faux message et  on lance le decodage
        ok = False
        f= open("fail.txt","w") #ouvre le document fail.txt
        f.write("") #remets le conteur a 0
        f.close()
        f = open ("fmessage.txt","w") #ouvre fmessage.txt
        f.write("") #remets a 0
        f.close ()
        import decode.py #lance decode.py
    else : #sinon on augmente le compteur de 1
        f= open("fail.txt","a") #ouvre le document fail.txt en mode .append
        f.write("I") #ajoute un strike
        f.close()
        tourne = True 
    f= open("fail.txt","r") #ouvre le document message.txt
    strike = f.read() #string strike = nombre d echecs
    f.close()
    if c == "" and b + c != a: # ne previens pas si mode secure et que le faux message a ete donne car la sequence etait correcte
        #Objectif : faire croire que le message a bien ete donne
        # and ... pour ne pas afficher a nouveau si le compteur n a pas ete augmente car la sequence est correcte
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