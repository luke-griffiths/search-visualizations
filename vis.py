import turtle
from time import sleep
import numpy as np
import argparse


### CONSTANTS ###
CELL_SIZE = 25
CELL_COLOR = "white"
PATH_COLOR = "blue"
SEARCH_COLOR = "orange"
###


### HELPER METHODS ###
def isValid(i, j, grid):
  return i >= 0 and i < len(grid) and j >= 0 and j < len(grid[0])


def iDFS(grid, visited):
  """
  Iterative DFS, each cell stores its parent to retrace
  """
  path = []
  s = []
  s.append((0,0, (None, None)))
  parents = {}
  parents[(0,0)] = None #start has no parent
  while(len(s)):
    tmp = s.pop()
    i , j = tmp[0], tmp[1]
    p = tmp[2]
    if not isValid(i, j, grid) or visited[i][j] or grid[i][j] == 1:
      continue
    visited[i][j] = True
    path.append((i, j))
    parents[(i, j)] = p
    if(grid[i][j] == -1):
      goal = (i , j)
      return goal, parents, path
    else:
      s.append((i + 1, j, (i , j)))
      s.append((i, j + 1, (i , j)))
      s.append((i - 1, j, (i , j)))
      s.append((i, j - 1, (i , j)))
  return


def bfs(grid, visited):
  path = []
  m = len(grid)
  n = len(grid[0])
  q = []
  q.append((0,0))
  visited[0][0] = True
  parents = {}
  parents[(0,0)] = None #start has no parent
  while len(q):
    tmp = q.pop(0)
    i, j = tmp[0], tmp[1]
    path.append((i, j))
    if grid[i][j] == -1:
      goal = (i , j)
      return goal, parents, path
    else:
      if not (i + 1 >= m  or visited[i + 1][j] or grid[i + 1][j] == 1):
        q.append((i + 1, j))
        visited[i + 1][j] = True
        parents[(i + 1, j)] = (i , j)
      if not (j + 1 >= n or visited[i][j + 1] or grid[i][j + 1] == 1):
        q.append((i, j + 1))
        visited[i][j + 1] = True
        parents[(i, j + 1)] = (i , j)
      if not (i - 1 < 0 or visited[i - 1][j] or grid[i - 1][j] == 1):
        q.append((i - 1, j))
        visited[i - 1][j] = True
        parents[(i - 1, j)] = (i , j)
      if not (j - 1 < 0 or visited[i][j - 1] or grid[i][j - 1] == 1):
        q.append((i, j - 1))
        visited[i][j - 1] = True
        parents[(i, j - 1)] = (i , j)
  return
    

def fillCell(t, row, col, color=CELL_COLOR):
  """
  Does not change the position/orientation of the turtle.
  Assumes zero indexing for row/col
  keep the penup at the end
  """
  t.setpos(t.pos()[0] + col * CELL_SIZE, t.pos()[1] - row * CELL_SIZE)
  t.pendown()
  t.fillcolor(color)
  t.begin_fill()
  #turtle starts facing right
  t.pendown()
  for _ in range(4):
    t.fd(CELL_SIZE)
    t.right(90)
  t.end_fill()
  t.penup()
  t.home()
  return 


def drawMap(t, m):
  N_ROWS = m.shape[0]
  N_COLS = m.shape[1]
  for row in range(N_ROWS):
    for col in range(N_COLS):
      if m[row][col] == 1:
        fillCell(t, row, col, "black")
      elif m[row][col] == -1:
        fillCell(t, row, col, "red")
      else:
        fillCell(t, row, col, "white")
  return


def initTurtle():
  t = turtle.Turtle()
  turtle.screensize(2560, 1600)
  t.speed("fastest")
  t.hideturtle()
  wn = turtle.Screen()
  wn.setup(width=2560, height=1600, startx=0, starty=0)
  # This turns off screen updates 
  wn.tracer(0) 
  return t, wn


def showPathFinding(t, wn, goal, parents, path):
  #show the cells we visited
  for j in range(len(path)):
    fillCell(t, path[j][0], path[j][1], SEARCH_COLOR)
    wn.update()
    sleep(0.1)
  #Now show the actual path we found
  while goal in parents:
    fillCell(t, goal[0], goal[1], PATH_COLOR)
    goal = parents[goal]
  wn.update()
  return


def run(map, alg, t, wn):
  #get our map and visited arrays
  m = np.loadtxt(map, dtype=int)
  NUM_ROWS = m.shape[0]
  NUM_COLS = m.shape[1]
  visited = np.full((NUM_ROWS, NUM_COLS), False, dtype=bool)
  #draw the map
  drawMap(t, m)
  #call the approriate alg function
  if alg == "bfs":
    goal, parents, path = bfs(m, visited)
  elif alg == "dfs":
    #goal, parents = dfs(0, 0, m, visited, None)
    goal, parents, path = iDFS(m, visited)
  else:
    print("You will never be able to see this print statement. Placeholder for more algs")
  #update the map with our path
  showPathFinding(t, wn, goal, parents, path)
  return
###


#Initialize parser
parser = argparse.ArgumentParser()
parser.add_argument('--map', choices = ['map1.txt', 'map2.txt', 'map3.txt'], required=True)
parser.add_argument('--alg', choices = ['bfs', 'dfs'], required=True, help="Enter your choice of algorithm")
#Read arguments from the command line
args = parser.parse_args()
#Now do the fun stuff
t, wn = initTurtle()
run(args.map, args.alg, t, wn)
# Keep the window open
wn.mainloop() 
