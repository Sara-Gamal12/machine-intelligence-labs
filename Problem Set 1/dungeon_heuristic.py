from dungeon import DungeonProblem, DungeonState,DungeonLayout
from mathutils import Direction, Point, euclidean_distance, manhattan_distance
from helpers import utils

# This heuristic returns the distance between the player and the exit as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: DungeonProblem, state: DungeonState):
    return euclidean_distance(state.player, problem.layout.exit)





from collections import deque
#get distance from start to each point in layout
def bfs_distance(start: Point, layout: DungeonLayout) -> float:
    distances = {}  # Dictionary to hold the shortest distance to each point
    queue = deque([start])  # Initialize the queue with the starting point
    distances[start] = 0  # Distance from the start point to itself is 0
    while queue:
        current = queue.popleft()  # Dequeue the next point to process
        current_distance = distances[current]  # Get the distance to the current point

        # Check all possible directions from the current point
        for direction in Direction:
            neighbor = current + direction.to_vector()  # Calculate the neighboring point
            if neighbor in layout.walkable and neighbor not in distances:  # Check if walkable and unvisited
                distances[neighbor] = current_distance + 1  # Update distance
                queue.append(neighbor)  # Enqueue the neighbor for further processing

    # Return the distances
    return distances

#TODO: Import any modules and write any functions you want to use
def strong_heuristic(problem: DungeonProblem, state: DungeonState) -> float:
    cache = problem.cache()
    # Cache key using player state and remaining_coins 
    state_key = (state.player, frozenset(state.remaining_coins))
    # Check if the heuristic for this state has already been computed
    if state_key in cache:
        return cache[state_key]

    # Get cached distances or compute them if not available
    distance_from_player = cache.get(state.player) or bfs_distance(state.player, state.layout)
    cache[state.player] = distance_from_player  # Cache the distance from the player

    distance_from_exit = cache.get(state.layout.exit) or bfs_distance(state.layout.exit, state.layout)
    cache[state.layout.exit] = distance_from_exit  # Cache the distance from the exit
    # If no coins are remaining, return the distance from player to exit
    if not state.remaining_coins:
        return distance_from_player.get(state.layout.exit, float('inf'))
    
    coinplayer = 0  # Total distance to collect all coins
    coinexit = 0  # Total distance from each coin to the exit
    coinplayer1 = 0  # Maximum distance from player to any coin
    coinexit1 = float('inf')  # Minimum distance from any coin to the exit

    # Loop through each remaining coin to calculate distances
    for coin in state.remaining_coins:
        distance_to_exit_coin = distance_from_player.get(coin, 0)  # Distance from player to coin
        distance_from_exit_coin = distance_from_exit.get(coin, float('inf'))  # Distance from exit to coin
        coinplayer += distance_to_exit_coin  # Accumulate distances from player to coins
        coinplayer1 = max(distance_to_exit_coin, coinplayer1)  # Track the maximum distance to a coin
        coinexit += distance_from_exit_coin  # Accumulate distances from coins to exit
        coinexit1 = min(distance_from_exit_coin, coinexit1)  # Track the minimum distance to exit

    # Calculate two potential heuristic values
    heuristic_value1 = int((coinplayer + coinexit) / len(state.remaining_coins))  # Average heuristic
    heuristic_value2 = coinplayer1 + coinexit1  # Combined max distance heuristic
    heuristic_value = max(heuristic_value1, heuristic_value2)  # Choose the stronger heuristic

    # Cache the computed heuristic value
    cache[state_key] = heuristic_value1  
    return heuristic_value1  # Return the calculated heuristic value

