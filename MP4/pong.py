import random
from state import GameState as gameState
import math

#global variables 
q_table = [list([0, 0, 0])] * 10369
N= [list([0, 0, 0])] * 10369
C= 100

# This function udpates the ball position and checks the bounce/termination conditions. Returns a state
def play_game(state, action): 
	#initialize game
	#check to make sure not terminal state first
	if state == None or state.special == 1: 
		print "TERMINAL STATE. GAME OVER"
		return None

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
		print "off the top"

	#if ball is off bottom of screen 
	if state.ball_y > 1: 
		state.ball_y = 2 - state.ball_y 
		state.velocity_y = -1 * state.velocity_y 

	#if ball is off left edge of screen 
	if state.ball_x < 0: 
		state.ball_x = -1 * state.ball_x 
		state.velocity_x = -1 * state.velocity_x
		if abs(board.velocity_x) <= 0.03:
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
		state.reward = 1
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
		state.reward = -1

	return (state, state.reward)

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
	state.ball_x = math.floor(12 * state.ball_x)
	state.ball_y = math.floor(12 * state.ball_y)
	
	#discretize the x velocity
	if state.velocity_x < 0: 
		state.velocity_x = -1 
	elif state.velocity_x >= 0:
		state.velocity_x = 1

	#discretize the y velocity
	if abs(state.velocity_y) < 0.015:
		state.velocity_y = 0
	elif state.velocity_y < 0: 
		state.velocity_y = -1
	elif state.velocity_y >=0: 
		state.velocity_y = 1

	#convert paddle location
	discrete_paddle = math.floor(12 * state.paddle_y/ (1- paddle_height))
	if state.paddle_y == (1- paddle_height):
		discrete_paddle = 11

	state.paddle_y = discrete_paddle

	return state

# #Given a state and an action (nothing, UP, DOWN), this function moves the paddle
# def move_paddle(state, action): 
# 	if state.special == 1: 
# 		print "TERMINAL STATE. GAME OVER"
# 		return None

# 	if action!= 0 or action!=1 or action!= 2:
# 		print "INVALID ACTION"

# 	state.paddle_y = state.paddle_y + state.actions[action]

def maptoidx(state):
	ten_thousand = state.ball_x * (10000)
	thousand = state.ball_y * (1000)
	hundred = state.velocity_x * (100)
	ten = state.velocity_y * 10 

	final = ten_thousand + thousand + hundred + ten + state.paddle_y 
	final = hash(final) % 10369 
	final = int(final)
	return final

# This function returns the action you should take given a table and an index
def exploration_policy(q_table, q_idx): 
	if q_table[q_idx][0] == q_table[q_idx][1] == q_table[q_idx][2]:
			a = random.randint(0,2)
			print "RANDOM: " + str(a)
			return a
	else:
			a = q_table[q_idx].index(max(q_table[q_idx][0], q_table[q_idx][1], q_table[q_idx][2]))
			print "I CHOSE: " + str(a)
			return a

	return a

def qlearning_agent(alpha_C, gamma):
	# IN CASE OF BUGS IMPOSE ADDITIONAL VELOCITY BOUNDS
	# Q table and seen table
	# q_table = [(0, 0, 0)] * 10369
	# N= [(0, 0, 0)] * 10369
	global q_table 
	global N 

	reward = 0 
	num_bounces = 0 
	n = 0 # number iterations

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
		discretized_board = discretize(board)

		#Terminal state check
		if discretized_board == None:
			print "ERROR"
			continue

		if discretized_board.special == 1:
			return None
			continue 

		else:
			#choose an action based on exploration policy
			while True:

				if discretized_board == None or discretized_board.special == 1: 
					keep_playing = False
					break

				q_idx = maptoidx(discretized_board)
				a = exploration_policy(q_table, q_idx)

				#increment number of times seen state action pair (s,a) and use the right alpha
				if N[q_idx][a] == 0:
					N[q_idx][a] = 1
					alpha = 1.0
				else:
					N[q_idx][a] += 1
					alpha = 1.0 * (C/(C + N[q_idx][a]))
				
				#given action and current state get successor state
				temp_tuple= play_game(discretized_board, a) #final successor state
				successor_state = temp_tuple[0]
				reward = temp_tuple[1]
				#print (discretized_board.ball_x, discretized_board.ball_y)
				# print "1, ",  
				# print (successor_state.ball_x, successor_state.ball_y)

				#update q-table with current state and successor state
				new_idx = maptoidx(successor_state)
				successor_action = exploration_policy(q_table, new_idx)
				q_table[q_idx][a] = q_table[q_idx][a] + (alpha * (reward + (gamma * successor_action) - q_table[q_idx][a]))
				
				if reward > 0: 
					num_bounces +=1
					print "HELLO"

				#update game state to next state
				board = successor_state
				discretized_board = discretize(board)
				# print "2, ", 
				# print (discretized_board.ball_x, discretized_board.ball_y)
		
		n+=1 
	return num_bounces

def main(): 
	bounces = qlearning_agent(100, 0.8)


if __name__ == '__main__':
	main()
