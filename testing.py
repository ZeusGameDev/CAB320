import sokoban
import mySokobanSolver

wh = sokoban.Warehouse()
wh.load_warehouse("warehouses\warehouse_8a.txt")
problem = mySokobanSolver.SokobanPuzzle(wh)

# action_seq = ['Up', 'Left', 'Up', 'Left', 'Left', 'Down', 'Left', 
#                        'Down', 'Right', 'Right', 'Right', 'Up', 'Up', 'Left', 
#                        'Down', 'Right', 'Down', 'Left', 'Left', 'Right', 
#                        'Right', 'Right', 'Right', 'Right', 'Right', 'Right'] 

# path_cost = 0

# for action in action_seq:
#     print(path_cost)
#     # print(path_cost + problem.h(wh))
#     print(wh)
#     wh_next = problem.result(wh, action)
#     path_cost = problem.path_cost(path_cost, wh, action, wh_next)
#     wh = wh_next

# print("-- Final --")
# print(path_cost)
# print(wh)

# answer, cost = mySokobanSolver.solve_weighted_sokoban(wh)
# print(answer)
# print(cost)


action_seq = ['Up', 'Left', 'Up', 'Left', 'Left', 'Down', 'Left', 
                       'Down', 'Right', 'Right', 'Right'] 

path_cost = 0

for action in action_seq:
    print(path_cost)
    print(wh)
    wh_next = problem.result(wh, action)
    path_cost = problem.path_cost(path_cost, wh, action, wh_next)
    wh = wh_next


answer, cost = mySokobanSolver.solve_weighted_sokoban(wh)
print(answer)
print(cost)