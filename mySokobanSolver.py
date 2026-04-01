
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


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [ (11885807, 'Zach', 'Coglan'), (1234568, 'Grace', 'Hopper'), (1234569, 'Eva', 'Tardos') ]
    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


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


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''
    
    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' method is needed
    #     to satisfy the interface of 'search.Problem'.
    #
    #     You are allowed (and encouraged) to use auxiliary functions and classes

    
    def __init__(self, warehouse):
        raise NotImplementedError()

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        """
        raise NotImplementedError

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_elem_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Impossible', if one of the action was not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()


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
    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

