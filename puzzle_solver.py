# Puzzle solver

# === Functions ===
def solve_puzzle(points, axis_turns, piece_counter, axis, xmin, xmax, ymin, ymax, zmin, zmax):
	if is_puzzle_solved(points):
		return (points, axis_turns)

	for new_axis in get_new_applicable_axises(axis):
		new_points = get_new_points(points, piece_counter, new_axis)

		if has_collision(points, new_points):
			continue

		(is_within_bounds, nxmin, nxmax, nymin, nymax, nzmin, nzmax) = check_is_within_bounds(new_points, xmin, xmax, ymin, ymax, zmin, zmax)
		if not is_within_bounds:
			continue

		(solution_points, solution_axis_turns) = solve_puzzle(points + new_points, axis_turns + [new_axis], piece_counter + 1, new_axis, nxmin, nxmax, nymin, nymax, nzmin, nzmax)
		if is_puzzle_solved(solution_points):
			return (solution_points, solution_axis_turns)

	return ([], [])


def get_new_applicable_axises(axis):
	if abs(axis) == 1:
		return [2, 3, -2, -3]
	elif abs(axis) == 2:
		return [1, 3, -1, -3]
	else:
		return [1, 2, -1, -2]


def get_new_points(points, piece_counter, new_axis):
	last_point = points[-1]

	new_points = []
	next_point = last_point
	for _ in range(puzzle_pieces[piece_counter]):
		next_point = get_next_point(next_point, new_axis)
		new_points.append(next_point)

	return new_points


def is_puzzle_solved(points):
	return len(points) == number_of_points_in_total


def check_is_within_bounds(new_points, xmin, xmax, ymin, ymax, zmin, zmax):
	last_new_point = new_points[-1]
	(x, y, z) = last_new_point
	xmin = min(xmin, x)
	ymin = min(ymin, y)
	zmin = min(zmin, z)
	xmax = max(xmax, x)
	ymax = max(ymax, y)
	zmax = max(zmax, z)

	if abs(xmax - xmin) >= cube_dimension:
		return (False, xmin, xmax, ymin, ymax, zmin, zmax)
	if abs(ymax - ymin) >= cube_dimension:
		return (False, xmin, xmax, ymin, ymax, zmin, zmax)
	if abs(zmax - zmin) >= cube_dimension:
		return (False, xmin, xmax, ymin, ymax, zmin, zmax)

	return (True, xmin, xmax, ymin, ymax, zmin, zmax)


def has_collision(points, new_points):
	for new_point in new_points:
		if new_point in points:
			return True
	return False


def get_next_point(point, axis):
	(x, y, z) = point
	sign = 1 if axis > 0 else -1
	if abs(axis) == 1:
		return (x+sign, y, z)
	elif abs(axis) == 2:
		return (x, y+sign, z)
	else:
		return (x, y, z+sign)


# Global variables and constants
puzzle_pieces = [2, 2, 2, 1, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1, 1, 2]
starting_points = [(1,1,1), (2,1,1), (3,1,1)]
starting_axis = 1
sxmin = symin = szmin = sxmax = symax = szmax = 1
cube_dimension = 3
number_of_points_in_total = cube_dimension**3


# === Solve and print solution ===
print("Starting...")

(solution_points, solution_axis_turns) = solve_puzzle(starting_points, [starting_axis], 0, starting_axis, sxmin, sxmax, symin, symax, szmin, szmax)
for i in range(len(solution_points)):
	line = str(i) + " ("
	if i % 2 == 0:
		line += "red): "
	else:
		line += "white): "
	line += str(solution_points[i])
	print(line)

for i in range(len(solution_axis_turns)):
	print(str(solution_axis_turns[i]))

print("Done")

