import random

class Firefly:

	def __init__(self, id, variables, seed):
		self.id = id
		self.variables = variables.copy()
		random.seed(seed)
		self.brightness = 0

	def randomizeSolution(self):		
		for x in self.variables:
			x[2] = random.randint(0, 2)

	def determineBrightness(self, size, islands, intersections):
		self.brightness = 0
		for i in range(size):
			sum = 0
			interest = [x for x in self.variables if x[0] == i or x[1] == i]	
			for x in interest:
				sum += x[2]
			self.brightness += abs(islands[i][1] - sum)

		for i in range(len(intersections)):
			if self.variables[intersections[i][0]][2] and self.variables[intersections[i][1]][2]:
				self.brightness += 1

		return self.brightness

	def performRandomWalk(self):
		for x in self.variables:
			self.randomWalks(random.randint(0, 2), x)

	def doNothing(self):
		return

	def doInsert(self, variable):
		if variable[2] < 2:
			variable[2] += 1

	def doDelete(self, variable):
		if variable[2] > 0:
			variable[2] -= 1

	def randomWalks(self, mode, variable):
		if mode == 0:
			self.doNothing()
		elif mode == 1:
			self.doInsert(variable)
		else:
			self.doDelete(variable)
