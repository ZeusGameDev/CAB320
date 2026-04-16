from scipy.optimize import linear_sum_assignment
'''

    Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.

You are NOT allowed to change the defined interfaces.
In other words, you must fully adhere to the specifications of the 
functions, their arguments and returned values.
Changing the interfacce of a function will likely result in a fail 
for the test of your code. This is not negotiable! 

You have to make sure that your code works with the files provided 
(search.py and sokoban.py) as your code will be tested 
with the original copies of these files. 

Last modified by 2021-08-17  by f.maire@qut.edu.au
- clarifiy some comments, rename some functions
  (and hopefully didn't introduce any bug!)

'''

# You have to make sure that your code works with 
# the files provided (search.py and sokoban.py) as your code will be tested 
# with these files
import search 
import sokoban

direction_offset = {'Left':(-1,0), 'Right':(1,0) , 'Up':(0,-1), 'Down':(0,1)} # (x,y) = (column,row)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [ (11885807, 'Zach', 'Coglan'), (12452068, 'Xavier', 'White')]
    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def list_taboo_cells(warehouse):
    # List of all coordinates  
    cells_to_check = [(x, y) for x in range(0, warehouse.ncols) for y in range(0, warehouse.nrows)]
    # Remove walls and targets
    cells_to_check = [cell for cell in cells_to_check if cell not in warehouse.walls and cell not in warehouse.targets]
    taboo_cell_list = []
    # Check each cell
    for cell in cells_to_check:
        x = cell[0]
        y = cell[1]
        # Check if cell within warehouse walls
        # Find walls in each cardinal direction
        walls_left = [(col, y) for col in range(0, x) if (col, y) in warehouse.walls]
        walls_right = [(col, y) for col in range(x+1, warehouse.ncols) if (col, y) in warehouse.walls]
        walls_up = [(x, row) for row in range(0, y) if (x, row) in warehouse.walls]
        walls_down = [(x, row) for row in range(y+1, warehouse.nrows) if (x, row) in warehouse.walls]
        # if not at least one wall in each direction, outside of warehouse
        if (not walls_left or not walls_right or not walls_up or not walls_down):
            continue

        # check if cell in a corner
        walls_adj_vert = [(row, col) for (row, col) in [(x, y-1), (x, y+1)] if (row, col) in warehouse.walls]
        walls_adj_hori = [(row, col) for (row, col) in [(x-1, y), (x+1, y)] if (row, col) in warehouse.walls]
        if (walls_adj_hori != [] and walls_adj_vert != []):
            taboo_cell_list.append(cell)
            continue

        # Check along upper wall for break in wall or target
        if ((x, y-1) in warehouse.walls):
            conf_valid = False
            # following wall to the left
            for i in range(x, 0, -1):
                # Stop once wall is reached
                if (i, y) in warehouse.walls:
                    break
                # Valid if taget along wall
                if (i, y) in warehouse.targets:
                    conf_valid = True
                    break
                # Valid if wall stops 
                if (i, y -1) not in warehouse.walls:
                    conf_valid = True
                    break
            
            # Same in oposite direction of cell
            for i in range(x, warehouse.ncols):
                if (i, y) in warehouse.walls:
                    break
                if (i, y) in warehouse.targets:
                    conf_valid = True
                    break
                if (i, y-1) not in warehouse.walls:
                    conf_valid = True
                    break
            if not conf_valid:
                taboo_cell_list.append(cell)
        
        # Check along lower wall
        if ((x, y+1) in warehouse.walls):
            conf_valid = False
            for i in range(x, 0, -1):
                if (i, y) in warehouse.walls:
                    break
                if (i, y) in warehouse.targets:
                    conf_valid = True
                    break
                if (i, y+1) not in warehouse.walls:
                    conf_valid = True
                    break
            
            for i in range(x, warehouse.ncols):
                if (i, y) in warehouse.walls:
                    break
                if (i, y) in warehouse.targets:
                    conf_valid = True
                    break
                if (i, y+1) not in warehouse.walls:
                    conf_valid = True
                    break
            if not conf_valid:
                taboo_cell_list.append(cell)

        # Check along left wall
        if ((x-1, y) in warehouse.walls):
            conf_valid = False
            for i in range(y, 0, -1):
                if (x, i) in warehouse.walls:
                    break
                if (x, i) in warehouse.targets:
                    conf_valid = True
                    break
                if (x-1, i) not in warehouse.walls:
                    conf_valid = True
                    break
            
            for i in range(y, warehouse.nrows):
                if (x, i) in warehouse.walls:
                    break
                if (x, i) in warehouse.targets:
                    conf_valid = True
                    break
                if (x-1, i) not in warehouse.walls:
                    conf_valid = True
                    break
            if not conf_valid:
                taboo_cell_list.append(cell)
        
        # Check along right wall
        if ((x+1, y) in warehouse.walls):
            conf_valid = False
            for i in range(y, 0, -1):
                if (x, i) in warehouse.walls:
                    break
                if (x, i) in warehouse.targets:
                    conf_valid = True
                    break
                if (x+1, i) not in warehouse.walls:
                    conf_valid = True
                    break
            
            for i in range(y, warehouse.nrows):
                if (x, i) in warehouse.walls:
                    break
                if (x, i) in warehouse.targets:
                    conf_valid = True
                    break
                if (x+1, i) not in warehouse.walls:
                    conf_valid = True
                    break
            if not conf_valid:
                taboo_cell_list.append(cell)
    
    return taboo_cell_list

