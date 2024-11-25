from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

#TODO: Import any built in modules you want to use

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].



def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
   #check if the state is terminal
    terminal, values = game.is_terminal(state)
    if terminal: 
        return values[0], None   
    #check if the max depth is reached
    if max_depth==0: 
        return heuristic(game, state, 0), None   
      # get the turn of the player
      # if the turn is 0, it is a max node
    if game.get_turn(state)==0:
            value = float('-inf')
            optimal_action = None
            #loop on all actions
            for action in game.get_actions(state):
                #get the new state after applying the action
                new_state = game.get_successor(state, action)
                #get the value of the new state
                new_value, _ = minimax(game, new_state, heuristic, max_depth - 1)
                #check if the new value is greater than the current value 
                if new_value > value:
                    value, optimal_action = new_value, action
            #return the value and the optimal action
            return value, optimal_action 
    # if the turn is not 0, it is a min node
    else:
        value = float('inf')
        optimal_action = None
        #loop on all actions
        for action in game.get_actions(state):
            #get the new state after applying the action
            new_state = game.get_successor(state, action)
            #get the value of the new state
            new_value, _ = minimax(game, new_state, heuristic, max_depth - 1)
            #check if the new value is less than the current value    
            if new_value < value:
                value, optimal_action = new_value, action
        #return the value and the optimal action
        return value, optimal_action

# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    if game.get_turn(state)==0:
        # if the turn is 0, it is a max node
        return max_value(float('-inf'),float('inf'),game, state, heuristic, max_depth) 
    # if the turn is not 0, it is a min node
    return min_value(float('-inf'),float('inf'),game, state, heuristic, max_depth)


# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    if game.get_turn(state)==0:
        # if the turn is 0, it is a max node
        return max_value_with_order(float('-inf'),float('inf'),game, state, heuristic, max_depth) 
    # if the turn is not 0, it is a min node
    return min_value_with_order(float('-inf'),float('inf'),game, state, heuristic, max_depth)

# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #TODO: Complete this function
      # get the turn of the player

    #check if the state is terminal
    terminal, values = game.is_terminal(state)
    if terminal: 
        return values[0], None   
    #check if the max depth is reached
    if max_depth==0: 
        return heuristic(game, state, 0), None
    # if the turn is 0, it is a max node
    if game.get_turn(state)==0: 
        value = float('-inf')
        optimal_action = None
        #loop on all actions
        for action in game.get_actions(state):
            #get the new state after applying the action
            new_state = game.get_successor(state, action)
            #get the value of the new state
            new_value, _ = expectimax(game, new_state, heuristic, max_depth - 1)       
            #check if the new value is greater than the current value 
            if new_value > value:
                value, optimal_action = new_value, action
        #return the value and the optimal action
        return value, optimal_action
        # if the turn is not 0, it is a random node
    else:
        value = 0
        #loop on all actions
        for action in game.get_actions(state):
            #get the new state after applying the action
            new_state = game.get_successor(state, action)
            #check if the new state is a max or random node
            #get the value of the new state
            new_value, _ = expectimax(game, new_state, heuristic, max_depth - 1)
            #add the value of the new state to the total value
            value += new_value
        
        #return the value and the optimal action
        return value/len(game.get_actions(state)), _

    

def max_value(A,B,game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #check if the state is terminal
    terminal, values = game.is_terminal(state)
    if terminal: 
        return values[0], None   
    #check if the max depth is reached
    if max_depth==0: 
        return heuristic(game, state, 0), None 
    value = float('-inf')
    optimal_action = None
    #loop on all actions
    for action in game.get_actions(state):
        #get the new state after applying the action
        new_state = game.get_successor(state, action)
        #check if the new state is a max or min node
        #get the value of the new state
        if  game.get_turn(new_state)==0:
          new_value, _ = max_value(A,B,game, new_state, heuristic, max_depth - 1)
        else:
            new_value, _ = min_value(A,B,game, new_state, heuristic, max_depth - 1)       
        #check if the new value is greater than the current value 
        if new_value > value:
            value, optimal_action = new_value, action
        #check if the new value is greater than B
        if new_value >= B:
            return new_value, action
        #update the value of A
        A = max(A, new_value)
    #return the value and the optimal action
    return value, optimal_action


def min_value(A,B,game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #check if the state is terminal
    terminal, values = game.is_terminal(state)
    if terminal: 
        return values[0], None   
    #check if the max depth is reached 
    if max_depth==0: 
        return heuristic(game, state, 0), None
    value = float('inf')
    optimal_action = None
    #loop on all actions
    for action in game.get_actions(state):
        #get the new state after applying the action
        new_state = game.get_successor(state, action)
        #check if the new state is a max or min node
        #get the value of the new state
        if  game.get_turn(new_state)==0:
          new_value, _ = max_value(A,B,game, new_state, heuristic, max_depth - 1)
        else:
            new_value, _ = min_value(A,B,game, new_state, heuristic, max_depth - 1)
        #check if the new value is less than the current value    
        if new_value < value:
            value, optimal_action = new_value, action
        #check if the new value is less than A
        if new_value <= A:
            return new_value, action
        #update the value of B
        B = min(B, new_value)
    #return the value and the optimal action
    return value, optimal_action





def max_value_with_order(A,B,game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #check if the state is terminal
    terminal, values = game.is_terminal(state)
    if terminal: 
        return values[0], None   
    #check if the max depth is reached
    if max_depth==0: 
        return heuristic(game, state, 0), None 
    value = float('-inf')
    optimal_action = None
    # Order actions based on the heuristic to maximize pruning opportunities
    actions = sorted(game.get_actions(state), key=lambda a: heuristic(game, game.get_successor(state, a), game.get_turn(state)), reverse=True)

    #loop on all actions
    for action in actions:
        #get the new state after applying the action
        new_state = game.get_successor(state, action)
        #check if the new state is a max or min node
        #get the value of the new state
        if  game.get_turn(new_state)==0:
          new_value, _ = max_value_with_order(A,B,game, new_state, heuristic, max_depth - 1)
        else:
            new_value, _ = min_value_with_order(A,B,game, new_state, heuristic, max_depth - 1)       
        #check if the new value is greater than the current value 
        if new_value > value:
            value, optimal_action = new_value, action
        #check if the new value is greater than B
        if new_value >= B:
            return new_value, action
        #update the value of A
        A = max(A, new_value)
    #return the value and the optimal action
    return value, optimal_action


def min_value_with_order(A,B,game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #check if the state is terminal
    terminal, values = game.is_terminal(state)
    if terminal: 
        return values[0], None   
    #check if the max depth is reached 
    if max_depth==0: 
        return heuristic(game, state, 0), None
    value = float('inf')
    optimal_action = None
    # Order actions based on the heuristic to maximize pruning opportunities
    actions = sorted(game.get_actions(state), key=lambda a: heuristic(game, game.get_successor(state, a),  game.get_turn(state)), reverse=True)
    #loop on all actions
    for action in actions:
        #get the new state after applying the action
        new_state = game.get_successor(state, action)
        #check if the new state is a max or min node
        #get the value of the new state
        if  game.get_turn(new_state)==0:
          new_value, _ = max_value_with_order(A,B,game, new_state, heuristic, max_depth - 1)
        else:
            new_value, _ = min_value_with_order(A,B,game, new_state, heuristic, max_depth - 1)
        #check if the new value is less than the current value    
        if new_value < value:
            value, optimal_action = new_value, action
        #check if the new value is less than A
        if new_value <= A:
            return new_value, action
        #update the value of B
        B = min(B, new_value)
    #return the value and the optimal action
    return value, optimal_action

