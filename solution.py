assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    
    # For loop over all dict entries of 'values', if a box has only 2 choices
    # then search their peers for boxes with the same 2 choices. If found, append 
    # to the list 'twin_values'
    twin_values = []
    for box in values.keys():
    	if len(values[box]) == 2:
    		twin_test = [twin_peer for twin_peer in peers[box] if values[twin_peer] == values[box]]
    		while len(twin_test) > 0:
    			twin_values.append([box,twin_test.pop()])
    
    # Eliminate the naked twins as possibilities for their peers

    # For loop over all 'twin_values' and determine the right 'kind' of peer (row,column,square or diag)
    # Apply the newly built 'remove_naked_twins()' function below to update the 'values' dictionary
    for boxes in twin_values:
    	if boxes[1] in row_peers[boxes[0]]:
    		values = remove_naked_twins(values, boxes, row_peers)
    	if boxes[1] in column_peers[boxes[0]]:
    		values = remove_naked_twins(values, boxes, column_peers)
    	if boxes[1] in square_peers[boxes[0]]:
    		values = remove_naked_twins(values, boxes, square_peers)
    	if boxes[1] in diag_peers[boxes[0]]:
    		values = remove_naked_twins(values, boxes, diag_peers)
    
    return values

def remove_naked_twins(values, boxes, subpeers):
    "Given a pair of naked_twins boxes and set of peers, update peers to remove naked_twins values."
    twin_digits = values[boxes[0]] 						# 2 digits of the naked_twins values
    boxes_to_have_digits_removed = subpeers[boxes[0]] 	# Create a copy of the peers to be updated
    boxes_to_have_digits_removed.remove(boxes[1]) 		# Remove the peer from the set of peers to update
    for p in boxes_to_have_digits_removed: 				# For every peer not included in the naked_twins
    	for j in range(len(twin_digits)): 				# For every digit in twin_digits
    		values = assign_value(values=values, box=p, value=values[p].replace(twin_digits[j],''))
    return values    
    
def cross(A, B):
    "Cross product of elements in A and elements in B."
    # From utils.py in Udacity provided code
    return [s+t for s in A for t in B] 

def grid_values(grid):
    "Convert grid into a dict of {square: char} with '.' for empties."
    # From utils.py in Udacity provided code
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    "Display these values as a 2-D grid."
    # From utils.py in Udacity provided code
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    """
    Note: This is sourced from utils.py in the Udacity provided code.
    
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """
    Note: This is sourced from utils.py in the Udacity provided code.

    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values=values, box=dplaces[0], value=digit)
    return values

def reduce_puzzle(values):
    """
    Note: Substantial portion of the code below 
    sourced from utils.py in the Udacity provided code.

    Iterate eliminate() and only_choice(). 
    If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)   
        values = only_choice(values) 
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def solve(grid):
    "Given a grid, solve a sudoku puzzle."
    # Note: Portion of below code sourced from utils.py in the Udacity provided code.
    # Account for either a string or dict sudoku puzzle being passed into solve()
    if type(grid) == dict:
    	values = grid
    else:
    	values = grid_values(grid)

    values = reduce_puzzle(values)
    if values is False:
        return False 
    if all(len(values[s]) == 1 for s in boxes): 
        return values
    # If constraint propogation doesn't work, must do search
    values = search(values)
    if values is False:
        return False 
    if all(len(values[s]) == 1 for s in boxes): 
        return values
    return 

def search(values):
    "Using depth-first search and propagation, try all possible values."
    # Note: This is sourced from utils.py in the Udacity provided code.
    # Chose one of the unfilled square s with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = solve(new_sudoku)
        if attempt:
            return attempt

# From utils.py in Udacity provided code
rows  = 'ABCDEFGHI'
cols  = '123456789'
boxes = cross(rows, cols)

row_units    = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# Add in diag_units
# First pass captures the diagonal going top left to bottom right (A1,B2,...,I9) 
# Second pass captures the diagnoal going bottom left to top right (I1,H2,...,A9)
# Since cross() returns individual lists, must access the first element with [0]
diag_units = [[cross(rows[i],cols[i])[0] for i in range(len(rows))]] # first pass
diag_units.append([cross(rows[-i-1],cols[i])[0] for i in range(len(rows))]) # second pass

unitlist = row_units + column_units + square_units + diag_units # add diag_units to unitlist
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

# Separate out peers into distinct dicts that represent what kind of peer they are
# This is needed to distinguish which boxes need to have values removed by naked_twins
row_dict 		= dict((s, [r for r in row_units if s in r]) for s in boxes)
column_dict 	= dict((s, [c for c in column_units if s in c]) for s in boxes)
square_dict 	= dict((s, [sq for sq in square_units if s in sq]) for s in boxes)
diag_dict		= dict((s, [d for d in diag_units if s in d]) for s in boxes)

row_peers 		= dict((s, set(sum(row_dict[s],[]))-set([s])) for s in boxes)
column_peers 	= dict((s, set(sum(column_dict[s],[]))-set([s])) for s in boxes)
square_peers 	= dict((s, set(sum(square_dict[s],[]))-set([s])) for s in boxes)
diag_peers 		= dict((s, set(sum(diag_dict[s],[]))-set([s])) for s in boxes)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(grid_values(diag_sudoku_grid)))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
