import sokoban
import mySokobanSolver

wh = sokoban.Warehouse()
wh.load_warehouse("CAB320 A1 Student Template\warehouses\warehouse_01.txt")

cells = mySokobanSolver.taboo_cells(wh)
print(cells)
print(wh.walls)