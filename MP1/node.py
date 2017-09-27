class Node:

	def __init__(self, xpos, ypos, action):
		self.x = xpos
		self.y = ypos 
		self.action = action
		self.parent = None
		self.state = None