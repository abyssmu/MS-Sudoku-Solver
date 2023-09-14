import numpy as np

def extract_num(num_bb, number_data):
	if num_bb.sum() == 0:
		return 0

	comparison = np.array([(num_bb == i).mean() for i in number_data])

	return comparison.argmax() + 1

def get_number_bb(cell):
	row = cell.sum(axis = 1).astype(bool).astype(int)
	col = cell.sum(axis = 0).astype(bool).astype(int)

	x_start = col.argmax()
	x_end = cell.shape[1] - col[::-1].argmax() - 1
	y_start = row.argmax()
	y_end = cell.shape[0] - row[::-1].argmax() - 1

	return cell[y_start : y_end, x_start : x_end]

def load_number_data(folder):
	number_data = [np.genfromtxt(folder + str(i + 1) + '.csv', delimiter = ',').astype(int)
					for i in range(9)]

	return number_data