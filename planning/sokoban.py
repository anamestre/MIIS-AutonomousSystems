#!/usr/bin/env python3

import argparse
import sys


def parse_arguments(argv):
    parser = argparse.ArgumentParser(description='Solve Sudoku problems.')
    parser.add_argument("-i", help="Path to the file with the Sokoban instance.")
    return parser.parse_args(argv)


class SokobanGame(object):
    """ A Sokoban Game. """
    def __init__(self, string):
        """ Create a Sokoban game object from a string representation such as the one defined in
            http://sokobano.de/wiki/index.php?title=Level_format
        """
        lines = string.split('\n')
        self.h, self.w = len(lines), max(len(x) for x in lines)
        self.player = None
        self.walls = set()
        self.boxes = set()
        self.goals = set()
        for i, line in enumerate(lines, 0):
            for j, char in enumerate(line, 0):
                if char == '#':  # Wall
                    self.walls.add((i, j))
                elif char == '@':  # Player
                    assert self.player is None
                    self.player = (i, j)
                elif char == '+':  # Player on goal square
                    assert self.player is None
                    self.player = (i, j)
                    self.goals.add((i, j))
                elif char == '$':  # Box
                    self.boxes.add((i, j))
                elif char == '*':  # Box on goal square
                    self.boxes.add((i, j))
                    self.goals.add((i, j))
                elif char == '.':  # Goal square
                    self.goals.add((i, j))
                elif char == ' ':  # Space
                    pass  # No need to do anything
                else:
                    raise ValueError(f'Unknown character "{char}"')

    def is_wall(self, x, y):
        """ Whether the given coordinate is a wall. """
        return (x, y) in self.walls

    def is_box(self, x, y):
        """ Whether the given coordinate has a box. """
        return (x, y) in self.boxes

    def is_goal(self, x, y):
        """ Whether the given coordinate is a goal location. """
        return (x, y) in self.goals

def write_problem(board, output, name):
    with open(output, 'w') as file:
        file.write("(define (problem " + name + ") \n")
        file.write("(:domain sokoban) \n")
        file.write('(:objects ')
        for col in range(board.w):
            for fila in range(board.h):
                file.write(" pos_" + str(fila) + "_" + str(col))
        file.write(" - position) \n")
        file.write("(:init \n")
        for col in range(board.w):
            for fila in range(board.h):
                pos = "pos_" + str(fila) + "_" + str(col)
                if(board.is_wall(fila, col)):
                    file.write("(haswall "+ pos + ") \n")
                elif(board.is_box(fila, col)):
                    file.write("(hasbox " + pos + ") \n")
                
                nextF = fila + 1
                nextC = col + 1
                if(nextF < board.h):
                    pos_next = "pos_" + str(nextF) + "_" + str(col)
                    file.write("(next " + pos + " " + pos_next + ") \n")
                    file.write("(next " + pos_next + " " + pos + ") \n")
                    nextnextF = nextF + 1
                    if(nextnextF < board.h):
                        pos_next = "pos_" + str(nextnextF) + "_" + str(col)
                        file.write("(double_next " + pos + " " + pos_next + ") \n")
                        file.write("(double_next " + pos_next + " " + pos + ") \n")
                if(nextC < board.w):
                    pos_next = "pos_" + str(fila) + "_" + str(nextC)
                    file.write("(next " + pos + " " + pos_next + ")\n")
                    file.write("(next " + pos_next + " " + pos + ")\n")
                    nextnextC = nextC + 1
                    if(nextnextC < board.w):
                        pos_next = "pos_" + str(fila) + "_" + str(nextnextC)
                        file.write("(double_next " + pos + " " + pos_next + ")\n")
                        file.write("(double_next " + pos_next + " " + pos + ")\n")
                
                if (fila, col) == board.player:
                    file.write("(at agent " + pos + ")\n")
        
        file.write("(= (num_teleports) 0))\n" )
        file.write("(:goal (and")
        
        for (fila, col) in board.goals:
             pos = "pos_" + str(fila) + "_" + str(col)
             file.write("(hasbox " + pos + ") \n")
        file.write(")))")
            
                
    


def main(argv):
    args = parse_arguments(argv)
    with open(args.i, 'r') as file:
        board = SokobanGame(file.read().rstrip('\n'))
    # TODO - Some of the things that you need to do:
    #  1. (Previously) Have a domain.pddl file somewhere in disk that represents the Sokoban actions and predicates.
    #  2. Generate an instance.pddl file from the given board, and save it to disk.
    #  3. Invoke some classical planner to solve the generated instance.
    #  3. Check the output and print the plan into the screen in some readable form.
    
    write_problem(board, "test.pddl", "box")    
    


if __name__ == "__main__":
    main(sys.argv[1:])
