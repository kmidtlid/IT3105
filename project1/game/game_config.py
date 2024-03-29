# This file contains declaration of the pivotal parameters to be used when initializing a game.

# Shape of the board: 'triangle' or 'diamond'
shape = "diamond"

# Size of the board: Integer larger than 1
size = 4

# Cells not containing pegs when initialized: (i, j) where i and j are coordinates (0-indexed)
openCells = [(2, 1)]

# Legal directions to move
directions = {"UP": (0, -1), "UPRIGHT": (1, -1), "RIGHT": (1, 0), "DOWNRIGHT": (1, 1), "DOWN": (0, 1), "DOWNLEFT": (-1, 1), "LEFT": (-1, 0), "UPLEFT": (-1, -1)}

# Visualization delay between frames, in ms 
delay = 1000

# Rewards
win = 10
lose = 0
default = 0