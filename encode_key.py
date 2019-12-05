from sense_hat import SenseHat

s = SenseHat()
s.low_light = True

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
            liste_action.append(action)
        if y == 0 and x == -1 and z == -1 :
            action = "flipleft"
            liste_action.append(action)
        if y == 0 and x == 1 and z == 0 :
            action = "turnright"
            liste_action.append(action)
        if y == 0 and x == 1 and z == -1 :
            action = "flipright"
            liste_action.append(action)
        if y == 1 and x == 0 and z == 0 :
            action = "turnbackward"
            liste_action.append(action)
        if y == -1 and x == 0 and z == 0 :
            action = "turnforward"
            liste_action.append(action)
        if y == 0 and x == 0 and z == -1 :
            action = "flipbackward"
            liste_action.append(action) 
    if event.action == "held" and event.direction == "middle" :
        break

key = hashing("".join(liste_action))
    