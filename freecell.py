#! /usr/bin/env python

"""A Freecell problem"""

import argparse

from search import Problem, astar


class FreeCell(Problem):
    def __init__(self, filename):
        """Read in a FreeCell game."""
        pass #todo

    def initial_state(self):
        return None #todo

    def is_goal(self, state):
        return False #todo

    def next_states(self, state):
        return [] #todo

    def heuristic(self, state):
        return 0 #todo

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    freecell_prob = FreeCell(args.filename)
    for move in astar(freecell_prob):
        print move


if __name__ == '__main__':
    main()
