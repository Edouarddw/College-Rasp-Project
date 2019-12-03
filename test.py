
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
    print(dec)
    return (dec)

f = open("message.txt", "w") #ouvre un .txt
f.write(encode ("chocolat","0497883266")) #ecrit le message chiffre 
f.close()