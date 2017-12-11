import random
from state import GameState as gameState
import math

# This function udpates the ball position and checks the bounce/termination conditions. Returns a state
def play_game(board): 
	#initialize game
	#check to make sure not terminal state first
	if board.special == 1: 
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

		if abs(board.velocity_x) <= 0.03:
			print "VELOCITY_X ERROR"

	#if ball passes paddle set state to TERMINAL
	if board.ball_x > 1 and (board.ball_y > board.paddle_y and board.ball_y < paddle_bottom):
		board.special = 1

	return board

#This function takes a game state and discretizes it
def discretize(state): 
	#check if terminal state
	if state.special == 1:
		return None

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

	#add special state for when ball passes paddle with reward -1 
	#should stay in this state regardless of ball's velocity or paddle's location
	if state.ball_x > 1:
		state.special = 1

	return state

#Given a state and an action (nothing, UP, DOWN), this function moves the paddle
def move_paddle(state, action): 
	if state.special == 1: 
		print "TERMINAL STATE. GAME OVER"
		return None

	if action!= 0 or action!=1 or action!= 2:
		print "INVALID ACTION"

	state.paddle_y = state.paddle_y + state.action[action]

def maptoidx(state)
	ten_thousand = state.ball_x * (10000)
	thousand = state.ball_y * (1000)
	hundred = state.velocity_x * (100)
	ten = state.velocity_y * 10 

	final = ten_thousand + thousand + hundred + ten + state.paddle_y 
	return final

def main():
	# IN CASE OF BUGS IMPOSE ADDITIONAL VELOCITY BOUNDS
	# Q table
	q_table = []

	#initialize board
	paddle_height = 0.2
	board = gameState(0.5, 0.5, 0.03, 0.01, 0.5 - paddle_height/2)
	
	#observe current state and convert from continuous to discrete space
	discretized_board = discretize(board)

	#Terminal state check
	if discretized_board!= None:
	 	if discretized_board.state == 1:
	 		return None
	 	else:
			#choose an action based on exploration policy

			#update paddle

			#given action and current state get successor state
			#update q-table with current state and successor state
			#update game state to next state


if __name__ == '__main__':
	main()
