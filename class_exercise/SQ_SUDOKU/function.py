from utils import *


# "Using depth-first search and propagation, create a search tree and solve the sudoku."
# First, reduce the puzzle using the previous function
def search(values):

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
