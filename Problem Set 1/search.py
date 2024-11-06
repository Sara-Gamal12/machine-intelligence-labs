from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers import utils


# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state

import heapq
# from dungeon import DungeonProblem,DungeonState
# from dungeon_heuristic import strong_heuristic
#priority queue for uniform search ,A* search and greedy search
class PriorityQueue(object):

    def __init__(self):
        self.queue = []
        self.counter=0

    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0
 
    # for inserting an element in the queue
    def insert(self, data):
        heapq.heappush(self.queue, (data[1], self.counter, data[0]))
        self.counter+=1
 
    # for popping an element based on Priority
    def delete(self):
        return heapq.heappop(self.queue)
    
    #check if node is inside queue with higher cost replace with lower cost
    def replaceCost(self,data,cost,oldcost=None):
         # Constants to represent return values
        NODE_NOT_FOUND = 0
        COST_UPDATED = 1
        COST_NOT_UPDATED = 2
        ind=-1
        if oldcost==None:
            for i in range (len(self.queue)):
                if data==self.queue[i][2]:
                    ind=i
                    break
        else:
            low, high = 0, len(self.queue) - 1
            while low <= high:
                mid = (low + high) // 2
                if self.queue[mid][0] == oldcost and self.queue[mid][2] == data:
                    ind = mid
                    break
                elif self.queue[mid][0] < oldcost:
                    low = mid + 1
                else:
                    high = mid - 1

        #node not found
        if ind==-1:
            return NODE_NOT_FOUND
        else:
            # Node found, check its cost
            if cost<self.queue[ind][0]:
                self.queue[ind]=(cost,self.queue[ind][1],data)
                # node found with higher cost so path should be changed
                return COST_UPDATED
            # node found with lower cost so path shouldn't be changed
            return COST_NOT_UPDATED

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    frontier:list=[initial_state]
    # Dictionary to keep track of the path to each state
    path:dict[S,list]={initial_state:[]}
    # List to keep track of explored nodes
    explored:set=set()
    while len(frontier)>0:
        # Remove the first node from the frontier
        node=frontier.pop(0)
        # Check if the current node is the goal state
        if problem.is_goal(node):
            return path[node]
         # Mark the current node as explored
        explored.add(node)
        actions=problem.get_actions(node)
         # Explore each action to find its resulting child state
        for action in actions:
            child=problem.get_successor(node,action)
            # Check if the child state has not been explored and is not in the frontier
            if child not in explored and child not in frontier:
                # Update the path to the child state and add child state to the forinter
                path[child] = path[node] + [action]
                frontier.append(child)
    return None

def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
   
    frontier:list=[initial_state]
    # Dictionary to keep track of the path to each state
    path:dict[S,list]={initial_state:[]}
     # List to keep track of explored nodes
    explored:set=set()
    while len(frontier)>0:
        # Remove the last node from the frontier
        node=frontier.pop()
        # Check if the current node is the goal state
        if problem.is_goal(node):
            return path[node]
         # Mark the current node as explored
        explored.add(node)
         # Explore each action to find its resulting child state
        actions=problem.get_actions(node)
        for action in actions:
            child=problem.get_successor(node,action)
             # Check if the child state has not been explored and is not in the frontier
            if child not in explored and child not in frontier:
                # Update the path to the child state and add child state to the forinter
                path[child] = path[node] + [action]
                frontier.append(child)
    return None  
  
