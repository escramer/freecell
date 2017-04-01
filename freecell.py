#! /usr/bin/env python

"""A Freecell problem"""

import argparse

from search import Problem, astar

SUITS = ('h', 'd', 'c', 's')


class Pile:
    def __init__(self):
        self._pile = []

    def push(self, card):
        self._pile.append(card)

    def empty(self):
        """Return whether or not the pile is empty."""
        return len(self._pile) == 0

    def pop(self):
        rtn = self._pile.pop()

    def __str__(self):
        return ''.join(str(card) for card in self._pile)

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        return self._pile == other._pile


def get_ranks():
    """Return a dictionary mapping a lower case character to its integer rank."""
    rtn = {'a': 1, 't': 10, 'j': 11, 'q': 12, 'k': 13}
    for num in xrange(2, 10):
        rtn[str(num)] = num
    return rtn
        

class Card:
    _ranks = get_ranks()

    def __init__(self, card_str):
        """Initialize from the 2-character card string.

        Letters are allowed to be upper or lower case.
        """
        self._str = card_str
        card_str = card_str.lower()
        if not self.is_card_str(card_str):
            raise ValueError('Incorrect card string: %s' % self._str)
        self._suit = SUITS.index(card_str[1])
        self._is_red = self._suit < 2
        self._rank = self._ranks[card_str[0]]

    @staticmethod
    def is_card_str(str_):
        return isinstance(str_, str) and len(str_) == 2 and \
            str_[1].lower() in SUITS and str_[0].lower() in self._ranks

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

    def __eq__(self, other):
        return self._suit == other._suit and self._rank == other._rank

    def __hash__(self):
        return hash((self._suit, self._rank))


class FreeCellState:
    def __init__(self, filename):
        pass #todo

    def get_foundations(self):
        """Return the foundations as a tuple of 4 integers.

        The value at index n refers to SUITS[n]. The value
        refers to the maximum rank on the foundation. If 0,
        the foundation is empty.
        """
        return (0,) * 4 #todo


class FreeCellProblem(Problem):
    def __init__(self, filename):
        """Read in a FreeCell game."""
        self._init_state = FreeCellState(filename)

    def initial_state(self):
        return self._init_state

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
