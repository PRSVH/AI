"""
    Enter your details below:

    Name: Preshtibye Raggoo
    Student ID: u7522927
    Email: u7522927@anu.edu.au
"""

from frontiers import Queue

from typing import List

from game_engine.util import raise_not_defined
from search_problems import SearchProblem


def solve(problem: SearchProblem) -> List[str]:
    from frontiers import Queue
    queue = Queue()  #I am defining my frontier as a queue
    visited_nodes = set()  # keeps track to visited nodes
    parentchild = dict()
    actions= []
    rootnode = problem.get_initial_state()
    parentchild[rootnode] = (None, None)
    queue.push(rootnode)
    while not queue.is_empty():
        nextnode = queue.pop() #This expands the shallowest nodes of the tree
        # if it is the goal, end
        if problem.goal_test(nextnode):
            while True:
                path = parentchild[nextnode]
                if None not in path:
                    nextnode = path[0]
                    action = path[1]
                    #print(action)
                    actions.append(action)
                else:
                    break
            #print(list(reversed(actions)))
            return list(reversed(actions))

        # if not the goal, expands all its children
        for successor, action, cost in problem.get_successors(nextnode):
            if successor in visited_nodes:
                continue
            if successor not in queue.contents:
                parentchild[successor] = (nextnode, action)
                queue.push(successor)
                #print(queue)

        visited_nodes.add(nextnode)



    """See 2_implementation_notes.md for more details.

    Your search algorithms needs to return a list of actions that reaches the
    goal from the start state in the given problem. The elements of this list
    need to be one or more references to the attributes NORTH, SOUTH, EAST and
    WEST of the class Directions.
    """
