import grid
import input
import number
import puzzle
import solver

import keyboard

while(True):
	keyboard.wait('space')
	print('started')

	delay = 5
	win = grid.convert_to_luminance(grid.get_window('Microsoft Sudoku', delay))

	number_data = number.load_number_data('number_data/')

	sum_threshold = 250
	grid_data, start_point = grid.get_grid(win, sum_threshold)
	grid_data = grid.clean_grid(grid_data)

	n = 9
	puzzle_data = puzzle.create_blank_puzzle(n)
	puzzle_data = puzzle.create_puzzle(grid_data, puzzle_data, number_data)

	zeros = puzzle.get_zero_locations(puzzle_data)
	midpoints = grid.get_empty_cell_midpoint(grid_data, zeros)

	solver.solve_puzzle(puzzle_data)
	# puzzle.print_puzzle(puzzle_data)

	delay = 1 / 20
	input.fill_in_puzzle(puzzle_data, start_point, zeros, midpoints, delay)

	print('finished')