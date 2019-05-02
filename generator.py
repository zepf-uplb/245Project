#https://github.com/pgorsira/hashiwokakero/blob/master/bridges.py
# -*- coding: utf-8 -*-
__author__ = 'Pieter Gorsira'

import random
from random import choice

size = 8
islands = 15
difficulty = "hard"
width = size
length = size

def display(board):
    s = [[str(e) for e in row] for row in board]
    lens = [len(max(col, key=len)) for col in zip(*s)]
    fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
    table = [fmt.format(*row) for row in s]
    print('\n'.join(table))


def reverse_direction(direction):
    return tuple([-1 * x for x in direction])

for i in range(100):

    generated = False
    print ("Generating puzzle " + str(i+1).zfill(3))

    while not generated:

        num_nodes = islands
        board = [[' ' for x in range(width)] for y in range(length)]  # solution (full board)

        # first node
        x = random.randrange(0, length)
        y = random.randrange(0, width)
        board[x][y] = '*'
        nodes = [(x, y)]
        directions = {nodes[-1]: []}

        looped = 0  # todo is this a dirty patch or a necessary fix

        while num_nodes > 1 and looped < 100:  # prepare board
            looped += 1

            home_node = choice(nodes)

            if len(directions[home_node]) == 4:  # all 4 directions used for this node
                continue

            direction_taken = True
            while direction_taken:  # find an unused direction for this node
                dx = random.randrange(-1, 2)
                dy = random.randrange(-1, 2)
                direction = (dx, dy)
                direction_taken = direction in directions[home_node] or (abs(dx) == abs(dy))

            x = home_node[0]
            y = home_node[1]

            # determine bridge specs
            double_bridge = random.randrange(0, 2) > 0.7

            if dx == 0:
                if double_bridge:
                    bridge = '='
                else:
                    bridge = '-'

                if dy < 0:
                    dist_avail = y
                else:
                    dist_avail = width - y
            else:
                if double_bridge:
                    bridge = '‖'
                else:
                    bridge = '|'

                if dx < 0:
                    dist_avail = x
                else:
                    dist_avail = length - x

            try:
                distance = random.randrange(2, dist_avail)
            except ValueError:  # no room
                continue

            d = 0

            new_node = tuple(a + b for a, b in zip(home_node, direction))
            x = new_node[0]
            y = new_node[1]

            bridges = [(x, y)]

            # check next space and next next space
            try:
                if board[x][y] != ' ' or board[x+dx][y+dy] != ' ' or x < 0 or x+dx < 0 or y < 0 or y+dy < 0:
                    continue
            except IndexError:
                continue

            directions[home_node].append(direction)

            while d < distance and board[x][y] == ' ' and 0 <= x < length and 0 <= y < width:
                new_node = tuple(a + b for a, b in zip(new_node, direction))
                x = new_node[0]
                y = new_node[1]
                bridges.append((x, y))
                d += 1

            # todo place node on bridge if possible (instead of instantly retreating)

            # undo last move
            new_node = tuple(a - b for a, b in zip(new_node, direction))
            bridges.remove((x, y))

            # add bridges
            for (x, y) in bridges:
                board[x][y] = bridge

            x = new_node[0]
            y = new_node[1]

            board[x][y] = '*'
            nodes.append(new_node)

            # note that this direction has been taken
            if new_node in direction:
                directions[new_node].append(reverse_direction(direction))
            else:
                directions[new_node] = [reverse_direction(direction)]
            num_nodes -= 1

            looped = 0

        if num_nodes == 1:
            generated = True

    usr_board = [[' ' for x in range(width)] for y in range(length)]  # user's board

    # nodes -> numbers
    for x in range(length):
        for y in range(width):
            if board[x][y] == '*':
                count = 0
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if abs(dx) == abs(dy):
                            continue
                        try:
                            if (board[x+dx][y+dy] == '|' and dx != 0) or (board[x+dx][y+dy] == '-' and dy != 0):
                                count += 1
                            if (board[x+dx][y+dy] == '‖' and dx != 0) or (board[x+dx][y+dy] == '=' and dy != 0):
                                count += 2
                        except IndexError:
                            pass

                board[x][y] = count
                usr_board[x][y] = count

    #print('\nPuzzle:')
    #display(usr_board)
    #print('\nSolution:')
    #display(board)

    for x in range(len(usr_board)):
        for y in range(len(usr_board[x])):
            if usr_board[x][y] == ' ':
                usr_board[x][y] = 0


    file = open("puzzles/"+ difficulty + str(i+1).zfill(3) +".txt", "w")
    file.write(str(size) + "\n")
    for line in usr_board:
        string = " ".join(str(x) for x in line)
        file.write(string + "\n")

    file.close()