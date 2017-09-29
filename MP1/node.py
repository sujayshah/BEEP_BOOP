class Node:

	def __init__(self, xpos, ypos, instate):
		self.x = xpos
		self.y = ypos 
		self.action = None
		self.parent = None
		self.state = instate