"""
    Enter your details below:

    Name: Preshtibye Raggoo
    Student ID: u7522927
    Email: u7522927@anu.edu.au
"""

from typing import Callable, List

from game_engine.util import raise_not_defined
from search_problems import SearchProblem


def solve(problem: SearchProblem, heuristic: Callable) -> List[str]:
    """See 2_implementation_notes.md for more details.

    Your search algorithms needs to return a list of actions that reaches the
    goal from the start state in the given problem. The elements of this list
    need to be one or more references to the attributes NORTH, SOUTH, EAST and
    WEST of the class Directions.
    """
    import heuristics
    from frontiers import PriorityQueue
    frontier = PriorityQueue()
    visitednodes = set()
    actions = list()
    dic1 = dict()
    dic2 = dict()

    previous= dict()


    root = problem.get_initial_state()
    # g-value from root to root is 0.
    dic1[root] = 0
    val = dic1[root] + heuristic(root, problem)
    dic2[root] = val
    frontier.push(root, val)
    backtrackval = None


    while not frontier.is_empty():
        current = frontier.peek()

        # if it is a goal
        if problem.goal_test(current):
            backtrackval = current
            break

        current = frontier.pop()
        visitednodes.add(current)
        for successor, action, cost in problem.get_successors(current):
            if successor not in visitednodes:
                dic1[successor] = dic1[current] + cost
                val = dic1[successor] + heuristic(successor, problem)

                if successor not in dic2.keys():
                    previous[successor] = (current, action)
                    frontier.push(successor, val)
                    dic2[successor] = val
                elif dic2[successor] > val:
                    frontier.change_priority(successor, val)
                    dic2[successor] = val
                    previous[successor] = (current, action)
    while backtrackval is not root:
        actions.append(previous[backtrackval][1])
        #print(actions)
        backtrackval = previous[backtrackval][0]
        #print(list(reversed(actions)))
    return list(reversed(actions))

