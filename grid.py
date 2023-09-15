import matplotlib.pyplot as plt
import numpy as np
from PIL import ImageGrab as ig
from pynput import keyboard
import skimage.transform as transform
import time
import win32gui

import pandas as pd

def clean_grid(grid):
	col = grid.copy()
	row = grid.copy()
	threshold = 200

	col_sums = col.sum(axis = 0)
	row_sums = row.sum(axis = 1)

	col_sums[col_sums <= threshold] = 0
	row_sums[row_sums <= threshold] = 0

	cols = create_mask(col_sums)
	rows = create_mask(row_sums)

	grid[rows == -1, :] = 0
	grid[:, cols == -1] = 0

	grid[rows > 0, :] = 1
	grid[:, cols > 0] = 1

	return grid

def convert_to_luminance(image):
	weights = np.array([0.2126, 0.7152, 0.0722]).reshape(1, 1, 3)
	
	return (weights * image).sum(axis = 2)

def create_mask(line):
	for i in range(len(line)):
		if line[i] != 0:
			pos = 1

			if i + pos < len(line) - 1:
				while line[i + pos] != 0:
					line[i + pos] = -1
					pos += 1

	return line

def detect_ad(delay, icon_data):
	time.sleep(delay)

	d = 800
	win = 256 - convert_to_luminance(np.array(ig.grab((0, 0, d, d))))

	threshold = 50
	win[win <= threshold] = 1
	win[win > threshold] = 0

	left = 740
	right = 790
	top = 40
	bottom = 75

	win = win[top : bottom, left : right].astype(int)

	row_sum = win.sum(axis = 0).astype(bool).astype(int)
	col_sum = win.sum(axis = 1).astype(bool).astype(int)

	left = row_sum.argmax()
	right = win.shape[1] - row_sum[::-1].argmax()
	top = col_sum.argmax()
	bottom = win.shape[0] - col_sum[::-1].argmax()

	win = win[ top : bottom, left : right]
	win = transform.resize(win, (16, 16), preserve_range = True)

	test = (win == icon_data).mean()
	if test >= 0.9:
		print('Ad detected')
		return True

	return False

def get_grid(win, threshold):
	left_init = 25
	right_init = 450
	top_init = 200
	bottom_init = 625

	grid = win.astype(int)[top_init : bottom_init, left_init : right_init]

	grid[grid <= threshold] = 1
	grid[grid > threshold] = 0

	border_width = 3
	pos = 200

	left = grid[pos, :].argmax() + border_width
	right = grid.shape[1] - grid[::-1, :][pos, :].argmax() + 2
	top = grid[:, pos].argmax() + border_width
	bottom = grid.shape[0] - grid[:, ::-1][:, pos].argmax() + 5

	grid = grid[top : bottom, left : right]

	start_left = left_init + left
	start_top = top_init + top

	start_point = (start_left, start_top)

	return (grid, start_point)

def get_grid_boundaries(grid):
	sum_threshold = 250

	row = grid.sum(axis = 0)
	row[row <= sum_threshold] = 0

	col = grid.sum(axis = 1)
	col[col <= sum_threshold] = 0

	row_boundaries = np.where(row.astype(bool).astype(int) == 1)[0].tolist()
	col_boundaries = np.where(col.astype(bool).astype(int) == 1)[0].tolist()

	return (row_boundaries, col_boundaries)

def get_window(name, delay):
	hwnd = win32gui.FindWindow(None, name)

	kbd = keyboard.Controller()
	kbd.press(keyboard.Key.alt)
	try:
		win32gui.SetForegroundWindow(hwnd)
	finally:
		kbd.release(keyboard.Key.alt)

	time.sleep(delay)

	d = 800

	win32gui.MoveWindow(hwnd, 0, 0, d, d, True)

	return np.array(ig.grab((0, 0, d, d)))

def get_empty_cell_midpoint(grid, zeros):
	row_boundaries, col_boundaries = get_grid_boundaries(grid)
	midpoints = []

	for point in zeros:
		row = point[0]
		col = point[1]

		left = col_boundaries[col]
		right = col_boundaries[col + 1]
		top = row_boundaries[row]
		bottom = row_boundaries[row + 1]

		mid_row = int((top + bottom) / 2)
		mid_col = int((left + right) / 2)

		midpoints.append((mid_row, mid_col))

	return midpoints

def load_icon_data():
	return np.genfromtxt('x.csv', delimiter = ',').astype(int)

def plot_window(image):
	plt.imshow(image, cmap = 'Greys')
	plt.show()