import random, time, copy


# Start the game.
def start():
	# The solution grid.
	zeros = [[0 for _ in range(9)] for _ in range(9)]

	for n in range(0, 10):
		placeBomb(zeros)

	for row in range(0, 9):
		for col in range(0, 9):
			value = lv(row, col, zeros)
			if value == '*':
				updateValues(row, col, zeros)

	# Sets the variable blanks to a grid of blank spaces, because nothing is yet known about the grid.
	blanks = [[' ' for _ in range(9)] for _ in range(9)]

	printBoard(blanks)

	# Start timer
	startTime = time.time()

	# The game begins!
	play(zeros, blanks, startTime)


# Gets the value of a coordinate on the grid.
def lv(row, col, board):
	return board[row][col]


# Places a bomb in a random location.
def placeBomb(board):
	row = random.randint(0, 8)
	col = random.randint(0, 8)
	# Checks if there's a bomb in the randomly generated location. If not, it puts one there.
	# If there is, it requests a new location to try.
	currentRow = board[row]
	if not currentRow[col] == '*':
		currentRow[col] = '*'
	else:
		placeBomb(board)


# Adds 1 to all of the squares around a bomb.
def updateValues(row, col, board):
	# Row above.
	if row - 1 > -1:
		row = board[row - 1]

		if col - 1 > -1:
			if not row[col - 1] == '*':
				row[col - 1] += 1

		if not row[col] == '*':
			row[col] += 1

		if 9 > col + 1:
			if not row[col + 1] == '*':
				row[col + 1] += 1

	# Same row.
	row = board[row]

	if col - 1 > -1:
		if not row[col - 1] == '*':
			row[col - 1] += 1

	if 9 > col + 1:
		if not row[col + 1] == '*':
			row[col + 1] += 1

	# Row below.
	if 9 > row + 1:
		row = board[row + 1]

		if col - 1 > -1:
			if not row[col - 1] == '*':
				row[col - 1] += 1

		if not row[col] == '*':
			row[col] += 1

		if 9 > col + 1:
			if not row[col + 1] == '*':
				row[col + 1] += 1


# When a zero is found, all the squares around it are opened.
def zeroProcedure(row, col, k, board):
	# Row above
	if row - 1 > -1:
		row = k[row - 1]
		if col - 1 > -1: row[col - 1] = lv(row - 1, col - 1, board)
		row[col] = lv(row - 1, col, board)
		if 9 > col + 1: row[col + 1] = lv(row - 1, col + 1, board)

	# Same row
	row = k[row]
	if col - 1 > -1: row[col - 1] = lv(row, col - 1, board)
	if 9 > col + 1: row[col + 1] = lv(row, col + 1, board)

	# Row below
	if 9 > row + 1:
		row = k[row + 1]
		if col - 1 > -1: row[col - 1] = lv(row + 1, col - 1, board)
		row[col] = lv(row + 1, col, board)
		if 9 > col + 1: row[col + 1] = lv(row + 1, col + 1, board)


# Checks known grid for 0s.
def checkZeros(k, board, row, col):
	oldGrid = copy.deepcopy(k)
	zeroProcedure(row, col, k, board)
	if oldGrid == k:
		return
	while True:
		oldGrid = copy.deepcopy(k)
		for x in range(9):
			for y in range(9):
				if lv(x, y, k) == 0:
					zeroProcedure(x, y, k, board)
		if oldGrid == k:
			return


# Places a marker in the given location.
def marker(row, col, board):
	board[row][col] = 'F'
	printBoard(board)


# Prints the given board.
def printBoard(board):
	print('    A   B   C   D   E   F   G   H   I')
	print('  +---+---+---+---+---+---+---+---+---+')
	for row in range(0, 9):
		print(row, '|', lv(row, 0, board), '|', lv(row, 1, board), '|', lv(row, 2, board), '|', lv(row, 3, board), '|',
		      lv(row, 4, board), '|', lv(row, 5, board), '|', lv(row, 6, board), '|', lv(row, 7, board), '|',
		      lv(row, 8, board), '|')
		if not row == 8:
			print('  +---+---+---+---+---+---+---+---+---+')
	print('  +---+---+---+---+---+---+---+---+---+')


# The player chooses a location.
def choose(board, k, startTime):
	# Variables 'n stuff.
	letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
	numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8']
	# Loop in case of invalid entry.
	while True:
		# clear()
		chosen = input('Choose a square (eg. A8) or place a marker (eg. mA8) : ').lower()
		# Checks for valid square.
		if len(chosen) == 3 and chosen[0] == 'm' and chosen[1] in letters and chosen[2] in numbers:
			col, row = (ord(chosen[1])) - 97, int(chosen[2])
			marker(row, col, k)
			play(board, k, startTime)
			break
		elif len(chosen) == 2 and chosen[0] in letters and chosen[1] in numbers:
			return (ord(chosen[0])) - 97, int(chosen[1])
		else:
			choose(board, k, startTime)


# The majority of the game play happens here.
def play(board, k, startTime):
	# Player chooses square.
	col, row = choose(board, k, startTime)
	# Gets the value at that location.
	v = lv(row, col, board)
	# If you hit a bomb, it ends the game.
	if v == '*':
		printBoard(board)
		print('You Lose!')
		# Print timer result.
		print('Time: ' + str(round(time.time() - startTime)) + 's')
		# Offer to play again.
		playAgain = input('Play again? (Y/N): ').lower()
		if playAgain == 'y':
			start()
		else:
			quit()
	# Puts that value into the known grid (k).
	k[row][col] = v
	# Runs checkZeros() if that value is a 0.
	if v == 0:
		checkZeros(k, board, row, col)
	printBoard(k)
	# Checks to see if you have won.
	squaresLeft = 0
	for x in range(0, 9):
		row = k[x]
		squaresLeft += row.count(' ')
		squaresLeft += row.count('F')
	if squaresLeft == 10:
		printBoard(board)
		print('You win!')
		# Print timer result.
		print('Time: ' + str(round(time.time() - startTime)) + 's')
		# Offer to play again.
		playAgain = input('Play again? (Y/N): ')
		playAgain = playAgain.lower()
		if playAgain == 'y':
			start()
		else:
			quit()
	# Repeats!
	play(board, k, startTime)


start()
