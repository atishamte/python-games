# SNAKE GAME
# Use ARROW KEYS to play,
# SPACE BAR for pausing/resuming and
# Esc Key for exiting

import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN
from random import randint

rows = 0
cols = 0
game_type = 0

while rows not in range(15, 26):
	rows = int(input("Enter number of rows between 15 to 25 : "))

while cols not in range(50, 271):
	cols = int(input("Enter number of columns between 50 to 70 : "))

while game_type not in ['Y', 'N']:
	game_type = input("Kill when touched boundary : Y or N : ").upper()

# Initializing values
curses.initscr()
curses.noecho()
curses.curs_set(0)
cons = curses.newwin(rows, cols, 0, 0)
cons.keypad(1)
cons.border(0)
cons.nodelay(1)
key = KEY_RIGHT
score = 0

# Initial snake co-ordinates
snake = [[1, 1]]

# First food pointer coordinates
food_pointer = [randint(5, rows - 2), randint(5, cols - 2)]

cons.addch(food_pointer[0], food_pointer[1], '*')

# Esc key is not pressed
while key != 27:

	previous_key_pressed = key

	cons.border(0)
	cons.addstr(0, 2, ' Score : ' + str(score) + ' ')
	cons.addstr(0, ((cols // 2) - 3), ' SNAKE ')

	# Increases the speed of as its length increases
	timeout = 150 - (int(len(snake)) if int(len(snake)) < 75 else 75)

	# slow down a snake a bit for vertical movement
	if key in [KEY_UP, KEY_DOWN]:
		timeout = round(timeout * 1.5)

	cons.timeout(timeout)

	event = cons.getch()

	key = key if event == -1 else event

	# If SPACE BAR is pressed, wait for another
	if key == ord(' '):
		key = -1
		while key != ord(' '):
			key = cons.getch()
		key = previous_key_pressed
		continue

	# If an invalid key is pressed
	if key not in [KEY_LEFT, KEY_RIGHT, KEY_UP, KEY_DOWN, 27]:
		key = previous_key_pressed

	# Calculates the new head position
	x_count = 0
	y_count = 0
	if key == KEY_DOWN:
		x_count = 1
	elif key == KEY_UP:
		x_count = -1
	elif key == KEY_LEFT:
		y_count = -1
	else:
		y_count = 1

	snake.insert(0, [snake[0][0] + x_count, snake[0][1] + y_count])

	# Exit if snake crosses the boundaries
	if game_type == 'Y':
		if snake[0][0] == 0 or snake[0][0] == (rows - 1) or snake[0][1] == 0 or snake[0][1] == (cols - 1): break
	# If snake crosses the boundaries, make it enter from the other side
	else:
		if snake[0][0] == 0: snake[0][0] = rows - 2
		if snake[0][1] == 0: snake[0][1] = cols - 2
		if snake[0][0] == rows - 1: snake[0][0] = 1
		if snake[0][1] == cols - 1: snake[0][1] = 1

	# If snake touches itself
	if snake[0] in snake[1:]: break

	# When snake eats the food, increase the length
	if snake[0] == food_pointer:
		food_pointer = []
		score += 1
		while food_pointer == []:
			food_pointer = [randint(1, rows - 2), randint(1, cols - 2)]
			if food_pointer in snake: food_pointer = []

		cons.addch(food_pointer[0], food_pointer[1], '*')
	# Else reset the length to old one
	else:
		last = snake.pop()
		cons.addch(last[0], last[1], ' ')

	cons.addch(snake[0][0], snake[0][1], '#')

curses.endwin()

print("Total Score : " + str(score))
