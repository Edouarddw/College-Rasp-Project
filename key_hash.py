
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

cle_pour_chiffrer = []
a = hashing(str(cle_pour_chiffrer))

cle_pour_dechiffrer =[]
b = hashing(str(cle_pour_dechiffrer))

if b == a:
    with open("key.txt", 'r') as f:
        print(f.read())
        sense.show_message(f.read())

