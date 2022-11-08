from __future__ import print_function

import time
import os
from sr.robot import *

R = Robot()

a_th = 2.0 
d_th = 0.4

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
    

def discover(silver_list, gold_list):
	"""
		Function that make the robot turn around 
		to search and measure all tokens it see
	"""
	print("Analizing the map...")
	i = 12 #12 is a good number to make it turn a complete round
	while(i > 0):
		turn(10,1)
		markers = R.see()
		for m in markers:
			#If he found a new token save it into the correct memory vector
			if(contains(gold_tokens, m.info.code) == -1 and m.info.marker_type == "gold-token"):
				token = [m.info.code,  m.dist, m.rot_y]				
				gold_list.append(token)
			elif(contains(silver_tokens, m.info.code) == -1 and m.info.marker_type == "silver-token"):
				token = [m.info.code,  m.dist, m.rot_y]
				silver_list.append(token)
		i -= 1
	return len(silver_tokens) + len(gold_tokens)

def chose_closer_token(list):
	"""
		He search into his memory the closer token.
		
		Args: list (...) is the memory vector of the type needed
	"""
	i = 0
	min_d = 0
	code = 0
	lalast_rot_y = 0
	for t in list:
		#If the i token is closer than the last save it
		if(t[1] < min_d or min_d == 0):
				code = t[0]
				min_d = t[1]
				last_rot_y = t[2]	
	print("Chosen the neasrest token with code: ", code, "distance =", min_d)
	return code, last_rot_y

def update_distance(list, m):
	"""
		Update the new distance of a token if inside the vector memory.
		
		Args: 	list (...) is the memory vector of the type needed
			m is the token object that contains the new data 
	"""
	index = contains(list, m.info.code)
	if(index != -1):	
		list[index][1] = m.dist
		list[index][2] = m.rot_y

def disable_token(list, code):
	"""
		Function to pop tokens used.
		
		Args: 	list (...) is the memory vector of the type needed
			code (int) is the code of the block to be removed
	"""
	index = contains(list, code)
	list.pop(index)


def contains(list, code):
	"""
		Check if exist a token inside the vector memory. 
		If it exist return the index of otherwise -1
		
		Args:	list (...) is the memory vector of the type needed
			code (int) is the code of the block wanted
	"""
	i = 0
	for c in list:
		if(c[0] == code):
			return i
		i += 1
	return -1


def reach_block_code(code, type, last_rot_y, m_dst, silver_list, gold_list):
	"""
	Function for reach a particular token
	
	Args: 	code (int) Code of the token to reach
		type (string) Type of the token to reach
		last_rot_y (double) The last rotation useful to turn in the right sense
		m_dst (double) The minimum distance to consider the token reached
		
	"""
	print("Going to reach the token with code :", code)	
	#Always start thinking is not visible the token
	dist = 0
	while(dist == 0):		
		if(last_rot_y < -a_th): 			
			turn(-10, 0.5)
		elif(last_rot_y > a_th):			
			turn(+10, 0.5)
		elif(last_rot_y == 0):
			turn(+10, 0.5)
		markers = R.see()
		for m in markers:
			if(m.info.code == code and m.info.marker_type == type):
				rot_y = m.rot_y	
				dist = m.dist
				print("I can see it now!")
			if(m.info.marker_type == "gold-token"):
				update_distance(gold_list, m)
			else:
				update_distance(silver_list, m)
	for m in markers:
		if(m.info.code == code and m.info.marker_type == type):
			rot_y = m.rot_y
			dist = m.dist
			while(dist > m_dst):
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
					else:
						if(m.info.marker_type == "gold-token"):
							update_distance(gold_list, m)
						else:
							update_distance(silver_list, m)					
							

"""
	These are a double list that works like a "memory vector". The idea
	is to profit by the current displacement of th erobot itself to remesure 
	the tokens he see and choose the one nearest. 
	
	----The structure of memory vector----
	
	 [i] The token
		[0] is the code; 
		[1] the last distance mesured; 
		[2] last rotatio measured;
"""
gold_tokens = []
silver_tokens = []	
os.system('clear')
n = discover(silver_tokens, gold_tokens)
print("Discovered : ", n, "elements")
while(len(gold_tokens) + len(silver_tokens) > 0):
	code, last_rot_y = chose_closer_token(silver_tokens)
	reach_block_code(code, "silver-token" , last_rot_y, d_th, silver_tokens, gold_tokens)
	R.grab()
	disable_token(silver_tokens, code)
	code, last_rot_y = chose_closer_token(gold_tokens)
	reach_block_code(code, "gold-token" , last_rot_y, 1.5*d_th, silver_tokens, gold_tokens)
	R.release()
	disable_token(gold_tokens, code)	
	drive(-10,1)
print("Finished!")
