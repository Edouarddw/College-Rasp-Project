#code a implementer dans le code de validation de la clef lors du decryptage.
#si la clef est la bonne, il remet le compteur a 0
#sinon, il l augmente de 1, si celui-ci atteint 3, le message est supprime
#le compteur est sauvegarde sur un .txt comme ca eteindre et rallumer le rasp ne laisse pas plus d opportunités 


a = "000" # emprunte rentree
f= open("key.txt","r") #ouvre le document key.txt
b = f.read() #string b = emprunte conservee 
f.close()

if a == b : # si identique, remettre le compteur a 0 
    f= open("fail.txt","w") #ouvre le document fail.txt
    f.write("") #remets le conteur a 0
    f.close()
else : #sinon l augmenter de 1
    f= open("fail.txt","a") #ouvre le document fail.txt en mode .append
    f.write("I") #ajoute un strike
    f.close()

f= open("fail.txt","r") #ouvre le document message.txt
strike = f.read() #string strike = nombre d echecs
f.close()
if strike == "III" : # Si le compteur atteint 3, suppression du message secret 
    f= open("message.txt","w") #ouvre le document message.txt
    f.write("") #remplace par un message vide donc supprime
    f.close()