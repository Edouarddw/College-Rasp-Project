
from sense_hat import SenseHat
from time import sleep
sense = SenseHat()
sense.clear()
sense.low_light = True

def roll():

	if 0<roll<=90:
		#afficher inclinaison gauche de l'appareil
		sense.show_letter("g")
	elif 270<=roll<=360:
		#afficher inclinaison droite de l'appareil
		sense.show_letter("d")
	else:
		#afficher appareil à l'envers
		sense.show_letter("x")

def pitch():

	if 270 <=pitch<=360:
		#affiche decolage, nez levé
		sense.show_letter("m")
		roll()
	elif 0< pitch<=90:
		#affiche atterisage, nez vers le bas
		sense.show_letter("d")
		roll()


while True:
	o = sense.get_orientation()
	pitch = o["pitch"]
	roll = o["roll"]
	yaw = o["yaw"]

	pitch = round(pitch, 1)
	roll = round(roll, 1)
	yaw = round(yaw, 1)

	etat_pitch = ""
	etat_roll = ""
	if 270 <=pitch<=360:
		#affiche decolage, nez levé
		#sense.show_letter("1")
		etat_pitch = "1"
		if 0<roll<=90:
			#afficher inclinaison gauche de l'appareil
			#sense.show_letter("g")
			etat_roll="g"
		elif 270<=roll<=360:
			#afficher inclinaison droite de l'appareil
			#sense.show_letter("d")
			etat_roll="d"
		else:
			#afficher appareil à l'envers
			#sense.show_letter("x")
			etat_roll="x"

	elif 0< pitch<=90:
		#affiche atterisage, nez vers le bas
		#sense.show_letter("2")
		etat_pitch = "2"
		if 0<roll<=90:
			#afficher inclinaison gauche de l'appareil
			#sense.show_letter("g")
			etat_roll="g"
		elif 270<=roll<=360:
			#afficher inclinaison droite de l'appareil
			#sense.show_letter("d")
			etat_roll="d"
		else:
			#afficher appareil à l'envers
			#sense.show_letter("x")
			etat_roll="x"
	else:
    	etat_pitch = "x"
	

	sense.show_letter(etat_roll)
	sleep(1)
	sense.show_letter(etat_pitch)
	sleep(1)

	print("pitch {0} roll {1} yaw {2}".format(pitch, roll, yaw))



	