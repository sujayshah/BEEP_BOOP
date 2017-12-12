import random
from state import GameState as gameState
import math

# This function udpates the ball position and checks the bounce/termination conditions. Returns a state
def play_game(board): 
	#initialize game
	#check to make sure not terminal state first
	if board == None or board.special == 1: 
		print "TERMINAL STATE. GAME OVER"
		return None

	paddle_height = 0.2

	#at each time step: 
	#increment ball_x by velocity_x and ball_y by velocity_y 
	orig_x = board.ball_x #old points 
	orig_y = board.ball_y

	board.ball_x = board.ball_x + board.velocity_x
	board.ball_y = board.ball_y + board.velocity_y

	new_x = board.ball_x #new points 
	new_y = board.ball_y

	#bounce
	#if ball is off the top of the screen
	if board.ball_y < 0: 
		board.ball_y = -1 * board.ball_y
		board.velocity_y = -1 * board.velocity_y 

	#if ball is off bottom of screen 
	if board.ball_y > 1: 
		board.ball_y = 2 - board.ball_y 
		board.velocity_y = -1 * board.velocity_y 

	#if ball is off left edge of screen 
	if board.ball_x < 0: 
		board.ball_x = -1 * board.ball_x 
		board.velocity_x = -1 * board.velocity_x
		if abs(board.velocity_x) <= 0.03:
			print "VELOCITY_X ERROR"

	#if ball bounced off paddle:
	#draw a line along direction ball is moving
	slope = (new_y - orig_y)/(new_x - orig_x)
	b = new_y - (slope * new_x)
	y_intersection= slope + b # y = mx + b, plug in x = 1
 	paddle_bottom = board.paddle_y - paddle_height

	#if x>1 and line intersects the x=1 line within paddle range
	if board.ball_x > 1 and (board.ball_y <= board.paddle_y and board.ball_y >= paddle_bottom):
		board.ball_x = 2 - board.ball_x
		board.velocity_x = (-1 * board.velocity_x) + random.uniform(-0.015, 0.015)
		board.velocity_y = board.velocity_y + random.uniform(-0.03, 0.03)
		board.reward = 1

		if abs(board.velocity_x) <= 0.03:
			print "VELOCITY_X ERROR"

	#if ball passes paddle set state to TERMINAL
	if board.ball_x > 1 and (board.ball_y > board.paddle_y and board.ball_y < paddle_bottom):
		board.special = 1
		board.reward = -1

	return (board, reward)

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

#Given a state and an action (nothing, UP, DOWN), this function moves the paddle
def move_paddle(state, action): 
	if state.special == 1: 
		print "TERMINAL STATE. GAME OVER"
		return None

	if action!= 0 or action!=1 or action!= 2:
		print "INVALID ACTION"

	state.paddle_y = state.paddle_y + state.actions[action]

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
	else:
			a = q_table[q_idx].index(max(q_table[q_idx][0], q_table[q_idx][1], q_table[q_idx][2]))

	return a

def qlearning_agent(alpha, gamma):
	# IN CASE OF BUGS IMPOSE ADDITIONAL VELOCITY BOUNDS
	# Q table and seen table
	q_table = [(0, 0, 0)] * 10369
	N= [(0, 0, 0)] * 10369
	reward = 0 
	num_bounces = 0 
	n = 0 # number iterations

	#initialize board; board is current game state 
	paddle_height = 0.2
	board = gameState(0.5, 0.5, 0.03, 0.01, 0.5 - paddle_height/2)

	while n < 100000:
		#observe current state and convert from continuous to discrete space
		discretized_board = discretize(board)

		#Terminal state check
		if discretized_board == None:
			print "ERROR"
			return

		if discretized_board.special == 1:
			return None
		else:
			#choose an action based on exploration policy
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
			successor_state1 = move_paddle(discretized_board, a) #original state with moved paddle 
			successor_state2, reward= play_game(successor_state1) #final successor state

			#update q-table with current state and successor state
			new_idx = maptoidx(successor_state2)
			successor_action = exploration_policy(q_table, new_idx)
			q_table[q_idx][a] = q_table[q_idx][a] + (alpha * (reward + (gamma * successor_action) - q_table[q_idx][a]))
			
			if reward > 0: 
				num_bounces +=1

			#update game state to next state
			board = successor_state2
		
		count +=1 
	return num_bounces

def main(): 
	qlearning_agent()


if __name__ == '__main__':
	main(1, 1)