def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    # Initialize the frontier as a priority queue to explore nodes based on their cost
    frontier:PriorityQueue=PriorityQueue()
    frontier.insert((initial_state,0))
    # Dictionary to keep track of the path to each state
    path:dict[S,list]={initial_state:[]}
     # List to keep track of explored nodes
    explored:set=set()
    while not frontier.isEmpty():
        # Remove the first node from the frontier
        (parent_cost,_,node)=frontier.delete()
         # Check if the current node is the goal state
        if problem.is_goal(node):
            return path[node]
         # Mark the current node as explored
        explored.add(node)
        # Explore each action to find its resulting child state
        actions=problem.get_actions(node)
        for action in actions:
            child=problem.get_successor(node,action)
            # Only proceed if the child state has not been explored
            if child not in explored :
                cost=problem.get_cost(node,action)+parent_cost
                #Check if the child state is already in the frontier with a higher cost and update cost if it is higher
                checked=frontier.replaceCost(child,cost)
                # If the child is not in the frontier, add it with the new cost
                if  checked==0:
                    path[child] = path[node] + [action]
                    frontier.insert((child,cost))
                 # If the child is found in the frontier with a higher cost, update the path
                elif checked==1:
                     path[child] = path[node] + [action]
    return None

def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    # Initialize the frontier as a priority queue to explore nodes based on their f(g + h)
    frontier:PriorityQueue=PriorityQueue()
     # Insert the initial state with its heuristic cost
    frontier.insert((initial_state,heuristic(problem,initial_state)))
    #set for frontier for faster search
    frontier_set=set()
    frontier_set.add(initial_state)
    # Dictionary to keep track of the path to each state
    path:dict[S,list]={initial_state:[]}
    # Dictionary to track the cost to reach each state (g cost)
    costs:dict={initial_state:0}
    # Dictionary to track the f to reach each state 
    f_cost:dict={initial_state:heuristic(problem,initial_state)}
    # List to keep track of explored nodes
    explored:set=set()
    while not frontier.isEmpty():
         # Remove the node with the lowest (f = g + h) from the frontier
        (_,_,node)=frontier.delete()
        #Check if the current node is the goal state
        if problem.is_goal(node):
            return path[node]
        # Mark the current node as explored
        explored.add(node)
        actions=problem.get_actions(node)
        # Explore each action to find its resulting child state
        for action in actions:
            child=problem.get_successor(node,action)
              # Only proceed if the child state has not been explored
            if child not in explored :
                 #Calculate the f for the child (f = g + h)
                f=heuristic(problem,child)+costs[node]+problem.get_cost(node,child)
                # Check if the child is already in the frontier
                # If the child is not in the frontier, add it with the new cost ,update its path and cost.
                if  child not in frontier_set:
                    path[child] = path[node] + [action]
                    costs[child]=costs[node]+problem.get_cost(node,child)
                    frontier.insert((child,f))
                    f_cost[child]=f
                    frontier_set.add(child)
                 # If the child is found in the frontier 
                else:
                     #check if it has a higher cost, update the path and cost
                     if f_cost[child]>f:
                        f_cost[child]=f
                        frontier.replaceCost(child,f,f_cost[child])
                        path[child] = path[node] + [action]
                        costs[child]=costs[node]+problem.get_cost(node,child)
    return None

def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    # Initialize the frontier as a priority queue to explore nodes based on their heuristic cost
    frontier:PriorityQueue=PriorityQueue()
    frontier.insert((initial_state,heuristic(problem,initial_state)))
    # Dictionary to keep track of the path to each state
    path:dict[S,list]={initial_state:[]}
    # List to keep track of explored nodes
    explored:set=set()
    while not frontier.isEmpty():
        # Remove the node with the lowest heuristic cost from the frontier
        (_,_,node)=frontier.delete()
         # Check if the current node is the goal state
        if problem.is_goal(node):
            return path[node]
         # Mark the current node as explored
        explored.add(node)
        actions=problem.get_actions(node)
        # Explore each action to find its resulting child state
        for action in actions:
            child=problem.get_successor(node,action)
             # Only proceed if the child state has not been explored
            if child not in explored :
                 # Calculate the heuristic cost for the child state
                h=heuristic(problem,child)
                # Check if the child is already in the frontier with a higher cost
                checked=frontier.replaceCost(child,h)
                # If the child is not in the frontier, add it with the heuristic cost
                if  checked==0:
                    path[child] = path[node] + [action]
                    frontier.insert((child,h))
                     # If the child is found in the frontier, update the path to the child
                elif checked==1:
                     path[child] = path[node] + [action]
    return None

