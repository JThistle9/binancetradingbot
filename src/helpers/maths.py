print("loading maths...")

def monotonically_increasing(num_list):
    return all(x>=y for x, y in zip(num_list, num_list[1:]))

def monotonically_decreasing(num_list):
    return all(x<=y for x, y in zip(num_list, num_list[1:]))

def slope(num_list):
	return float(num_list[-1:] - num_list[0]) / len(num_list)
