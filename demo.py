from subprocess import call
#Verifie s il y a un message enregistre, si oui lance le .py pour rentrer le mdp. S il n y en a pas lance message.py pour en rentrer un.
f= open("message.txt","r") #ouvre le document message.txt
message = f.read() #string message = contenu du doc
f.close()

if message == "" :
    call("python3 encode_key.py", shell=True) # Permet de rentrer la clef
else :
    call("python3 decode_key.py", shell=True) # Demande la clef