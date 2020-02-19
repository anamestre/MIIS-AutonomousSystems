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

    # TODO: Map the SAT assignment back into a Sudoku solution
    return solution

def v(i, j, d): 
    return 81 * (i) + 9 * (j) + d # ojo al -1 q n esta


def check_row(coords, starty, finishy,clauses):
    for x , y in coords:
        for s in range(starty, finishy):
            for k in range(1,10):
                clauses.append([-v(x, y, k), -v(x, s, k)])

def check_col(coords, startx, finishx, clauses):
    for x , y in coords:
        for s in range(startx, finishx):
            for k in range(1,10):
                clauses.append([-v(x, y, k), -v(s, y, k)]) # no por estar en la mateixa fila el mateix numero K

def check_box(coords, startx, starty, clauses):
    check_row(coords, starty, starty + 3, clauses) #el +3 es per anarse movent dins del lbloc de 3, qe acabara a la posicio indicada +3.
    check_col(coords, startx, startx + 3, clauses)




def generate_theory(board, verbose):
    """ Generate the propositional theory that corresponds to the given board. """
    size = board.size()
    clauses = []
    variables = {}
    
    for x, y in board.all_coordinates(): # per a cada coordenada de la board
        for k in range(1, 10): # per a cada valor possible que pot agafar
            for kp in range(k + 1, 10): #per cada valor possible que pot agafar. no contemplem l'1 perq vols mirar que a partir del seguent no hi hagui cap numero igual, pq l'1 ja hi pot ser
                clauses.append([-v(x, y, k), -v(x, y, kp)]) # per les coordenades x ,y no hi poden haver numeros diferents a k. cada posicio pot tenir max 1 valor. i no diferent al que hi ha a k.

    for x in range (0,9):
        check_row([(x,y) for y in range(0,9)], 0, 9, clauses)#clauses rows chek, que el valor no estigui repetit mateixa fila
        check_col([(y,x) for y in range(0,9)], 0, 9, clauses) #clauses cols, que el valor no estigui repetit mateixa col

   #box 3x3
    for x in 0,3,6: # per cada blocs de 3
        for y in 0,3,6:
            check_box([((x + k % 3), (y + k // 3)) for k in range(0, 9)], x, y,clauses)  # clauses rows, modul i divisio per mouret dins de cada bloc de 3

    return clauses, variables, size


def count_number_solutions(board, verbose=False):
    count = 0

    # TODO

    print(f'Number of solutions: {count}')


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
