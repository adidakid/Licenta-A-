import pygame
import math
from queue import PriorityQueue
from tkinter import messagebox

WIDTH = 1000

WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* pathfinding algorithm ")

# # # ----------------------------------------
# The colors for specific parents/childs in RGB
start_COLOR = (0, 255, 0)         # Green
end_COLOR = (255, 0, 0)           # Red
wall_COLOR = (0, 0, 51)           # Dark Blue
closed_COLOR = (255, 128, 0)      # Orange
open_COLOR = (0, 0, 204)          # Blue
path_COLOR = (255, 255, 51)       # Yellow
default_COLOR = (255, 255, 255)   # White
grid_COLOR = (128, 128, 128)      # Grey

# # # ----------------------------------------
# Def. parent proprieties
class Parent:
    def __init__(self, row, col, width, total_rows):
        
        # "width" == width of the node (all the nodes are squares)
        self.width = width
        self.row = row
        self.col = col
        
        # The node coordonates
        self.x = row * width
        self.y = col * width
        
        self.total_rows = total_rows
        self.color = default_COLOR
        self.childs = []
    
    # # # ----------------------------------------
    # start = the starting node
    # end = the end node 
    # wall = obstacles/walls
    # open = the nodes that the algorithm can check
    # closed = the nodes that were checked
    def get_pos(self):
        return self.row, self.col
    def is_start(self):
        return self.color == start_COLOR
    def is_end(self):
        return self.color == end_COLOR
    def is_wall(self):
        return self.color == wall_COLOR
    def is_closed(self):
        return self.color == closed_COLOR
    def is_open(self):
        return self.color == open_COLOR

    # # # ----------------------------------------
    # Changing the node type
    def make_start(self):
        self.color = start_COLOR
    def make_end(self):
        self.color = end_COLOR
    def make_wall(self):
        self.color = wall_COLOR
    def make_closed(self):
        self.color = closed_COLOR
    def make_open(self):
        self.color = open_COLOR
    def make_path(self):
        self.color = path_COLOR
    def reset(self):
        self.color = default_COLOR
    
    # Drawing the "node" in the shape of a square
    def draw(self, win, shape = 1):
        if shape == 1:
            pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        else:
            pygame.draw.circle(win, self.color, (self.x + self.width//2, self.y + self.width//2), self.width//3)
    
    def update_childs(self, grid):
        self.childs = []

        # # # ----------------------------------------
        # row = "x"
        # col = "y"
        # y - 1 = up
        # y + 1 = down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():        # Moving RIGHT a node
            self.childs.append(grid[self.row + 1][self.col])
            
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():                          # Moving LEFT a node
            self.childs.append(grid[self.row - 1][self.col])
            
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():        # Moving DOWN a node
            self.childs.append(grid[self.row][self.col + 1])
        
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():                          # Moving UP a node
            self.childs.append(grid[self.row][self.col - 1])
    
    def __lt__(self, other):
        return False

# The Heuristic value !
def h_value(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def show_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

def algortithm(draw, grid, start, end):
    count = 0                       #  count = take note about who enters first the extended list
    open_set = PriorityQueue()      
    
    ## # # ----------------------------------------
    # 0 == f_value ( F )
    # start == starting node
    open_set.put((0, count, start))
    came_from = {}
    
    g_value = {parent: float("inf") for row in grid for parent in row}      # getting the distance from the START parent to the CURRENT parent
    g_value[start] = 0
    
    f_value = {parent: float("inf") for row in grid for parent in row} 
    f_value[start] = h_value(start.get_pos(), end.get_pos())
    
    open_set_hash = {start}     # Keeping track if the the parents are in PriorityQueue
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
        # Eliminating the checked nodes, so they can't be rechecked
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        # Path Found
        if current == end:
            show_path(came_from, end, draw)
            end.make_end()
            start.make_start()
            return True
        
        for child in current.childs:
            temp_g_value = g_value[current] + 1 
            
            # If we found a better/shorter way continue from there
            if temp_g_value < g_value[child]:
                came_from[child] = current
                g_value[child] = temp_g_value 
                f_value[child] = temp_g_value + h_value(child.get_pos(), end.get_pos())
                
                if child not in open_set_hash:
                    count += 1
                    open_set.put((f_value[child], count, child))
                    open_set_hash.add(child)
                    child.make_open()
                    global shape 
                    shape = 2 
                      
        draw()
        
        # If the current node != start:     will be a "checked node"
        if current != start:
            current.make_closed()
    messagebox.showinfo("No Solution", "There was no solution")
    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows                 
    for i in range(rows):                      
        grid.append([])         
        for j in range(rows):
            # i will be the "row"  
            # j will be the "column"                 
            parent = Parent(i, j, gap, rows)        
            grid[i].append(parent)
    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        # For each "i" draw a line
        pygame.draw.line(win, grid_COLOR, (0, i * gap), (width, i * gap))
        pygame.draw.line(win, grid_COLOR, (i * gap, 0), (i * gap, width))

def draw(win, grid, rows, width):
    win.fill(default_COLOR)                 # Redraw everything white
    
    # Drawing the spots
    for row in grid:
        for parent in row:
            parent.draw(win)
    
    draw_grid(win, rows, width)
    pygame.display.update()         # updateing the display/win
    
def get_clicked_pos(pos, rows, width):
    gap = width // rows 
    y, x = pos 
    
    row = y // gap
    col = x // gap
    
    return row, col

# # # ----------------------------------------
# The PyGame win/display
def main(win, width):
    ROWS =  35
    grid = make_grid(ROWS, width)
    
    start = None
    end = None
    run = True
    started = False
    
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if started:
                continue
            
            if pygame.mouse.get_pressed()[0]:   # 0 = left
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                parent = grid[row][col]
            
                if not start and parent != end:
                    start = parent
                    start.make_start()  # Start point
            
                elif not end and parent != start:
                    end = parent
                    end.make_end()  # End point
            
                elif parent != end and parent != start:
                    parent.make_wall()  # wall / Obstacle point
            
            # Deleting things
            elif pygame.mouse.get_pressed()[2]:     # 2 = Right
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                parent = grid[row][col]
                parent.reset()
                if parent == start:
                    start = None
                elif parent == end:
                    end = None
            
            # Start
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    
                    # First checking for valid nodes/nodes
                    for row in grid:
                        for parent in row:
                            parent.update_childs(grid)
                    
                    algortithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                
                # Reset
                if event.key == pygame.K_r:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(WIN, WIDTH)