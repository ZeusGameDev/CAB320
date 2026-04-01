import sokoban
import mySokobanSolver

wh = sokoban.Warehouse()
wh.load_warehouse("warehouses\warehouse_11.txt")

cells = mySokobanSolver.taboo_cells(wh)
print(cells)
