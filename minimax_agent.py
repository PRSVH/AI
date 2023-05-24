# minimax_agent.py
# --------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course

"""
    Enter your details below:

    Name: Preshtibye Raggoo
    Student ID: u7522927
    Email: u7522927@anu.edu.au
"""

from typing import Tuple

from agents import Agent
from game_engine.actions import Directions
from search_problems import AdversarialSearchProblem

Position = Tuple[int, int]
Positions = Tuple[Position]
State = Tuple[int, Position, Position, Positions, float, float]


class MinimaxAgent(Agent):
    """ The agent you will implement to compete with the black bird to try and
        save as many yellow birds as possible. """

    def __init__(self, max_player, depth="2"):
        """ Make a new Adversarial agent with the optional depth argument.
        """
        self.max_player = max_player
        self.depth = int(depth)

    def evaluation(self, problem: AdversarialSearchProblem, state: State) -> float:
        """
            (MinimaxAgent, AdversarialSearchProblem,
                (int, (int, int), (int, int), ((int, int)), number, number))
                    -> number
        """
        player, red_pos, black_pos, yellow_birds, score, yb_score = state #Here we use the state passed as the parameeter to assign values to player,red_pos,black_pos,yellow_birds, score and yb_score
        increase = 0
        for bird in yellow_birds:
            red =  problem.distance[bird,red_pos] #we need to find the distance between the position of the red agent and every yellow bird in the list
            if red <=problem.distance[bird,black_pos]: #if the above calculated distance is less than the distance between that yellow bird and the vlack agent, it is favoured
                increase += yb_score / (red+0.001)
                #This part tentativzly tells our agent to handle close targets first but to ignore targets that are too hard to reach. Hence the chance value
        chance = 1 / (0.001+problem.distance[red_pos,black_pos])
        rem = len(yellow_birds) #The more birds are left uneaten, the less is our agent's score as seen in the below equations
        if (chance>=0.01):
            score = 0.2*increase + 0.5*score - 10*rem + chance
        else:
            score = 0.2*increase + 5*score - 10*rem + chance
        return score

    def maximize(self, problem: AdversarialSearchProblem, state: State,
                 current_depth: int, alpha=float('-inf'), beta=float('inf')) -> Tuple[float, str]:
        """ This method should return a pair (max_utility, max_action).
            The alpha and beta parameters can be ignored if you are
            implementing minimax without alpha-beta pruning.
        """
        #alpha is the value of the best choice for maxval so far
        #beta is the value of the best choice for minval so far
        if current_depth == self.depth: return self.evaluation(problem,state), Directions.STOP #This is a stopping condition. When we reach the maximum depth we stop.
        if problem.terminal_test(state): return problem.utility(state),Directions.STOP #This is a stopping condition. When we reach a goal state we stop
        actions=dict()
        val = float('-inf')
        for next,action,_ in problem.get_successors(state):
            val = max(val,self.minimize(problem,next,current_depth+1))
            actions[action]=val
            if val >= beta:
                return val,action #The child's siblings is pruned and val is returned
            alpha = max(alpha,val)
        maxval=max(actions,key=actions.get)
        return actions[maxval],maxval




    def minimize(self, problem: AdversarialSearchProblem, state: State,
                 current_depth: int, alpha=float('-inf'), beta=float('inf')) -> float:
        """ This function should just return the minimum utility.
            The alpha and beta parameters can be ignored if you are
            implementing minimax without alpha-beta pruning.
        """
        if current_depth == self.depth: return self.evaluation(problem,state)
        if problem.terminal_test(state): return problem.utility(state)
        val = float('inf')
        for next,action,_ in problem.get_successors(state):
            val = min(val,self.maximize(problem,next,current_depth+1)[0])
            if val<= alpha:
                return val
            beta = min(beta,val)
        return val



    def get_action(self, game_state):
        """ This method is called by the system to solicit an action from
            MinimaxAgent. It is passed in a State object.

            Like with all of the other search problems, we have abstracted
            away the details of the game state by producing a SearchProblem.
            You will use the states of this AdversarialSearchProblem to
            implement your minimax procedure. The details you need to know
            are explained at the top of this file.
        """
        # We tell the search problem what the current state is and which player
        # is the maximizing player (i.e. who's turn it is now).
        problem = AdversarialSearchProblem(game_state, self.max_player)
        state = problem.get_initial_state()
        utility, max_action = self.maximize(problem, state, 0)
        print("At Root: Utility:", utility, "Action:",
              max_action, "Expanded:", problem._expanded)
        return max_action
