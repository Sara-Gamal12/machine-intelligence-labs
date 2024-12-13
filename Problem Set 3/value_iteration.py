from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json
from helpers.utils import NotImplemented

# This is a class for a generic Value Iteration agent
class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training 
    utilities: Dict[S, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        self.utilities = {state:0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor
    
    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        #TODO: Complete this function
        #if the state is terminal, return 0
        if self.mdp.is_terminal(state):
            return 0
        
        max_utility = float('-inf')
        # as the the reward is a function of current state, action and next state , we need to use the following variant of bellman equation
        for action in self.mdp.get_actions(state):
            untiity = 0
            # U(s) = max( sum( P(s'|s,a) * (R(s,a,s') + gamma * U(s')) for s' in S ) for a in A )
            for next_state, probability in self.mdp.get_successor(state, action).items():
                untiity += probability*(self.mdp.get_reward(state,action,next_state)+ self.discount_factor * self.utilities[next_state]    )
            #update the max utility
            if untiity > max_utility:
                max_utility = untiity
        return max_utility
    # Applies a single utility update
    # then returns True if the utilities has converged (the maximum utility change is less or equal the tolerance)
    # and False otherwise
    def update(self, tolerance: float = 0) -> bool:
        #TODO: Complete this function
        max_change = 0  
        updated_utilities = {}
        #loop through all the states
        for state in self.mdp.get_states():
            #compute the utility of the state
            updated_utilities[state] = self.compute_bellman(state)
            #update the max change
            if abs(self.utilities[state] - updated_utilities[state]) > max_change:
                max_change = abs(self.utilities[state] - updated_utilities[state])


          # update the utilities
        for state in self.mdp.get_states():
            self.utilities[state] = updated_utilities[state]

        

        return max_change < tolerance

    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: Optional[int] = None, tolerance: float = 0) -> int:
        #TODO: Complete this function to apply value iteration for the given number of iterations
        #loop through the number of iterations
        i=0
        while i < iterations:
            i+=1
            #update the utilities
            if self.update(tolerance):
                return i
        return i
            
    
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        #TODO: Complete this function
        #if the state is terminal, return None
        if self.mdp.is_terminal(state):
            return None
        max_utility = float('-inf')
        best_action = None
        # as the the reward is a function of current state, action and next state , we need to use the following variant of bellman equation
        for action in self.mdp.get_actions(state):
            untiity = 0
            # U(s) = max( sum( P(s'|s,a) * (R(s,a,s') + gamma * U(s')) for s' in S ) for a in A )
            for next_state, probability in self.mdp.get_successor(state, action).items():
                untiity += probability*(self.mdp.get_reward(state,action,next_state)+ self.discount_factor * self.utilities[next_state]    )
            #update the max utility and best action
            if untiity > max_utility:
                max_utility = untiity
                best_action = action
        return best_action
    
    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(state): value for state, value in self.utilities.items()}
            json.dump(utilities, f, indent=2, sort_keys=True)
    
    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            utilities = json.load(f)
            self.utilities = {self.mdp.parse_state(state): value for state, value in utilities.items()}
