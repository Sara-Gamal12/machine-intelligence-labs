from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers import utils

#TODO: (Optional) Instead of Any, you can define a type for the parking state
#2D list of the parking  
ParkingState = list[list[str]]
# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]

# This is the implementation of the parking problem
class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[Point]    # A set of points which indicate where a car can be (in other words, every position except walls).
    cars: Tuple[Point]      # A tuple of points where state[i] is the position of car 'i'. 
    slots: Dict[Point, int] # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the lot of car 'i') for every position.
                            # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking lot.
    height: int             # The height of the parking lot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        #initilize all slots with walls
        initial_State= [["#" for i in range(self.width)] for j in range(self.height)]

        for passage in self.passages:
            #check if passage is slot and update the state
            if passage  in self.slots.keys():
                initial_State[passage.y][passage.x]=str(self.slots[passage])
            #check if passage is car and update the state
            elif passage in self.cars:
                initial_State[passage.y][passage.x]= chr(ord('A') + self.cars.index(passage))
            #the passage is empty slot
            else:
                initial_State[passage.y][passage.x]="."
        return initial_State


    
    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        #check if all cars are in their slots
        for slot in self.slots.keys():
            #if solt of the car dosn't contain the index of the car return false
            if  state[slot.y][slot.x]!=chr(self.slots[slot] + ord('A')) :
                return False
        return True
    
    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
         actions:list=[]
         #loop on every position in state
         for i in range (self.height):
             for j in range(self.width):
                 #for every position check if it contain a car
                 if("A"<=state[i][j]<="Z"):
                     #for every direction check if the car can move in this direction
                     for dirc in Direction:
                        new_x = j + dirc.to_vector().x
                        new_y = i + dirc.to_vector().y
                        if 0 <= new_x < self.width and 0 <= new_y < self.height:  # Check bounds
                         newPosition=state[new_y][new_x]
                         #check if newposition is empty
                         if newPosition=="." or newPosition.isdigit():
                             actions.append((ord(state[i][j])-ord('A'),dirc))
         return actions
    
    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        new_state = [row[:] for row in state]   
        initial_state=self.get_initial_state()
         #loop on every position in state
        for i in range (self.height):
             for j in range(self.width):
                 #for every position check if it contain the car in the action(the car that should move)
                 if(ord(state[i][j])-ord('A')==action[0]):
                   
                    new_x = j + action[1].to_vector().x
                    new_y = i + action[1].to_vector().y
                    if 0 <= new_x < self.width and 0 <= new_y < self.height:  # Check bounds
                    #put the car in the new position 
                     new_state[new_y][new_x]=chr(action[0]+ord('A'))
                     #reset the empty passage
                     new_state[i][j]=initial_state[i][j] if initial_state[i][j].isdigit() else "."
                     
        return new_state
    
    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        #loop on every position in state
        for i in range (self.height):
             for j in range(self.width):
                 #for every position check if it contain the car in the action(the car that should move)
                 if "z">=state[i][j]>="A" and (ord(state[i][j])-ord('A')==action[0]):
                     #check if new position contain slot or not
                     new_x=j+action[1].to_vector().x
                     new_y=i+action[1].to_vector().y
                     newPosition=state[new_y][new_x]
                     #if new position is empty or if it the slot of the car itself
                     if(newPosition=="." or( Point(new_x,new_y)in self.slots.keys() and self.slots[Point(new_x,new_y)]==ord(state[i][j])-ord('A')) ):
                         return 1
                     #if it contain a slot
                     else :
                       return 101
                      
      
    
     # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages =  set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position:index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
    
