#!/usr/bin/env python3

import argparse
import itertools
import math
import sys

from utils import save_dimacs_cnf, solve


def parse_arguments(argv):
    parser = argparse.ArgumentParser(description='Solve Sudoku problems.')
    parser.add_argument("board", help="A string encoding the Sudoku board, with all rows concatenated,"
                                      " and 0s where no number has been placed yet.")
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Do not print any output.')
    parser.add_argument('-c', '--count', action='store_true',
                        help='Count the number of solutions.')
    return parser.parse_args(argv)


def print_solution(solution):
    """ Print a (hopefully solved) Sudoku board represented as a list of 81 integers in visual form. """
    print(f'Solution: {"".join(map(str, solution))}')
    print('Solution in board form:')
    Board(solution).print()


def compute_solution(sat_assignment, variables, size):
    solution = []
    for x in range(0, 9):
        for y in range(0, 9):
            for k in range(1, 10):
                val = var(x, y, k)
                # If there's a value on our solution that corresponds to our
                # "base 9" transformation, then we can know the value of that
                # position of the sudoku.
                if(sat_assignment[val]):
                    solution.append(k)
                    break
    return solution

# This transforms our position (x, y) with value k into one single value.
def var(x, y, k): 
    return 81 * x + 9 * y + k

# We write clauses so there is not such K repeated on every row.
def check_row(coords, starty, finishy,clauses):
    for x , y in coords:
        for s in range(starty, finishy):
            if s > y:
                for k in range(1,10):
                    clauses.append([-var(x, y, k), -var(x, s, k)])

# We write clauses so there is not such K repeated on every col.
def check_col(coords, startx, finishx, clauses):
    for x , y in coords:
        for s in range(startx, finishx):
            if s > x:
                for k in range(1,10):
                    clauses.append([-var(x, y, k), -var(s, y, k)])

# We write clauses so there is not such K repeated on every 3x3 box.
def check_box(coords, clauses):
    for x, y in coords:
        for x_, y_ in coords:
            for k in range(1, 10):
                if (x == x_ and y_ > y) or x_ > x:
                    clauses.append([-var(x, y, k), -var(x_, y_, k)])


def generate_theory(board, verbose):
    """ Generate the propositional theory that corresponds to the given board. """
    size = board.size()
    clauses = []
    variables = {}
    
    for x, y in board.all_coordinates():
        val = board.value(x, y)
        if val == 0:
            clauses.append([var(x, y, z) for z in range(1, 10)]) # We add all possible values
            for k in range(1, 10): # for every possible value
                for kp in range(k + 1, 10): 
                    clauses.append([-var(x, y, k), -var(x, y, kp)]) # Only one value per coord
        else:
            clauses.append([var(x, y, val)]) # We add the values we already have on our input

    # Values cannot be repeated on a same row/column
    for x in range (0,9):
        check_row([(x,y) for y in range(0,9)], 0, 9, clauses)
        check_col([(y,x) for y in range(0,9)], 0, 9, clauses)

   # Values cannot be repeated on a same 3x3 block
    for x in 0,3,6:
        for y in 0,3,6:
             # this is how we move through a 3x3 block
            check_box([((x + k % 3), (y + k // 3)) for k in range(0, 9)], clauses) 

    return clauses, variables, size


def count_number_solutions(board, verbose=False):
    count = 0
    clauses, variables, size = generate_theory(board, verbose)
    print("Number of solutions:", count_solutions(clauses, variables, size, count, verbose))

# Recursively we count the number of solutions
def count_solutions(clauses, variables, size, count, verbose):
    sol = solve_sat_problem(clauses, "theory.cnf", size, variables, verbose)
    if sol is None:
        return count
    else:
        # If we have found a solution, we negate that solution and add it as a clause and 
        # launch again the satsolver adding that new clause.
        neg = negate(sol)
        if neg not in clauses:
            clauses.append(neg)
        else:
            return count
        return count_solutions(clauses, variables, size, count + 1, verbose)

# If a clause is "False" we turn it into "True" and if it is "True", we make it "False"
def negate(clause):
    neg_clause = []
    for key in clause:
        if key != 0:
            if clause[key]:
                neg_clause.append(-key)
            else:
                neg_clause.append(key)
    return neg_clause


def find_one_solution(board, verbose=False):
    clauses, variables, size = generate_theory(board, verbose)
    return solve_sat_problem(clauses, "theory.cnf", size, variables, verbose)


def solve_sat_problem(clauses, filename, size, variables, verbose):
    save_dimacs_cnf(variables, clauses, filename, verbose)
    result, sat_assignment = solve(filename, verbose)
    if result != "SAT":
        if verbose:
            print("The given board is not solvable")
        return None
    solution = compute_solution(sat_assignment, variables, size)
    if verbose:
        print_solution(solution)
    return sat_assignment


class Board(object):
    """ A Sudoku board of size 9x9, possibly with some pre-filled values. """
    def __init__(self, string):
        """ Create a Board object from a single-string representation with 81 chars in the .[1-9]
         range, where a char '.' means that the position is empty, and a digit in [1-9] means that
         the position is pre-filled with that value. """
        size = math.sqrt(len(string))
        if not size.is_integer():
            raise RuntimeError(f'The specified board has length {len(string)} and does not seem to be square')
        self.data = [0 if x == '.' else int(x) for x in string]
        self.size_ = int(size)

    def size(self):
        """ Return the size of the board, e.g. 9 if the board is a 9x9 board. """
        return self.size_

    def value(self, x, y):
        """ Return the number at row x and column y, or a zero if no number is initially assigned to
         that position. """
        return self.data[x*self.size_ + y]

    def all_coordinates(self):
        """ Return all possible coordinates in the board. """
        return ((x, y) for x, y in itertools.product(range(self.size_), repeat=2))

    def print(self):
        """ Print the board in "matrix" form. """
        assert self.size_ == 9
        for i in range(self.size_):
            base = i * self.size_
            row = self.data[base:base + 3] + ['|'] + self.data[base + 3:base + 6] + ['|'] + self.data[base + 6:base + 9]
            print(" ".join(map(str, row)))
            if (i + 1) % 3 == 0:
                print("")  # Just an empty line


def main(argv):
    args = parse_arguments(argv)
    board = Board(args.board)

    if args.count:
        count_number_solutions(board, verbose=False)
    else:
        find_one_solution(board, verbose=not args.quiet)


if __name__ == "__main__":
    main(sys.argv[1:])
