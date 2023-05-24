"""
    Enter your details below:

    Name: Preshtibye Raggoo
    Student ID: u7522927
    Email: u7522927@anu.edu.au
"""

#rferences:https://www.geeksforgeeks.org/iterative-deepening-searchids-iterative-deepening-depth-first-searchiddfs/
#          https://www.algorithms-and-technologies.com/iterative_deepening_dfs/python
#It expands way too many nodes but does work for ANUsearch

from typing import List

from game_engine.util import raise_not_defined
from search_problems import SearchProblem

from search_strategies import SearchNode
from frontiers import Stack

class Node(SearchNode): #This class handles the definition of a node so that I do not have to reuse code everytie
    def __init__(self,state,action=None,path_cost=0,parent=None,depth=0,visited=None):
        super().__init__(state,action,path_cost,parent,depth)
        self.visited = visited


def solve(problem: SearchProblem) -> List[str]:
    max_depth = 1000 #I am giving maxdepth a large value so that the algorithm doesn't terminate without handling more depths of the graph
    solution = search(problem,max_depth)
    solution.IDS()
    return solution.path()



class search():
    def __init__(self,problem,depth):
        self.problem = problem
        self.stack = None
        self.max_depth   = depth

    def IDS(self):
        for d in range(1, self.max_depth):
            r = self.DLS(d)
            if r == "cutoff":
                continue
            if r == "goal": #Once we have found the goal we can return
                return
        raise ValueError #This means that the search algo has failed

    def path(self):
        actions = []
        retlist = []
        while not self.stack.is_empty():
            actions.append((self.stack.pop()).action)
            retlist = actions[::-1]
        return retlist

    def recursive_DLS(self,limit,node):
        self.visited.add(node.state)
        if self.problem.goal_test(node.state): return "goal"
        if node.depth == limit: return "cutoff"

        for successor,action,cost in self.problem.get_successors(node.state):
            # wall check needed to prevent unnecessary computation
            if self.problem.get_walls()[successor[0]][successor[1]] or successor in self.visited:
                continue
            self.visited.add(successor)
            successor = Node(state=successor,action=action,parent=node.state,depth=node.depth+1)
            self.stack.push(successor)
            r = self.recursive_DLS(limit=limit,node=successor) #recursive call to handle next successor
            if r == "cutoff":
                garbage = self.stack.pop()
                continue
            if r == "goal":
                return r
        return "cutoff"
    def DLS(self,depth):
        self.stack = Stack()
        self.visited = set()
        return self.recursive_DLS(depth,Node(state=self.problem.get_initial_state()))


