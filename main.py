

def main():
	lines = [line.rstrip('\n') for line in open("Hashi_Puzzles/100/Hs_16_100_25_00_001.has")]
	islands = []
	variables = []
	size = int(lines[0].split()[0])

	for i in range(1, len(lines)):
		for j, k in enumerate(lines[i].split()):
			if k != "0":
				islands.insert(len(islands), ((i-1, j), int(k)))
	
	for i in range(size):
		row = [(x,y) for (x,y) in enumerate(islands) if y[0][0] == i]
		for j in range(len(row)-1):
			variables.insert(len(variables), (row[j][0], row[j+1][0], 0))

	for i in range(size):
		col = [(x,y) for (x,y) in enumerate(islands) if y[0][1] == i]
		for j in range(len(col)-1):
			variables.insert(len(variables), (col[j][0], col[j+1][0], 0))

	print(variables)

if __name__ == "__main__":
	main()