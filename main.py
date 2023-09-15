import grid
import input
import number
import puzzle
import solver

def go():
	ad_x = 765
	ad_y = 57
	n = 9
	play_x = 350
	play_y = 575
	sum_threshold = 250

	number_data = number.load_number_data('number_data/')
	icon_data = grid.load_icon_data()

	while(True):
		delay = 15
		ad_detected = grid.detect_ad(delay, icon_data)

		while ad_detected:
			input.click_at_point(0, ad_x, ad_y)
			ad_detected = grid.detect_ad(delay, icon_data)

		win = grid.convert_to_luminance(grid.get_window('Microsoft Sudoku', delay))

		grid_data, start_point = grid.get_grid(win, sum_threshold)
		grid_data = grid.clean_grid(grid_data)

		puzzle_data = puzzle.create_blank_puzzle(n)
		puzzle_data = puzzle.create_puzzle(grid_data, puzzle_data, number_data)

		zeros = puzzle.get_zero_locations(puzzle_data)
		midpoints = grid.get_empty_cell_midpoint(grid_data, zeros)

		solver.solve_puzzle(puzzle_data)
		# puzzle.print_puzzle(puzzle_data)

		delay = 1 / 20
		input.fill_in_puzzle(puzzle_data, start_point, zeros, midpoints, delay)

		delay = 3
		input.click_at_point(delay, play_x, play_y)
		input.click_at_point(delay, play_x, play_y)
		input.click_at_point(delay, play_x, play_y)

go()