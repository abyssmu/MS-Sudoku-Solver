import grid
import number
import numpy as np
import skimage.transform as transform

def create_blank_puzzle(n):
	return np.zeros((n, n), int)

def create_puzzle(grid_data, puzzle, number_data):
	n = 9

	row_boundaries, col_boundaries = grid.get_grid_boundaries(grid_data)

	for row in range(n):
		for col in range(n):
			x_start = col_boundaries[col] + 3
			x_end = col_boundaries[col + 1]
			y_start = row_boundaries[row] + 1
			y_end = row_boundaries[row + 1] - 2

			cell = grid_data[y_start : y_end, x_start : x_end]
			output = transform.resize(number.get_number_bb(cell),
										(30, 30),
										preserve_range = True)
			output = output.astype(bool).astype(int)

			puzzle[row, col] = number.extract_num(output, number_data)

	return puzzle

def get_zero_locations(puzzle_data):
	zeros = np.where(puzzle_data == 0)

	x = zeros[0].tolist()
	y = zeros[1].tolist()

	return [(x[i], y[i]) for i in range(len(x))]

def print_puzzle(puzzle_data):
	output = ''
	for i in range(9):
		if i % 3 == 0: print('-' * 22)

		for j in range(9):
			if j % 3 == 0: output += '|'
			output += str(puzzle_data[i, j]) + ' '

		print(output + '|')
		output = ''
	print('-' * 22)