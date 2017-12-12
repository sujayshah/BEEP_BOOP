import random
from state import GameState as gameState
import math

#global variables 
# q_table = [list([0, 0, 0])] * 10369
# N= [list([0, 0, 0])] * 10369
q_table = {}
N = {}
epsilon = 0.3

# This function udpates the ball position and checks the bounce/termination conditions. Returns a state
def play_game(state, action): 
	#initialize game
	#check to make sure not terminal state first
	if state == None or state.special == 1: 
		#print "TERMINAL STATE. GAME OVER"
		return None

	reward = 0 
	paddle_height = 0.2

	state.paddle_y = state.paddle_y + state.actions[action]

	#if paddle goes off the top of the screen
	if state.paddle_y < 0: 
		state.paddle_y = 0

	#if any part of the paddle goes off the bottom of the scr
	if (state.paddle_y > 0.8):
		state.paddle_y = 0.8


	#at each time step: 
	#increment ball_x by velocity_x and ball_y by velocity_y 
	orig_x = state.ball_x #old points 
	orig_y = state.ball_y

	state.ball_x = state.ball_x + state.velocity_x
	state.ball_y = state.ball_y + state.velocity_y

	new_x = state.ball_x #new points 
	new_y = state.ball_y

	#bounce
	#if ball is off the top of the screen
	if state.ball_y < 0: 
		state.ball_y = -1 * state.ball_y
		state.velocity_y = -1 * state.velocity_y 

	#if ball is off bottom of screen 
	if state.ball_y > 1: 
		state.ball_y = 2 - state.ball_y 
		state.velocity_y = -1 * state.velocity_y 

	#if ball is off left edge of screen 
	if state.ball_x < 0: 
		state.ball_x = -1 * state.ball_x 
		state.velocity_x = -1 * state.velocity_x
		if abs(state.velocity_x) <= 0.03:
			print "VELOCITY_X ERROR"

	#if ball bounced off paddle:
	#draw a line along direction ball is moving
	slope = (new_y - orig_y)/(new_x - orig_x)
	b = new_y - (slope * new_x)
	y_intersection= slope + b # y = mx + b, plug in x = 1
 	paddle_bottom = state.paddle_y + paddle_height

	#if x>1 and line intersects the x=1 line within paddle range
	if state.ball_x > 1 and (state.ball_y >= state.paddle_y and state.ball_y <= paddle_bottom):
		state.ball_x = 2 - state.ball_x
		reward = 1
		while True:
			U =  random.uniform(-0.015, 0.015)
			V = random.uniform(-0.03, 0.03)

			state.velocity_x = (-1 * state.velocity_x) + U
			state.velocity_y = state.velocity_y + V

			if abs(state.velocity_x) > 0.03:
				break


	#if ball passes paddle set state to TERMINAL
	if state.ball_x > 1 and (state.ball_y > state.paddle_y and state.ball_y < paddle_bottom):
		state.special = 1
		reward = -1
		print "w a o w"

	return (state.ball_x, state.ball_y, state.velocity_x, state.velocity_y, state.paddle_y, reward)

#This function takes a game state and discretizes it
def discretize(state): 
	#check if terminal state
	if state.special == 1:
		return None

	#add special state for when ball passes paddle with reward -1 
	#should stay in this state regardless of ball's velocity or paddle's location
	if state.ball_x > 1:
		state.special = 1

	paddle_height = 0.2
	#treat the entire board as a 12x12 grid so there are 144 possible ball locations
	ball_x = math.floor(12 * state.ball_x)
	ball_y = math.floor(12 * state.ball_y)
	
	#discretize the x velocity
	if state.velocity_x < 0: 
		velocity_x = -1 
	elif state.velocity_x >= 0:
		velocity_x = 1

	#discretize the y velocity
	if abs(state.velocity_y) < 0.015:
		velocity_y = 0
	elif state.velocity_y < 0: 
		velocity_y = -1
	elif state.velocity_y >=0: 
		velocity_y = 1

	#convert paddle location
	discrete_paddle = math.floor(12 * state.paddle_y/ (1- paddle_height))
	if state.paddle_y == (1- paddle_height):
		discrete_paddle = 11

	paddle_y = discrete_paddle

	return (ball_x, ball_y, velocity_x, velocity_y, paddle_y)

