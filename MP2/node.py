class Node:

	#def __init__(self, xpos, ypos, instate):
	#	self.x = xpos
	#	self.y = ypos 
	#	self.action = None
		# self.parent = None
		# self.children = []
		# self.state = instate

	def __init__(self, instate):
		self.state = instate #starter grid
		self.possiblemoves = [] # list of possible grids