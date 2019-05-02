import random

class Firefly:

	def __init__(self, id, variables, seed):
		self.id = id
		self.variables = variables
		random.seed(seed)
		self.brightness = 0

	def randomizeSolution(self):		
		for x in self.variables:
			x[2] = random.randint(0, 2)

	def determineBrightness(self, islands, intersections):
		self.brightness = 0
		for i in range(len(islands)):
			sum = 0
			interest = [x for x in self.variables if x[0] == i or x[1] == i]	
			for x in interest:
				sum += x[2]
			self.brightness += abs(islands[i][1] - sum)

		for i in range(len(intersections)):
			if self.variables[intersections[i][0]][2] and self.variables[intersections[i][1]][2]:
				self.brightness += 1

		return self.brightness

	def performLocalWalk(self, alphaVariables, exploitChance):
		for i in range(len(self.variables)):
			if random.randint(0, 9) < exploitChance:
				self.variables[i][2] = alphaVariables[i][2]

	def performRandomWalk(self, exploreChance):
		for i in range(len(self.variables)):
			if random.randint(0, 9) < exploreChance:
				if random.randint(0, 1) == 0:
					self.doInsert(self.variables[i])
				else:
					self.doDelete(self.variables[i])

	def doInsert(self, variable):
		if variable[2] < 2:
			variable[2] += 1
		else:
			self.doDelete(variable)

	def doDelete(self, variable):
		if variable[2] > 0:
			variable[2] -= 1
		else:
			self.doInsert(variable)
