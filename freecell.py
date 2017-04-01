#! /usr/bin/env python

"""A Freecell problem"""

import argparse

from search import Problem, astar

SUITS = ('h', 'd', 'c', 's')


class Card:
    def __init__(self, card_str):
        """Initialize from the 2-character card string.

        Letters are allowed to be upper or lower case.
        """
        self._str = card_str
        card_str = card_str.lower()
        self._suit = SUITS.index(card_str[1])
        self._is_red = self._suit < 2
        rank_str = card_str[0]
        if rank_str.isdigit():
            self._rank = int(rank_str)
        else:
            self._rank = {'a': 1, 't': 10, 'j': 11, 'q': 12, 'k': 13}[rank_str]

    @property
    def suit(self):
        """The numbered suit (from SUITS)"""
        return self._suit

    @property
    def rank(self):
        """Should return a number for the rank (e.g. Ace is 1, and King is 
        13)
        """
        return self._rank

    def is_red(self):
        """Return True if the card is red; return False if it's black."""
        return self._is_red

    def __str__(self):
        return self._str


class FreeCellState:
    pass #todo


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
    parser.add_argument('filename', help=(
        'A csv file where each row represents a pile '
        'from top to bottom.'
        ' Each card is a two-character string (e.g. "3C").'
        ' Non-single-digit cards are one of these strings: '
        '"A", "T", "J", "Q", and "K". The suits are "H", '
        '"D", "C", and "S". All letters may be upper or '
        'lower case.'
    ))
    args = parser.parse_args()

    freecell_prob = FreeCell(args.filename)
    for move in astar(freecell_prob):
        print move


if __name__ == '__main__':
    main()
