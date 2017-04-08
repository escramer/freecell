#! /usr/bin/env python

"""A Freecell problem"""

from copy import deepcopy, copy
import csv
import argparse
from itertools import permutations

from search import Problem, astar

SUITS = ('H', 'D', 'C', 'S')
MAX_RANK = 13
DECK_SIZE = 52
NUM_PILES = 8
NUM_FREECELLS = 4


class Tableau(object):
    def __init__(self, filename):
        """Initialize the tableau from this csv."""
        self._tableau = {}
        with open(filename) as file_obj:
            for row in csv.reader(file_obj):
                pile = []
                for card_str in row:
                    pile.append(Card.get(card_str))
                self._tableau[pile[-1]] = tuple(pile)

    def __deepcopy__(self, _):
        rtn = copy(self)
        rtn._tableau = dict(rtn._tableau)
        return rtn

    def internal_moves(self):
        """Return a list of (tableau, move) pairs of moves within the tableau.
        """
        rtn = []

        # Put cards in a new pile
        if len(self._tableau) < NUM_PILES:
            for card, pile in self._tableau.iteritems():
                if len(pile) > 1:
                    tableau = deepcopy(self)
                    tableau._remove(card)
                    tableau._put_in_new_pile(card)
                    rtn.append((tableau, 'Put %s in a new pile.' % card))

        # Put cards on top of other cards
        for on_top, on_bottom in permutations(self._tableau, 2):
            if on_top.goes_on_top_of(on_bottom):
                tableau = deepcopy(self)
                tableau._remove(on_top)
                tableau._put_on_pile(on_bottom, on_top)
                rtn.append(
                    (tableau, 'Put %s on top of %s.' % (on_top, on_bottom))
                )

        return rtn

    def _put_in_new_pile(self, card):
        """Put the card (Card, string, or tuple) in a new pile."""
        card = Card.get(card)
        assert card not in self._tableau
        assert len(self._tableau) < NUM_PILES
        self._tableau[card] = card,

    def _moves_in_new_pile(self, card):
        """Return a list of (Tableau, move) pairs (a list of length 0 or 1) 
        resulting in placing this card (Card, string, or tuple) in a new pile.
        """
        card = Card.get(card)
        assert card not in self._tableau
        if len(self._tableau) == NUM_PILES:
            return []
        tableau = deepcopy(self)
        tableau._put_in_new_pile(card)
        return [(tableau, 'Put %s in a new pile.' % card)]

    def _put_on_pile(self, old_top_card, new_top_card):
        """Put the new_top_card on top of the old_top_card. Both cards can
        be Cards, strings, or tuples.
        """
        old_top_card = Card.get(old_top_card)
        new_top_card = Card.get(new_top_card)
        assert old_top_card in self._tableau
        assert new_top_card.goes_on_top_of(old_top_card)
        assert new_top_card not in self._tableau
        self._tableau[new_top_card] = self._tableau[old_top_card] + new_top_card,
        del self._tableau[old_top_card]

    def _moves_on_a_pile(self, card):
        """Return a list of (Tableau, move) pairs resulting in placing this
        card (Card, string, or tuple) on a pile.
        """
        rtn = []
        for top_card in self._tableau:
            if card.goes_on_top_of(top_card):
                tableau = deepcopy(self)
                tableau._put_on_pile(top_card, card)
                rtn.append((tableau, 'Put %s on top of %s.' % (card, top_card)))

        return rtn

    def place(self, card):
        """Return (tableau, move) pairs resulting from placing this card
        in the tableau. card can be a string, tuple, or Card.
        """
        return self._moves_on_a_pile(card) + self._moves_in_new_pile(card)

    def top_cards(self):
        """Return the set of cards that are on the top of each pile."""
        return set(self._tableau)

    def _remove(self, card):
        """Remove the card (Card, (rank, suit) tuple, or string from this
        tableau.
        """
        card = Card.get(card)
        new_pile = self._tableau[card][:-1]
        del self._tableau[card]
        if new_pile:
            self._tableau[new_pile[-1]] = new_pile

    def remove(self, card):
        """Return a new Tableau with this card removed. The card should be from
        the top of a pile. card may be a Card, (rank, suit) tuple, or
        string.
        """
        new_tableau = deepcopy(self)
        new_tableau._remove(card)
        return new_tableau

    def _place_on_top(self, new_top_card, old_top_card):
        """Place new_top_card on top of old_top_card. The cards can be
        Cards, tuples, or strings.
        """
        new_top_card = Card.get(new_top_card)
        old_top_card = Card.get(old_top_card)
        pile = self._tableau[old_top_card] + (new_top_card,)
        self._tableau[new_top_card] = pile
        del self._tableau[old_top_card]

    def _put_in_new_pile(self, card):
        """Place this card (Card, string, or tuple) in a new pile."""
        assert not self.is_full()
        card = Card.get(card)
        assert card not in self._tableau
        self._tableau[card] = (card,)
        

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
    def get(cls, info):
        """Return a Card where info describes the card.

        info can be a Card (it'll just be returned), (rank, suit)
        tuple, or a 2-character card string.
        """
        if isinstance(info, Card):
            return info
        if isinstance(info, tuple):
            return cls._from_ranksuit(*info)
        if isinstance(info, str):
            return cls._from_str(info)
        raise Exception('What card is this?: %s' % info)

    
    @classmethod
    def _from_ranksuit(cls, rank, suit):
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
    def _from_str(cls, card_str):
        """Return a Card from the 2-character card string.

        Letters are allowed to be upper or lower case.
        """
        return cls._from_ranksuit(*cls._card_map.str_to_int(card_str))

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

    def goes_on_top_of(self, other):
        """Return whether this card can go on top of other (Card, string, or
        tuple.
        """
        other = Card.get(other)
        return self._rank == other._rank - 1 and self._is_red != other._is_red

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
        rtn = []
        for card in self._tableau.top_cards():
            if card.rank == self._foundations[card.suit] + 1:
                new_tableau = self._tableau.remove(card)
                new_state = deepcopy(self)
                new_state._foundations[card.suit] += 1
                new_state._tableau = new_tableau
                rtn.append((new_state, 'Move %s to its foundation.' % card, 1))

        return rtn

    def _foundations_to_tableau(self):
        """Return a list of (state, move, cost) tuples from the foundations to
        the tableau.
        """
        rtn = []
        for suit, rank in enumerate(self._foundations):
            if rank != 0:
                for tableau, move in self._tableau.place((rank, suit)):
                    new_state = deepcopy(self)
                    new_state._tableau = tableau
                    new_state._foundations[suit] -= 1
                    rtn.append((new_state, move, 1))

        return rtn                

    def _tableau_moves(self):
        """Return a list of (state, move, cost) tuples from moving cards within
        the tableau.
        """
        rtn = []
        for tableau, move in self._tableau.internal_moves():
            new_state = deepcopy(self)
            new_state._tableau = tableau
            rtn.append((new_state, move, 1))
        return rtn

    def _tableau_to_free(self):
        """Return a list of (state, move, cost) tuples from moving cards from
        the tableau to the free cells.
        """
        if len(self._freecells) == NUM_FREECELLS:
            return []

        rtn = []

        for card in self._tableau.top_cards():
            new_tableau = self._tableau.remove(card)
            new_state = deepcopy(self)
            new_state._tableau = new_tableau
            new_state._freecells.add(card)
            rtn.append((new_state, 'Put %s in a free cell.' % card, 1))

        return rtn

    def _free_to_tableau(self):
        """Return a list of (state, move, cost) tuples from moving cards from
        the free cells to the tableau.
        """
        rtn = []
        for card in self._freecells:
            for tableau, move in self._tableau.place(card):
                state = deepcopy(self)
                state._tableau = tableau
                state._freecells.remove(card)
                rtn.append((state, move, 1))

        return rtn

    def _free_to_foundations(self):
        """Return a list of (state, move, cost) tuples from moving cards from
        the free cells to the foundations.
        """
        rtn = []
        for card in self._freecells:
            if card.rank == self._foundations[card.suit] + 1:
                state = deepcopy(self)
                state._foundations[card.suit] = card.rank
                state._freecells.remove(card)
                rtn.append((state, 'Put %s in its foundation.' % card, 1))

        return rtn

    def _foundations_to_free(self):
        """Return a list of (state, move, cost) tuples from moving cards from
        the foundations to the free cells.
        """
        return [] #todo

    def __hash__(self):
        return hash(
            frozenset(self._freecells), 
            tuple(self._foundations), 
            frozenset(self._tableau.values())
        )

    def __eq__(self, other):
        return self._foundations == other._foundations and \
            self._tableau == other._tableau and \
            self._freecells == other._freecells

    def __deepcopy__(self, _):
        rtn = copy(self)
        rtn._foundations = self._foundations[:]
        rtn._freecells = self._freecells.copy()
        return rtn

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
        rtn += self._foundations_to_free()

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
