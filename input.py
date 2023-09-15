import pyautogui
import time

def fill_in_puzzle(puzzle_data, start_point, zeros, midpoints, delay):
	for i in range(len(zeros)):
		x = start_point[0] + midpoints[i][1]
		y = start_point[1] + midpoints[i][0]

		val = puzzle_data[zeros[i][0], zeros[i][1]]

		pyautogui.moveTo(x, y)
		pyautogui.click()

		time.sleep(delay)
		pyautogui.typewrite(str(val))
		time.sleep(delay)

def click_at_point(delay, x, y):
	time.sleep(delay)
	pyautogui.moveTo(x, y)
	print('click')
	pyautogui.click()
	pyautogui.moveTo(1000, 1000)