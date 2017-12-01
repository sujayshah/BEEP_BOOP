import random

class board_state:
	def __init__(self):
		self.ball_x = .5
		self.ball_y = .5
		self.velocity_x = .03
		self.velocity_y = .01
		self.paddle_height = .2
		self.paddle_x = 1
		self.paddle_y = (.5 - paddle_height) / 2
		self.paddle_action = {"nothing", "up", "down"}

def move_paddle(paddle_y, action):
	if action == "nothing":
		return paddle_y
	if action == "up":
		return paddle_y - .04
	if action == "down":
		return paddle_y + .04

def move_ball(state):
	#hit paddle
	if state.ball_x >= 1:
		state.ball_x = 2 * state.paddle_x - state.ball_x
		#do stuff with velocity
	if state.ball_y < 0:
		state.ball_y = -1*state.ball_y
		state.velocity_y = -1*state.velocity_y
	if state.ball_y > 1:
		state.ball_y = 2 - state.ball_y
		state.velocity_y = -1* state.velocity_y
	if state.ball_x < 0:
		state.ball_x = -1*state.ball_x
		state.velocity_x = -1* state.velocity_x

def make_game(): 
