import random
import copy
from firefly import Firefly

random.seed(16)
population = 100
exploitChance = 9
exploreChance = 3
iterations = 100
#difficulty = "easy"
#difficulty = "normal"
difficulty = "hard"

def main():
	complete = 0
	for counter in range(100):
		lines = [line.rstrip('\n') for line in open("puzzles/"+ difficulty + str(counter+1).zfill(3) +".txt")]
		size = int(lines[0].split()[0])
		islands = []
		variables = []
		intersections = []
		firefly = [None]*population	

		createIslands(lines, islands)
		generateVariables(size, islands, variables)	
		findIntersections(islands, variables, intersections)

		for i in range(population):
			firefly[i] = Firefly(i, copy.deepcopy(variables), random.random())
			firefly[i].randomizeSolution()
			firefly[i].determineBrightness(islands, intersections)

		firefly = sorted(firefly, key=lambda x: x.brightness)

		for j in range(iterations):
			for i in range(1, len(firefly)):	
				firefly[i].performLocalWalk(firefly[0].variables, exploitChance)
				firefly[i].performRandomWalk(exploreChance)	
				firefly[i].determineBrightness(islands, intersections)

			firefly = sorted(firefly, key=lambda x: x.brightness)

			if firefly[0].brightness == 0:
				complete += 1
				break

	print("Number of accomplished puzzles: " + str(complete))	

def createIslands(lines, islands):
	for i in range(1, len(lines)):
		for x, y in enumerate(lines[i].split()):
			if y != "0":
				islands.insert(len(islands), ((i-1, x), int(y)))

def generateVariables(size, islands, variables):
	for i in range(size):
		row = [(x,y) for (x,y) in enumerate(islands) if y[0][0] == i]
		for j in range(len(row)-1):
			variables.insert(len(variables), [row[j][0], row[j+1][0], 0])

	for i in range(size):
		col = [(x,y) for (x,y) in enumerate(islands) if y[0][1] == i]
		for j in range(len(col)-1):
			variables.insert(len(variables), [col[j][0], col[j+1][0], 0])

def findIntersections(islands, variables, intersections):
	for i in range(len(variables)-1):
		for j in range(i+1, len(variables)):
			if len(set(variables[i][:2]) & set(variables[j][:2])) > 0:
				continue				
			elif intersect(islands[variables[i][0]][0], islands[variables[i][1]][0], \
				islands[variables[j][0]][0], islands[variables[j][1]][0]):

				intersections.insert(len(intersections), (i, j))

def ccw(A, B, C):
	return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def intersect(A, B, C, D):
	return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

if __name__ == "__main__":
	main()