# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?
A: In the naked twins problem, we identify 2 boxes with 2 identical possible remaining digits in the same peer group. We use the logical constraints of the puzzle (1-9 in each row, column, and square) to further reduce the possible remaining digits in the rest of the peer group by eliminating the 2 digits from the naked twins boxes from consideration. After constraining the problem in this way, the set of possible solutions is reduced, and may be further constrained by iterating over other strategies (only_one, eliminate) again after implementing naked_twins, or at least shrinking the search space. 

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?
A: In the original problem, the logical constraints of the puzzle (1-9 in each row, column and square) allow us to implement strategies so shrink the possible outcomes. By adding an additional diagonal constraint, the set of possible outcomes is shrunk even further when using strategies to minimize the possible outcomes (only_one, eliminate, naked_twins).

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in function.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
