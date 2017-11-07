# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?

A:  Naked twins technique - 2 grid boxes amongst peers contain the same digits, for example F3 and I3 has the same values 23.  
		For sure one of the boxes F3 or I3 either 2 or 3 is locked and no other boxes in the third column can have 2 or 3. 
		Based on this, check the 2 digits in their peers and remove them. This process is called Naked twins technique.
		Apply this constraint using the following steps 

    Step 1 : Identify boxes with only two digits and match them in pairs.
		Step 2 : Find pairs of identical values within each unit.
		Step 3 : Remove the digits of the naked-twin pair from the other boxes in the unit.
		Step 4 : Apply this constraint repeatedly until the puzzle stops changing.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: The constraint propagation is similar to the square sudoku problem. For diagonl, we need to add the diagonal constraint.
We need to create 2 additional units whihc represent the diagonal units "X".
diagonal_units[0] = ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']
diagonal_units[1] = ['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']
By further applying the elimination, only choice, naked-twin and search tree techniques, we can use constraint propagation
to solve the sudoku puzzle.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - Fill in the required functions in this file to complete the project.
* `test_solution.py` - You can test your solution by running `python -m unittest`.
* `PySudoku.py` - This is code for visualizing your solution.
* `visualize.py` - This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the `assign_value` function provided in solution.py

### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login) for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

