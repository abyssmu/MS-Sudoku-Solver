import numpy as np

# After several hours of fiddling with the grid builder,
# I was much too lazy to do this from scratch. So I looked
# up a solution.

# I did spruce it up a bit by numpy-ifying it.

# Overall solver solution from backtracking section (2nd) from:
# https://www.geeksforgeeks.org/sudoku-backtracking-7/#

def get_box(puzzle_data, pos):
	y = pos[0]
	x = pos[1]

	left = x - x % 3
	right = x + 3 - x % 3
	top = y - y % 3
	bottom = y + 3 - y % 3

	return (left, right, top, bottom)

def verify_box(box, num):
	return num not in box

def verify_col(col, num):
	return num not in col

def verify_row(row, num):
	return num not in row

def solve_puzzle(puzzle_data):
	if puzzle_data.min() != 0:
		return True

	# Solution to find first zero from:
	# https://stackoverflow.com/questions/20938586/get-minimum-x-and-y-from-2d-numpy-array-of-points

	first_zero = np.unravel_index(np.argmin(puzzle_data), puzzle_data.shape)

	row = puzzle_data[first_zero[0], :]
	col = puzzle_data[:, first_zero[1]]

	left, right, top, bottom = get_box(puzzle_data, first_zero)
	box = puzzle_data[top : bottom, left : right]

	for num in range(1, 10):
		result = verify_box(box, num) and verify_col(col, num) and verify_row(row, num)

		if result:
			puzzle_data[first_zero] = num

			if solve_puzzle(puzzle_data):
				return True

			puzzle_data[first_zero] = 0

	return False