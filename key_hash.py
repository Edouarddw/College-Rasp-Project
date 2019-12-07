import encode_key


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

cle_pour_chiffrer = encode_key.liste_action  #la suite de mouvements qui notre clé pour encoder le message
a = hashing(str(cle_pour_chiffrer)) #on hash cette clé

#il faut un code pour permettre de rentrer la clé et la stocker dans la liste juste en dessous

cle_pour_dechiffrer =[] # clé pour essayer d'ouvrir le message
b = hashing(str(cle_pour_dechiffrer)) # on hash cette clé aussi

if b == a: #on compare les deux hash, si ils sont egaux(clé la meme) alors on ouvre le 'message.txt' et on l'affiche
    with open("message.txt", 'r') as f:
        print(f.read()) #affiche le message sur la console
        sense.show_message(f.read()) #affiche le message sur le senseHat