# def maptoidx(state):
# 	ten_thousand = state.ball_x * (10000)
# 	thousand = state.ball_y * (1000)
# 	hundred = state.velocity_x * (100)
# 	ten = state.velocity_y * 10 

# 	final = ten_thousand + thousand + hundred + ten + state.paddle_y 
# 	final = hash(final) % 10369 
# 	final = int(final)
# 	return final

# This function returns the action you should take given a state
def exploration_policy(state, israndom): 
	if state is None or state.special == 1:
		print "ERROR" 
		return None

	#with probability e choose randomly 
	if israndom is True: 
		a = random.randint(0, 2)
		return a
	else:
		#with probability (1-e) follow the greedy policy 
		q_max = -10000000000000
		for i in range(3):
			if (discretize(state), i) not in N or (discretize(state), i) not in q_table:
				a = random.randint(0,2)
				return a 

			if q_table[(discretize(state), i)] > q_max:
				q_max = q_table[(discretize(state), i)]
				a = i
				#print "chose actual"
	return a

def qmax(state):
	if state is None or state.special == 1: 
		print "ERROR" 
		return None 

	q_max = -10000000000000
	for i in range(3):
		if (discretize(state), i) not in q_table: 
			temp_value = 0 
		else:
			temp_value = q_table[(discretize(state), i)]
	
	return max(temp_value, q_max)


def qlearning_agent(C, gamma):
	# IN CASE OF BUGS IMPOSE ADDITIONAL VELOCITY BOUNDS
	global q_table 
	global N 

	reward = 0 
	num_bounces = 0 
	n = 0 # number iterations
	random_count = 0 

	#initialize board; board is current game state 
	paddle_height = 0.2
	
	while n < 100000:
		if n%1000 == 0:
			print "n: " + str(n)
			if n> 0:
				print "Num_bounces: " + str(num_bounces/1000.0)
				num_bounces = 0

		#observe current state and convert from continuous to discrete space
		#start from scratch
		board = gameState(0.5, 0.5, 0.03, 0.01, 0.5 - paddle_height/2)
		current_state = board

		#Terminal state check
		if current_state == None:
			print "ERROR"
			continue

		if current_state.special == 1:
			return None
			continue 

		else:	
			while True:
				choose_random = False
				if current_state == None or current_state.special == 1: 
					random_count = 0 
					break

				random_count +=1 
				if random_count > 10: 
					random_count = 1

				if random_count/10.0 == 0.3:
					choose_random = True

				#choose an action based on exploration policy
				a = exploration_policy(current_state, choose_random)

				#given action and current state get successor state
				temp_tuple= play_game(current_state, a) #final successor state
				if temp_tuple == None:
					random_count = 0 
					break
				else:
					#update next game state to successor state
					successor_state = gameState(temp_tuple[0], temp_tuple[1], temp_tuple[2], temp_tuple[3], temp_tuple[4])	
					# print "CURRENT: ", (current_state.ball_x, current_state.ball_y, current_state.velocity_x, current_state.velocity_y)
					# print "SUCCESSOR: ", (successor_state.ball_x, successor_state.ball_y, successor_state.velocity_x, successor_state.velocity_y)
				
				reward = temp_tuple[5]

				if (discretize(current_state), a) not in N: 
					N[(discretize(current_state), a)] = 1
					alpha = 1.0 
				else:
					N[(discretize(current_state), a)] += 1
					alpha = 1.0 * (C/(C + N[(discretize(current_state), a)]))

				#update q-table with current state and successor state
				if N[(discretize(current_state), a)] == 1:
					q_table[(discretize(current_state), a)] = alpha * (reward + gamma * qmax(successor_state))
				
				else:
					q_table[(discretize(current_state), a)] = q_table[(discretize(current_state), a)] + (alpha * (reward + (gamma * qmax(successor_state)) - q_table[(discretize(current_state), a)]))
				
				if reward > 0: 
					num_bounces +=1

				current_state = gameState(successor_state.ball_x, successor_state.ball_y, successor_state.velocity_x, successor_state.velocity_y, successor_state.paddle_y)
				
		n+=1 
	return num_bounces

def main(): 
	global q_table
	global N 

	q_table = {}
	N = {}
	bounces = qlearning_agent(100, 0.7)



if __name__ == '__main__':
	main()
