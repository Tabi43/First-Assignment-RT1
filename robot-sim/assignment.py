from __future__ import print_function

import time
import os
from sr.robot import *

#silver-token and gold-token are the types of blocks!


R = Robot()
silver_token = []
gold_token = []

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
    
a_th = 2.0
d_th = 0.4

def find_block(type):
	print("I'm searching the nearest...")
	markers = R.see()
	dist = 0
	rot_y = 0
	code = 0
	i = 0
	while(i < 10):
		markers = R.see()
		for m in markers:
			#print("token ->",m.dist,m.rot_y,m.info.code,m.info.marker_type)	
			if(m.info.marker_type == type):			
				if(m.dist < dist or dist == 0):
					if(check_used_silver_token(m.info.code) and (type == "silver-token")):
						print("token already used!")
					else:
						dist = m.dist
						rot_y = m.rot_y
						code = m.info.code
		i += 1
		turn(10,1)
	if(dist == 0):
		print("There is no token of type: ", type)
	else:
		print("Founded a token distant: ", dist, " angle: " , rot_y , "code: ", code) 
		return code
		
			
def grab_block_code(code, type):
	print("Going to grab the token with code :", code)
	markers = R.see()
	dist = 0
	while(dist == 0):
		turn(10,1)
		markers = R.see()
		for m in markers:
			if(m.info.code == code and m.info.marker_type == type):
				rot_y = m.rot_y	
				dist = m.dist
				print("I can see it!")
	for m in markers:
		if(m.info.code == code and m.info.marker_type == type):
			rot_y = m.rot_y
			dist = m.dist
			while(dist > d_th):
				if(-a_th<= rot_y <= a_th): 
					print("Ah, here we are!.")
					drive(15, 0.5)
				elif(rot_y < -a_th): 
					print("Left a bit...")
					turn(-2, 0.5)
				elif(rot_y > a_th):
					print("Right a bit...")
					turn(+2, 0.5)
				#Update of the relative position to markers
				markers = R.see()
				for m in markers:
					if(m.info.code == code and m.info.marker_type == type):
						rot_y = m.rot_y	
						dist = m.dist					
			check = R.grab()
			return check
				
	
def reach_block_code(code, type):
	print("Going to reach the token with code :", code)
	markers = R.see()
	dist = 0
	while(dist == 0):
		turn(10,1)
		markers = R.see()
		for m in markers:
			if(m.info.code == code and m.info.marker_type == type):
				rot_y = m.rot_y	
				dist = m.dist
				print("I can see it!")
	for m in markers:
		if(m.info.code == code and m.info.marker_type == type):
			rot_y = m.rot_y
			dist = m.dist
			while(dist > 1.5*d_th):
				if(-a_th<= rot_y <= a_th): 
					print("Ah, here we are!.")
					drive(20, 0.5)
				elif(rot_y < -a_th): 
					print("Left a bit...")
					turn(-2, 0.5)
				elif(rot_y > a_th):
					print("Right a bit...")
					turn(+2, 0.5)
				#Update of the relative position to markers
				markers = R.see()
				for m in markers:
					if(m.info.code == code and m.info.marker_type == type):
						rot_y = m.rot_y	
						dist = m.dist				
	
def check_used_silver_token(code):
	for c in silver_token:
		print("c = ",c)
		if(code == c):
			return 1
	return 0
	
while(1):
	os.system('clear')
	code = find_block("silver-token")
	check = grab_block_code(code,"silver-token")
	if(check == 1):
		print("silver-token code: ",code," added...")
		silver_token.append(code)
	code = find_block("gold-token")
	reach_block_code(code,"gold-token")
	R.release()
	drive(-10,2)

