from random import randint


def print_grid(grid_data):
	print(
		"""
	 {} | {} | {}
	---+---+---
	 {} | {} | {}
	---+---+---
	 {} | {} | {}""".format(*grid_data)
	)


def is_win(board, choice):
	return (
			(board[0] == choice and board[1] == choice and board[2] == choice) or  # across the top
			(board[3] == choice and board[4] == choice and board[5] == choice) or  # across the middle
			(board[6] == choice and board[7] == choice and board[8] == choice) or  # across the bottom

			(board[0] == choice and board[3] == choice and board[6] == choice) or  # down the left side
			(board[1] == choice and board[4] == choice and board[7] == choice) or  # down the middle
			(board[2] == choice and board[5] == choice and board[8] == choice) or  # down the right side

			(board[2] == choice and board[4] == choice and board[6] == choice) or  # diagonal
			(board[0] == choice and board[4] == choice and board[8] == choice)  # diagonal
	)


grid_values = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

player_1 = ''
player_2 = ''
game_mode = ''

while game_mode not in ['1', '2']:
	game_mode = input('Select game mode\n1. Human Vs Human\n2. Human Vs Computer\nChoose the option : ').upper()

while player_1 not in ['X', 'O']:
	player_1 = input('Player 1 - Select your choice (X or O) : ').upper()

player_2 = 'O' if player_1 == 'X' else 'X'

while True:
	while True:
		selection = int(input('Player 1 - Select the position from 1 to 9 : '))
		if grid_values[selection - 1] == ' ':
			grid_values[selection - 1] = player_1
			break

	if is_win(grid_values, player_1):
		print_grid(grid_values)
		print("Player 1 won...")
		break

	if game_mode == '1':
		print_grid(grid_values)
		while True:
			selection = int(input('Player 2 - Select the position from 1 to 9 : '))
			if grid_values[selection - 1] == ' ':
				grid_values[selection - 1] = player_2
				break
	else:
		while True:
			i = randint(0, 9)
			if (grid_values[i] == ' '):
				grid_values[i] = player_2
				break

	if is_win(grid_values, player_2):
		print_grid(grid_values)
		print("Player 2 won...")
		break

	print_grid(grid_values)
