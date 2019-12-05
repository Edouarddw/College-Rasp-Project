from sense_hat import SenseHat

s = SenseHat()
s.low_light = True

#Cmt vérifier si un message est déjà enregistré ? Try open(message.txt) -> demander clé, except : entrer un message ? 

liste_action = []
action = 0

while True :
    event = s.stick.wait_for_event()
    if event.action == "pressed" and event.direction == "middle" :
        x = round(s.get_accelerometer_raw()["x"])
        y = round(s.get_accelerometer_raw()["y"])
        z = round(s.get_accelerometer_raw()["z"])
        if y == 0 and x == -1 and z == 0 : 
            action = "turnleft"
        if y == 0 and x == -1 and z == -1 :
            action = "flipleft"
        if y == 0 and x == 1 and z == 0 :
            action = "turnright"
        if y == 0 and x == 1 and z == -1 :
            action = "flipright"
        if y == 1 and x == 0 and z == 0 :
            action = "turnbackward"
        if y == -1 and x == 0 and z == 0 :
            action = "turnforward"
        if y == 0 and x == 0 and z == -1 :
            action = "flipbackward"
        liste_action.append(action)
    if event.action == "held" and event.direction == "middle" :
        break

key = hashing("".join(liste_action))



    
def hashing(string):
    """
    Hachage d'une chaîne de caractères fournie en paramètre.
    Le résultat est une chaîne de caractères.
    Attention : cette technique de hachage n'est pas suffisante (hachage dit cryptographique) pour une utilisation en dehors du cours.

    :param (str) string: la chaîne de caractères à hacher
    :return (str): le résultat du hachage
    """
    def to_32(value):
        """
        Fonction interne utilisée par hashing.
        Convertit une valeur en un entier signé de 32 bits.
        Si 'value' est un entier plus grand que 2 ** 31, il sera tronqué.

        :param (int) value: valeur du caractère transformé par la valeur de hachage de cette itération
        :return (int): entier signé de 32 bits représentant 'value'
        """
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
    