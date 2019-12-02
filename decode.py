key= "chocolat"
    
def decode(key, cipher_text): #Fonction dechiffrant le message selon le chiffrement vigenere
    
   
    dec = []
    for i, e in enumerate(cipher_text):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(e) - ord(key_c)) % 256)
        dec.append(dec_c)
    dec= str("".join(dec))
    print(dec)
    return (dec)


f= open("message.txt","r")
message = f.read()
f.close()

sense.show_message(decode(key,message))

