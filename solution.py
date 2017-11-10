assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Find all instances of naked twins

    Step 1 : first find all possible naked twins values on the board
    Step 2 : then we use those values and isolate only the ones that appears more than once on the board - Twin Value list
    Step 3 : using the Twin value list, iterate through our unitlist and find units that have square with the twin value
    Step 4 : once we isolated the possible units with our Twin Values, we get a list of all values for that unit
    Step 5 : with the unit value list, we confirm our naked-twins by verifying that they occur more than once in a unit and add them to our list.
    Step 6 : with the confirmed set of naked-twins, we search the units that have them and add them to a dictionary
    Step 7 : Eliminate the naked twins as possibilities for their peers

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Step 1
    all_possible_naked_twins_values = [values[box] for box in values.keys()
                                       if len(values[box]) == 2]

    # Step 2
    twins_value_lst = [frstTwinVal for frstTwinVal in all_possible_naked_twins_values
                       if all_possible_naked_twins_values.count(frstTwinVal) > 1]

    # Step 3
    units_with_frstTwinVal = [unit for unit in unitlist for frstTwinVal in twins_value_lst for s in unit
                              if values[s] == frstTwinVal]

    # Step 4
    units_with_twins_value_lst = dict(("+".join(unit), [values[s] for s in unit]) for unit in units_with_frstTwinVal)

    # Step 5
    naked_twin_list = [twins for twins in twins_value_lst for unit in units_with_frstTwinVal
                       if units_with_twins_value_lst["+".join(unit)].count(twins) > 1]

    # Step 6
    units_with_naked_twins = dict(("+".join(unit), naked) for unit in units_with_frstTwinVal for naked in naked_twin_list
                                  if units_with_twins_value_lst["+".join(unit)].count(naked) > 1)

    # Step 7
    for naked_unit in units_with_naked_twins.keys():
        naked = units_with_naked_twins[naked_unit]

        # we just need to iterate through them and for squares that are not the ones with the naked-twins values,
        for box in naked_unit.split('+'):

            # if the boxes are not part of the naked-twins.
            if values[box] != naked:
                for digit in naked:
                    # remove the digits from boxes that are not part of the naked-twins.
                    values[box] = values[box].replace(digit, '')
    return values

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s + t for s in a for t in b]

rows = 'ABCDEFGHI'
cols = '123456789'

## create board and different views into the boards boxes
boxes = cross(rows, cols)

# and units: row_units, column_units, square_units

# Element example: row_units
# row_units[0] = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
# This is the top most row.
row_units = [cross(r, cols) for r in rows]

# Element example: column_units
# column_units[0] = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
# This is the left most column.
column_units = [cross(rows, c) for c in cols]

# Element example:square_units
# square_units[0] = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
# This is the top left square.
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]


# Creating diagonal units
# Element example:diagonal_units
# diagonal_units[0] = ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']
# A diagonal sudoku is like a regular sudoku, except that among the two main diagonals,
#   the numbers 1 to 9 should all appear exactly once.
colslist = list(cols)
colslist.reverse()
revcols = "".join(colslist)
diagonal_units = [[rs + cs for rs, cs in zip(rows, cols)], [rs + cs for rs, cs in zip(rows, revcols)]]

# now a list of units
unitlist = row_units + column_units + square_units + diagonal_units

# create dictionaries
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - set([s])) for s in boxes)
traversed = dict((s, False) for s in boxes)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    board = dict(((boxes[i], grid[i]) for i in range(len(grid))))
    for box in board:
        if board[box] == '.':
            board[box] = '123456789'
    return board

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """Eliminate values from peers of each box with a single value.
        Go through all the boxes, and whenever there is a box with a single value,
        eliminate this value from the set of values of all its peers.
        Args:
            values: Sudoku in dictionary form.
        Returns:
            Resulting Sudoku in dictionary form after eliminating values.
        """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit, '')
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.
        Go through all the units, and whenever there is a unit with a value
        that only fits in one box, assign the value to this box.
        Input: Sudoku in dictionary form.
        Output: Resulting Sudoku in dictionary form after filling in only choices.
        """
    new_values = values.copy()  # note: do not modify original values
    for unit in unitlist:
        for digit in '123456789':
            digitlist = [box for box in unit if digit in values[box]]
            if (len(digitlist)) == 1:
                new_values[digitlist[0]] = digit
    return new_values

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # use eliminate, only_choice, naked_twins to try to solve the puzzle.
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    # "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function

    values = reduce_puzzle(values)
    if values is False:
        return False
    if len([box for box in boxes if len(values[box]) == 1]) == 81:
        # we are done
        return values

    # Choose one of the unfilled squares with the fewest possibilities
    n, box = min((len(values[box]), box) for box in boxes if len(values[box]) > 1)

    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for digit in values[box]:
        new_values = values.copy()
        new_values[box] = digit
        attempt = search(new_values)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')