def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A "taboo cell" is by definition
    a cell inside a warehouse such that whenever a box get pushed on such 
    a cell then the puzzle becomes unsolvable. 
    
    Cells outside the warehouse are not taboo. It is a fail to tag one as taboo.
    
    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
    Use only the following rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.
    
    @param warehouse: 
        a Warehouse object with a worker inside the warehouse

    @return
       A string representing the warehouse with only the wall cells marked with 
       a '#' and the taboo cells marked with a 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    # Main functionality in list_taboo_cells, leaves cells in list form for use in heuristic
    taboo_cell_list = list_taboo_cells(warehouse)
        
    # Convert list of cells into map
    # Modified version of warehouse.__str__
    X,Y = zip(*warehouse.walls) # pythonic version of the above
    x_size, y_size = 1+max(X), 1+max(Y)
    
    vis = [[" "] * x_size for y in range(y_size)]
    # can't use  vis = [" " * x_size for y ...]
    # because we want to change the characters later
    for (x,y) in warehouse.walls:
        vis[y][x] = "#"
    for (x,y) in taboo_cell_list:
        vis[y][x] = "X"
    return "\n".join(["".join(line) for line in vis])


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Due to issues with 
class State(sokoban.Warehouse):
    def __init__(self, warehouse):
        self.worker = warehouse.worker
        self.boxes = warehouse.boxes
        self.weights = warehouse.weights
        self.targets = warehouse.targets
        self.walls = warehouse.walls
        self.ncols = warehouse.ncols
        self.nrows = warehouse.nrows

    def __lt__(self, state):
        return True

