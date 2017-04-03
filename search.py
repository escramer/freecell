"""Module for search algorithms"""

from Queue import PriorityQueue

class _Node:
    """Represents a node in the search problem."""

    def __init__(
        self, state, problem, parent_node=None, move=None, cost=1
    ):
        """Initialize a new node.

        The parent node is the node that generates this state.
        Use None if this is the root node.
        move is the move that is done to go from the parent_node
        to this node (this is only to be displayed).
        """
        self._state = state
        self._parent = parent_node
        self._move = move
        self._problem = problem
        if parent_node is None:
            self._step_cost = 0
        else:
            self._step_cost = parent_node._step_cost + cost

    def get_state(self):
        return self._state

    def get_parent(self):
        return self._parent

    def get_move(self):
        return self._move

    def get_cost(self):
        """Return the total cost (step + heuristic)."""
        return self._step_cost + self._problem.heuristic(self._state)


class Problem:
    """Represents a problem.

    A subclass must have states that are hashable.
    """

    def initial_state(self):
        """Return the initial state."""
        raise NotImplementedError

    def is_goal(self, state):
        """Return whether or not this is a goal state."""
        raise NotImplementedError

    def next_states(self, state):
        """Return a list of (state, move, cost) pairs that can be expanded from 
        this state. Cost should be an integer. A move could be a descriptive
        string.
        """
        raise NotImplementedError

    def heuristic(self, state):
        """Return a heuristic. A subclass may override this to use with A
        star.
        """
        return 0


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
        self._queue.put((node.get_cost(), node))

    def pop(self):
        return self._queue.get(False)[1]

    def is_empty(self):
        return self._queue.empty()


def _move_seq(node):
    """Return the list of moves to get to this _Node."""
    rtn = []
    while node.get_parent() is not None:
        rtn.append(node.get_move())
        node = node.get_parent()
    return list(reversed(rtn))


def _search(problem, fringe_cls):
    """Return a sequence of moves that goes towards the solution.
    If no solution exists, return None.
    """
    closed = set()
    fringe = fringe_cls()
    fringe.push(_Node(problem.initial_state(), problem))

    while True:
        if fringe.is_empty():
            return None

        node = fringe.pop()
        state = node.get_state()
        if problem.is_goal(state):
            return _move_seq(node)

        if state not in closed:
            closed.add(state)
            for next_state, move, cost in problem.next_states(state):
                fringe.push(_Node(
                    next_state, problem, parent_node=node, move=move, cost=cost
                ))


def astar(problem):
    """Return a sequence of moves that goes towards the solution.
    If no solution exists, return None.
    """
    return _search(problem, _PriorityQueue)
            
