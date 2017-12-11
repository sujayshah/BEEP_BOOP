import random
from state import GameState as gameState

def play_game(): 
	#initialize game
	paddle_height = 0.2
	board = gameState(0.5, 0.5, 0.03, 0.01, 0.5 - paddle_height/2)

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

#This function takes a game state and discretizes it
def discretize(state): 
	paddle_height = 0.2
	#treat the entire board as a 12x12 grid so there are 144 possible ball locations
	
	#discretize the x velocity
	if state.velocity_x < 0: 
		state.velocity_x = -1 
	else if state.velocity_x >= 0:
		state.velocity_x = 1

	#discretize the y velocity
	if abs(state.velocity_y) < 0.015:
		state.velocity_y = 0
	else if state.velocity_y < 0: 
		state.velocity_y = -1
	else if state.velocity_y >=0: 
		state.velocity_y = 1

	#convert paddle location
	discrete_paddle = floor(12 * state.paddle_y/ (1- paddle_height))
	if state.paddle_y == (1- paddle_height):
		discrete_paddle = 11

	#add special state for when ball passes paddle with reward -1 
	#should stay in this state regardless of ball's velocity or paddle's location
	if state.ball_x > 1:
		state.special = 1


def main():
	# IN CASE OF BUGS IMPOSE ADDITIONAL VELOCITY BOUNDS 
	# TERMINATION??
	play_game()	


if __name__ == '__main__':
	main()