class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''
    

    
    def __init__(self, warehouse):
        self.taboo_cells_list = list_taboo_cells(warehouse)
        self.initial = State(warehouse)

    def actions(self, warehouse):
        """Return a list of actions that can be executed in the given state. 
        Checks to determine if player or box movement can be within walls or 
        other boxes, and disallows them if so."""
        # index of the blank
        x,y = warehouse.worker
        L = []  # list of legal actions

        for i in direction_offset.keys():
            xy_offset = direction_offset[i]
            next_x , next_y = x+xy_offset[0] , y+xy_offset[1] # where the player will go if possible
            # ches if possible to move the player in this direction
            if (next_x,next_y) in warehouse.walls:
                continue # impossible move, do nothing
            elif (next_x,next_y) in warehouse.boxes:
                if (next_x + xy_offset[0], next_y + xy_offset[1]) in warehouse.walls or (next_x + xy_offset[0], next_y + xy_offset[1]) in warehouse.boxes:
                    continue # box next to the player could not be pushed
                else:
                    L.append(i)
            else:
                L.append(i)
        
        return L

    
    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        # Create a copy of the current state to modify into next state
        next_state = state.copy()
        # Extract the worker and boxes for easy access
        boxes = state.boxes.copy()
        worker = state.worker
        x = worker[0]
        y = worker[1]
        
        # Depending on action, move in different direction
        match action:
            case "Up":
                # Check if box above
                if (x, y-1) in boxes:
                    # Move box up
                    box_index = boxes.index((x, y-1))
                    boxes[box_index] = (x, y-2)
                # Move worker
                worker = (x, y-1)

            case "Down":
                # Same as first case except down
                if (x, y+1) in boxes:
                    box_index = boxes.index((x, y+1))
                    boxes[box_index] = (x, y+2)
                worker = (x, y+1)

            case "Left":
                if (x-1, y) in boxes:
                    box_index = boxes.index((x-1, y))
                    boxes[box_index] = (x-2, y)
                worker = (x-1, y)

            case "Right":
                if (x+1, y) in boxes:
                    box_index = boxes.index((x+1, y))
                    boxes[box_index] = (x+2, y)
                worker = (x+1, y)
            
            case _:
                # Raise error if action not a valid Up, Down, Left, Right
                raise TypeError("Action not of valid value")
        
        # Set the new positions of workers / boxes
        next_state.worker = worker
        next_state.boxes = boxes

        return State(next_state)


    def goal_test(self, state):
        """Return True if the state is a goal. The default method compares the
        state to self.goal, as specified in the constructor. Override this
        method if checking against a single self.goal is not enough."""
        return (set(state.boxes) == set(state.targets))

    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        # Always costs at least 1 to move player
        c += 1

        # Check each box to see if moved
        for i in range(len(state1.boxes)):
            if state1.boxes[i] != state2.boxes[i]:
                # If box is defferent, add the weight of the box to cost
                c += state1.weights[i]
        
        return c
            

        

    def h(self, node):
        state = node.state
        heuristic = 0
        player_h = 9999999
        box_h_mat = [[0 for x in range(len(state.boxes))] for y in range(len(state.targets))] 
        for i in range(len(state.boxes)):
            box_x = state.boxes[i][0]
            box_y = state.boxes[i][1]
            for j in range(len(state.targets)):
                target_x = state.targets[j][0]
                target_y = state.targets[j][1]
                box_h = (abs(box_x - target_x) + abs(box_y - target_y)) * (state.weights[i] + 1)
                box_h_mat[i][j] = box_h
            if state.boxes[i] in self.taboo_cells_list:
                heuristic += 999999999
            player_cur_h = abs(box_x - state.worker[0]) + abs(box_y - state.worker[1]) - 1
            if player_cur_h < player_h:
                player_h = player_cur_h
        
        boxes, targets = linear_sum_assignment(box_h_mat)

        for box, target in zip(boxes, targets):
            heuristic += box_h_mat[box][target]

        heuristic += player_h
        return heuristic

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_elem_action_seq(warehouse, action_seq):
    """Function that compares the actions in the provided sequence to the legal 
    actions and the result of those actions. If the sequence is legal, return 
    the resulting warehouse configuration as a string. If not, return "Impossible"."""
    
    ##         "INSERT YOUR CODE HERE"
    sokoban_problem = SokobanPuzzle(warehouse)
    
    for action in action_seq:
        #general checks for action validity
        if action not in direction_offset.keys():
            return "Impossible"
        if action not in sokoban_problem.actions(warehouse):
            return "Impossible"

        warehouse = sokoban_problem.result(warehouse, action)
        
    return warehouse.__str__()
    


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban(warehouse):
    '''
    This function analyses the given warehouse.
    It returns the two items. The first item is an action sequence solution. 
    The second item is the total cost of this action sequence.
    
    @param 
     warehouse: a valid Warehouse object

    @return
    
        If puzzle cannot be solved 
            return 'Impossible', None
        
        If a solution was found, 
            return S, C 
            where S is a list of actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
            C is the total cost of the action sequence C

    '''
    
    sokoban_problem = SokobanPuzzle(warehouse)

    solution = search.astar_graph_search(sokoban_problem)

    if solution == None:
        return 'Impossible', None
    
    S = solution.path()
    C = solution.path_cost
    return S, C



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

