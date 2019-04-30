import random

random.seed(11)

def main():
	lines = [line.rstrip('\n') for line in open("Hashi_Puzzles/100/Hs_16_100_25_00_001.has")]
	size = int(lines[0].split()[0])
	islands = []
	variables = []
	intersections = []	

	createIslands(lines, islands)
	generateVariables(size, islands, variables)	
	findIntersections(islands, variables, intersections)
	randomizeSolution(variables)	
	brightness = determineBrightness(size, islands, variables, intersections)
		
	print(brightness)

	
	

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

def randomizeSolution(variables):
	for x in variables:
		x[2] = random.randint(0, 2)

def determineBrightness(size, islands, variables, intersections):
	brightness = 0	
	for i in range(size):
		sum = 0
		interest = [x for x in variables if x[0] == i or x[1] == i]	
		for x in interest:
			sum += x[2]
		brightness += abs(islands[i][1] - sum)

	for i in range(len(intersections)):
		if variables[intersections[i][0]][2] and variables[intersections[i][1]][2]:
			brightness += 1

	return brightness

def ccw(A, B, C):
	return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])

def intersect(A, B, C, D):
	return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

if __name__ == "__main__":
	main()