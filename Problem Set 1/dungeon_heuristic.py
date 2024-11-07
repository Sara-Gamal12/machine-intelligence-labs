from dungeon import DungeonProblem, DungeonState,DungeonLayout
from mathutils import Direction, Point, euclidean_distance, manhattan_distance
from helpers import utils
from collections import deque
from itertools import combinations



# This heuristic returns the distance between the player and the exit as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: DungeonProblem, state: DungeonState):
    return euclidean_distance(state.player, problem.layout.exit)




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

# Minimum Spanning Tree function for calculating cost of visiting remaining coins
def mst_cost(points: list, distances: dict) -> float:
    if len(points) <= 1:
        return 0

    # Map each point to an index for easy reference
    point_indices = {point: i for i, point in enumerate(points)}

    # Build a graph of distances between each pair of points using indices
    edges = [
        (distances[p1][p2], point_indices[p1], point_indices[p2])
        for p1, p2 in combinations(points, 2)
        if p2 in distances[p1]
    ]

    # Apply Kruskal's algorithm for MST
    edges.sort()  # Sort edges by distance
    mst_cost = 0
    sets = {i: i for i in range(len(points))}

    def find(x):
        if sets[x] != x:
            sets[x] = find(sets[x])
        return sets[x]

    def union(x, y):
        root_x, root_y = find(x), find(y)
        if root_x != root_y:
            sets[root_y] = root_x

    for dist, i1, i2 in edges:
        if find(i1) != find(i2):
            union(i1, i2)
            mst_cost += dist

    return mst_cost


# Strong heuristic function
def strong_heuristic(problem: DungeonProblem, state: DungeonState) -> float:
    cache = problem.cache()
    state_key = (state.player, frozenset(state.remaining_coins))
    #if this state is in cache return it from the cahce
    if state_key in cache:
        return cache[state_key]

   
    if 0 not in cache:
     # calculate distances between all coins and exit and save it in cache 
     ##this step is done only once 
        all_points = [*state.remaining_coins,state.layout.exit]
        distances = {point: bfs_distance(point, state.layout) for point in all_points}
        cache[0]=distances
    else:
        distances=cache[0]
    ##calculate distances between players and everything else
    distance_from_player=bfs_distance(state.player,state.layout)
    # If no coins are remaining, return the distance from player to exit
    if not state.remaining_coins:
        return distance_from_player.get(state.layout.exit, float('inf'))

    # Compute MST cost on remaining coins
    mst_coins_cost = mst_cost(list(state.remaining_coins), distances)

    # Combine heuristic: Player-to-nearest coin + MST of coins + nearest coin to exit
    player_to_coin = min(distance_from_player[coin] for coin in state.remaining_coins)
    coin_to_exit = min(distances[state.layout.exit][coin] for coin in state.remaining_coins)

    heuristic_value = player_to_coin + mst_coins_cost + coin_to_exit
    cache[state_key] = heuristic_value
    return heuristic_value















##doesn't get good result so try anther approach


# #TODO: Import any modules and write any functions you want to use
# def strong_heuristic(problem: DungeonProblem, state: DungeonState) -> float:
#     cache = problem.cache()
#     # Cache key using player state and remaining_coins 
#     state_key = (state.player, frozenset(state.remaining_coins))
#     # Check if the heuristic for this state has already been computed
#     if state_key in cache:
#         return cache[state_key]

#     # Get cached distances or compute them if not available
#     distance_from_player = cache.get(state.player) or bfs_distance(state.player, state.layout)
#     cache[state.player] = distance_from_player  # Cache the distance from the player

#     distance_from_exit = cache.get(state.layout.exit) or bfs_distance(state.layout.exit, state.layout)
#     cache[state.layout.exit] = distance_from_exit  # Cache the distance from the exit
#     # If no coins are remaining, return the distance from player to exit
#     if not state.remaining_coins:
#         return distance_from_player.get(state.layout.exit, float('inf'))
    
#     coinplayer = 0  # Total distance to collect all coins
#     coinexit = 0  # Total distance from each coin to the exit
#     coinplayer1 = 0  # Maximum distance from player to any coin
#     coinexit1 = float('inf')  # Minimum distance from any coin to the exit

#     # Loop through each remaining coin to calculate distances
#     for coin in state.remaining_coins:
#         distance_to_exit_coin = distance_from_player.get(coin, 0)  # Distance from player to coin
#         distance_from_exit_coin = distance_from_exit.get(coin, float('inf'))  # Distance from exit to coin
#         coinplayer += distance_to_exit_coin  # Accumulate distances from player to coins
#         coinplayer1 = max(distance_to_exit_coin, coinplayer1)  # Track the maximum distance to a coin
#         coinexit += distance_from_exit_coin  # Accumulate distances from coins to exit
#         coinexit1 = min(distance_from_exit_coin, coinexit1)  # Track the minimum distance to exit

#     # Calculate two potential heuristic values
#     heuristic_value1 = int((coinplayer + coinexit) / len(state.remaining_coins))  # Average heuristic
#     heuristic_value2 = coinplayer1 + coinexit1  # Combined max distance heuristic
#     heuristic_value = max(heuristic_value1, heuristic_value2)  # Choose the stronger heuristic

#     # Cache the computed heuristic value
#     cache[state_key] = heuristic_value
#     return heuristic_value1 # Return the calculated heuristic value

