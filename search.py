"""Module for search algorithms"""

from Queue import PriorityQueue

class _Node:
    """Represents a node in the search problem."""

    def __init__(self, state, parent_node=None, move=None):
        """Initialize a new node.

        The parent node is the node that generates this state.
        Use None if this is the root node.
        """
        self._state = state
        self._parent = parent_node
        self._move = move

    def get_state(self):
        return self._state

    def get_parent(self):
        return self._parent

    def get_move(self):
        return self._move


class Problem:
    """Represents a problem."""

    def initial_state(self):
        """Return the initial state."""
        raise NotImplementedError

    def is_goal(self, state):
        """Return whether or not this is a goal state."""
        raise NotImplementedError

    def next_states(self, state):
        """Return a list of (state, move) pairs that can be expanded from this
        state.
        """
        raise NotImplementedError


class _Fringe:
    """Represents a fringe."""

    def __init__(self):
        """Return a new fringe."""
        raise NotImplementedError

    def push(self, node):
        """Push a node onto this fringe."""
        raise NotImplementedError

    def pop(self):
        """Remove and return a node from this fringe. If there is nothing
        to remove, raise an Exception.
        """
        raise NotImplementedError

    def is_empty(self):
        """Return whether or not this fringe is empty."""
        raise NotImplementedError


class _PriorityQueue(_Fringe):
    """A priority queue for a-star."""

    def __init__(self):
        self._queue = PriorityQueue()

    def push(self, node):
        self._queue.put((node.get_state().get_cost(), node))

    def pop(self):
        return self._queue.get(False)[1]

    def is_empty(self):
        return self._queue.empty()


def _search(problem, fringe_cls):
    """Return a sequence of moves that goes towards the solution.
    If no solution exists, return None.
        
