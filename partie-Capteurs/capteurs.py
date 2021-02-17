from sense_hat import SenseHat
import time
import paho.mqtt.client as mqtt
import os
from math import *
import ssl


monIP = os.popen('ip a s dev eth0 | grep -oE "inet .*/16" | sed "s/inet //" | sed "s/\/16//"').read().split('\n')[0]
finIP = monIP.split('.')[::-1][0]

sense = SenseHat()


def on_connect(client, userdata, flags, rc):
	if rc==0:
		client.connected_flag=True
		print("Connexion OK")
	else:
		print("Mauvaise Connexion Returned code=",rc)

broker_address="10.202.9.1"
client = mqtt.Client("P1")
client.connected_flag=False

client.on_connect=on_connect
client.loop_start()

client.username_pw_set(username="ido",password="lpido")

print("Connexion au broker ",broker_address)

client.tls_set(ca_certs="/home/pi/ca.crt")
client.tls_insecure_set(True)

client.connect(broker_address,8883)

while not client.connected_flag:
    print("En attente de connexion au broker")
    time.sleep(1)
client.loop_stop()


dernierePositionJoystick = ""

def joystick_up():
	global dernierePositionJoystick
	if dernierePositionJoystick != "HAUT":
		print("rasp-{}/joystick <- HAUT".format(finIP))
		client.publish("rasp-{}/joystick".format(finIP),"HAUT")
		dernierePositionJoystick = "HAUT"
		print

def joystick_down():
	global dernierePositionJoystick
	if dernierePositionJoystick != "BAS":
		print("rasp-{}/joystick <- BAS".format(finIP))
		client.publish("rasp-{}/joystick".format(finIP),"BAS")
		dernierePositionJoystick = "BAS"
		print

def joystick_left():
	global dernierePositionJoystick
	if dernierePositionJoystick != "GAUCHE":
		print("rasp-{}/joystick <- GAUCHE".format(finIP))
		client.publish("rasp-{}/joystick".format(finIP),"GAUCHE")
		dernierePositionJoystick = "GAUCHE"
		print

def joystick_right():
	global dernierePositionJoystick
	if dernierePositionJoystick != "DROITE":
		print("rasp-{}/joystick <- DROITE".format(finIP))
		client.publish("rasp-{}/joystick".format(finIP),"DROITE")
		dernierePositionJoystick = "DROITE"
		print

def joystick_middle():
	global dernierePositionJoystick
	if dernierePositionJoystick != "CENTRE":
		print("rasp-{}/joystick <- CENTRE".format(finIP))
		client.publish("rasp-{}/joystick".format(finIP),"CENTRE")
		dernierePositionJoystick = "CENTRE"
		print

sense.stick.direction_up = joystick_up
sense.stick.direction_down = joystick_down
sense.stick.direction_left = joystick_left
sense.stick.direction_right = joystick_right
sense.stick.direction_middle = joystick_middle


while 1:
	temperature = sense.get_temperature()
	pression = sense.get_pressure()
	humidite = sense.get_humidity()


	orientation = sense.get_orientation()

	roulis = orientation["roll"]
	tangage = orientation["pitch"]
	lacet = orientation["yaw"]

	roulis = round(roulis, 1)
	tangage = round(tangage, 1)
	lacet = round(lacet, 1)


	coord_acceleration = sense.get_accelerometer_raw()
	x = coord_acceleration['x']
	y = coord_acceleration['y']
	z = coord_acceleration['z']

	x=round(x, 0)
	y=round(y, 0)
	z=round(z, 0)

	acceleration = round(abs(sqrt(x**2+y**2+z**2)-1),2)


	print("rasp-{}/temperature <- {}".format(finIP,temperature))
	client.publish("rasp-{}/temperature".format(finIP),temperature)

	print("rasp-{}/pression <- {}".format(finIP,pression))
	client.publish("rasp-{}/pression".format(finIP),pression)

	print("rasp-{}/humidite <- {}".format(finIP,humidite))
	client.publish("rasp-{}/humidite".format(finIP),humidite)

	print("rasp-{}/gyro/roulis <- {}".format(finIP,roulis))
	client.publish("rasp-{}/gyro/roulis".format(finIP),roulis)

	print("rasp-{}/gyro/tangage <- {}".format(finIP,tangage))
	client.publish("rasp-{}/gyro/tangage".format(finIP),tangage)

	print("rasp-{}/gyro/lacet <- {}".format(finIP,lacet))
	client.publish("rasp-{}/gyro/lacet".format(finIP),lacet)

	print("rasp-{}/acceleration <- {}".format(finIP,acceleration))
	client.publish("rasp-{}/acceleration".format(finIP),acceleration)


	print
	time.sleep(1)