#! /usr/bin/env python

"""A Freecell problem"""

from copy import deepcopy, copy
import csv
import argparse

from search import Problem, astar

SUITS = ('H', 'D', 'C', 'S')
MAX_RANK = 13
DECK_SIZE = 52


class Tableau(object):
    def __init__(self, filename):
        """Initialize the tableau from this csv."""
        self._tableau = set()
        with open(filename) as file_obj:
            for row in csv.reader(file_obj):
                pile = []
                for card_str in row:
                    pile.append(Card.from_str(card_str))
                self._tableau.add(tuple(pile))

    def __deepcopy__(self, _):
        return self #todo
        

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

    
    @classmethod
    def from_ranksuit(cls, rank, suit):
        """Return a new Card. rank and suit are integers."""
        pair = (rank, suit)
        assert pair in cls._made_cards
        card = cls._made_cards[pair]
        if card is not None:
            return card

        rtn = cls()
        rtn._suit = suit
        rtn._rank = rank
        rtn._is_red = suit < 2
        cls._made_cards[pair] = rtn
        return rtn

    @classmethod
    def from_str(cls, card_str):
        """Return a Card from the 2-character card string.

        Letters are allowed to be upper or lower case.
        """
        return cls.from_ranksuit(*cls._card_map.str_to_int(card_str))

    @classmethod
    def missing_cards(cls):
        """Return the set of cards ((rank, suit) pairs) that were not 
        instantiated.
        """
        return set(
            pair 
            for pair, card in cls._made_cards.iteritems() 
            if card is None
        )

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

    def __deepcopy__(self, _):
        return self

    def __copy__(self):
        return self        

    _card_map = _CardMap()
    _made_cards = {
        (rank, suit): None 
        for rank in xrange(1, MAX_RANK+1) 
        for suit in xrange(len(SUITS))
    }


class FreeCellState(object):
    def __init__(self, filename):
        """Return a new state from this csv file."""
#        The value at index n refers to SUITS[n]. The value
#        refers to the maximum rank on the foundation. If 0,
#        the foundation is empty.
        self._foundations = [0] * 4

        self._freecells = set() # Set of cards
        self._tableau = Tableau(filename)

    def is_goal(self):
        """Return whether or not we have won."""
        return self._foundations == [MAX_RANK] * 4

    def heuristic(self):
        """Return a heuristic."""
        return DECK_SIZE - sum(self._foundations)

    def _trivial_next_state(self):
        """Return a (state, move, cost) tuple for obvious moves. If there
        are no obvious moves, return None.
        """
        return None #todo

    def _tableau_to_foundations(self):
        """Return a list of (state, move, cost) tuples from the tableau to the
        foundations.
        """
        return [] #todo

    def _foundations_to_tableau(self):
        """Return a list of (state, move, cost) tuples from the foundations to
        the tableau.
        """
        return [] #todo

    def _tableau_moves(self):
        """Return a list of (state, move, cost) tuples from moving cards within
        the tableau.
        """
        return [] #todo

    def _tableau_to_free(self):
        """Return a list of (state, move, cost) tuples from moving cards from
        the tableau to the free cells.
        """
        return [] #todo

    def _free_to_tableau(self):
        """Return a list of (state, move, cost) tuples from moving cards from
        the free cells to the tableau.
        """
        return [] #todo

    def _free_to_foundations(self):
        """Return a list of (state, move, cost) tuples from moving cards from
        the free cells to the foundations.
        """
        return [] #todo

    def __hash__(self):
        return hash(
            frozenset(self._freecells), 
            tuple(self._foundations), 
            frozenset(self._tableau)
        )

    def __eq__(self, other):
        return self._foundations == other._foundations and \
            self._tableau == other._tableau and \
            self._freecells == other._freecells

    def next_states(self):
        """Return a list of (state, move, cost) tuples."""
        trivial_pair = self._trivial_next_state()
        if trivial_pair is not None:
            return [trivial_pair]

        rtn = []
        rtn += self._tableau_to_foundations()
        rtn += self._foundations_to_tableau()
        rtn += self._tableau_moves()
        rtn += self._tableau_to_free()
        rtn += self._free_to_tableau()
        rtn += self._free_to_foundations()

        return rtn

        
class FreeCellProblem(Problem):
    def __init__(self, filename):
        """Read in a FreeCell game."""
        self._init_state = FreeCellState(filename)

    def initial_state(self):
        return self._init_state

    def is_goal(self, state):
        return state.is_goal()

    def next_states(self, state):
        return state.next_states()

    def heuristic(self, state):
        return state.heuristic()

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
