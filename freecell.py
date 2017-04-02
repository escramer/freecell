#! /usr/bin/env python

"""A Freecell problem"""

import csv
import argparse

from search import Problem, astar

SUITS = ('H', 'D', 'C', 'S')


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
        

class Card:
    class _CardMap(object):
        """Maps a card string to its pair of integers."""
        
        def __init__(self):
            ranks = ['A']
            for rank in xrange(2, 10):
                ranks.append(str(rank))
            ranks += ['T', 'J', 'Q', 'K']
            
            int_to_str = {}
            str_to_int = {}
            for rank_num, rank_name in enumerate(ranks, start=1):
                for suit_num, suit_name in enumerate(SUITS):
                    pair = (rank_num, suit_num)
                    card_name = rank_name + suit_name
                    int_to_str[pair] = card_name
                    str_to_int[card_name] = pair

            self._int_to_str = int_to_str
            self._str_to_int = str_to_int

        def str_to_int(self, card_str):
            """Return the integer pair representing this card string.

            card_str is a two-character string representing the card.
            Letters may be upper or lower case.
            """
            return self._str_to_int[card_str.upper()]

        def int_to_str(self, rank, suit):
            """Return the string representing this card.
            """
            return self._int_to_str[(rank, suit)]

            
    def __init__(self, rank, suit):
        """Suit and rank are integers."""
        self._suit = suit
        self._rank = rank
        self._is_red = suit < 2

    @classmethod
    def from_str(cls, card_str):
        """Return a Card from the 2-character card string.

        Letters are allowed to be upper or lower case.
        """
        return cls(*cls._card_map.str_to_int(card_str))

    @property
    def suit(self):
        """Return the numbered suit (from SUITS)"""
        return self._suit

    @property
    def rank(self):
        """Return a number for the rank (e.g. Ace is 1, and King is 
        13)
        """
        return self._rank

    def is_red(self):
        """Return True if the card is red; return False if it's black."""
        return self._is_red

    def __str__(self):
        return self._card_map.int_to_str(self._rank, self._suit)

    def __eq__(self, other):
        return self._suit == other._suit and self._rank == other._rank

    def __hash__(self):
        return hash((self._suit, self._rank))

    _card_map = _CardMap()


class FreeCellState:
    def __init__(self, filename):

#        The value at index n refers to SUITS[n]. The value
#        refers to the maximum rank on the foundation. If 0,
#        the foundation is empty.
        self._foundations = [0] * 4

        self._freecells = set()
        self._tableau = set()

        with open(filename) as file_obj:
            for row in csv.reader(file_obj):
                pile = Pile()
                for card_str in row:
                    pile.push(Card(card_str))
                self._tableau.add(pile)

        
        


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
