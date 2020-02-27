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
        file.write('(:objects ' + ' '.join(["pos_" + str(x) + "_" + str(y) for x in range(board.w) for y in range(board.h)]))
        file.write(" - position) \n")
        file.write("(:init \n")
        for x in range(board.w):
            for y in range(board.h):
                pos = "pos_" + str(x) + "_" + str(y)
                if(board.is_wall(x, y)):
                    file.write("(haswall "+ pos + ") \n")
                elif(board.is_box(x, y)):
                    file.write("(hasbox " + pos + ") \n")
                
                nextX = x + 1
                nextY = y + 1
                if(nextX < board.w):
                    pos_next = "pos_" + str(nextX) + "_" + str(y)
                    file.write("(next " + pos + " " + pos_next + ") \n")
                    file.write("(next " + pos_next + " " + pos + ") \n")
                    nextnextX = nextX + 1
                    if(nextnextX < board.w):
                        pos_next = "pos_" + str(nextnextX) + "_" + str(y)
                        file.write("(double_next " + pos + " " + pos_next + ") \n")
                        file.write("(double_next " + pos_next + " " + pos + ") \n")
                if(nextY < board.h):
                    pos_next = "pos_" + str(x) + "_" + str(nextY)
                    file.write("(next " + pos + " " + pos_next + ")\n")
                    file.write("(next " + pos_next + " " + pos + ")\n")
                    nextnextY = nextY + 1
                    if(nextnextY < board.h):
                        pos_next = "pos_" + str(nextnextY) + "_" + str(y)
                        file.write("(double_next " + pos + " " + pos_next + ")\n")
                        file.write("(double_next " + pos_next + " " + pos + ")\n")
                
                if (x, y) == board.player:
                    file.write("(at agent " + pos + ")\n")
        
        file.write("(= (num_teleports) 0))\n" )
        file.write("(:goal (and")
        
        for (y, x) in board.goals:
             pos = "pos_" + str(x) + "_" + str(y)
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
    print(board.player)
    print(board.boxes)
    print(board.walls)
    
    


if __name__ == "__main__":
    main(sys.argv[1:])
