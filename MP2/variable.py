class Variable:

	def __init__(self, xpos, ypos, assignment, domain, state):
		self.x = xpos
		self.y = ypos
		self.assignment = assignment 
		self.domain = []
		self.state = state   # This state corresponds to 0 if a variable is unassigned, 1 if given assignment at start of problem,
								   # and 2 if assigned but not certain to be correct value
		