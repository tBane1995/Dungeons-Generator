

import numpy as np
import heapq
import time

map_wdt = 56
map_hgh = 32
mapa = np.empty((map_hgh, map_wdt), dtype=str)

empty_char = '.'
wall_char = '#'
floor_char = '+'

##############################

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)

    def __repr__(self):
        return f"({self.x},{self.y})"

##############################

def heuristic(a: Point, b: Point):
    return abs(a.x - b.x) + abs(a.y - b.y)

def getNeighbours(p: Point):
    neighbours = []
    for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
        nx, ny = p.x + dx, p.y + dy
        if 0 <= nx < map_wdt and 0 <= ny < map_hgh:
            if mapa[ny][nx] != floor_char:
                neighbours.append(Point(nx, ny))
    return neighbours

def aStar(start: Point, goal: Point):
    openSet = []
    heapq.heappush(openSet, (0, start))
    cameFrom = {}
    costSoFar = {}
    cameFrom[start] = None
    costSoFar[start] = 0

    while openSet:
        _, current = heapq.heappop(openSet)

        if current == goal:
            path = []
            while current:
                path.append(current)
                current = cameFrom[current]
            path.reverse()
            return path

        for neighbor in getNeighbours(current):
            newCost = costSoFar[current] + 1
            if neighbor not in costSoFar or newCost < costSoFar[neighbor]:
                costSoFar[neighbor] = newCost
                priority = newCost + heuristic(neighbor, goal)
                heapq.heappush(openSet, (priority, neighbor))
                cameFrom[neighbor] = current

    return []
   
   ##############################

def generate_room(x,y,w,h,iter):
    if iter > 0 and w>=4 and h>=4 and mapa[y][x] != floor_char:
	    sx = int(x-w/2)
	    sy = int(y-h/2)
	    
	    if sx < 0 or sy < 0 or sx+int(w)>=map_wdt or sy+int(h)>=map_hgh:
	    	return
	    
	    for yy in range(sy, sy+int(h)):
	        for xx in range(sx, sx+int(w)):
	            if xx>=0 and yy>=0 and xx<map_wdt and yy<map_hgh:
	            	mapa[yy][xx] = floor_char
	    
	    neighbour = np.random.choice([1,2,3,4])
	    xx : int
	    yy : int
	    	
	    if neighbour == 1:
	    	#top neighbour 
	    	xx = np.random.randint(-4,4)
	    	yy = np.random.randint(h*5/4, h*6/4)
	    if neighbour == 2:
	    	#right neighbour 
	    	xx = np.random.randint(w*5/4, w*6/4)
	    	yy = np.random.randint(-4,4)
	    if neighbour == 3:
	    	#bottom neighbour 
	    	xx = np.random.randint(-4,4)
	    	yy = -np.random.randint(h*5/4, h*6/4)
	    if neighbour == 4:
	    	#left neighbour 
	    	xx = -np.random.randint(w*5/4, w*6/4)
	    	yy = np.random.randint(-4,4)
	    	
	    	
	    rx = x + xx
	    ry = y + yy
	    
	    if rx>=0 and ry>=0 and rx<map_wdt and ry<map_hgh:
	    	
	    	rw = np.random.uniform(w*3/4, w*5/6)
	    	rh = np.random.uniform(h*3/4, h*5/6)
	    	generate_room(rx, ry, rw, rh, iter-1)
	    	 ##############################

def char_in_range(char, r, x, y):
	for yy in range(y-r, y+r+1):
		for xx in range(x-r, x+r+1):
			if xx>=0 and yy>=0 and xx<map_wdt and yy<map_hgh and mapa[yy][xx] == char:
				return True
	
	return False
	
def add_walls():
	for y in range(map_hgh):
	   for x in range(map_wdt):
            if mapa[y][x]==floor_char and char_in_range(empty_char, 1, x, y):
            	mapa[y][x] = wall_char

##############################

def clear_map():
    for y in range(map_hgh):
        for x in range(map_wdt):
            mapa[y][x] = empty_char

def draw_map():
    for y in range(map_hgh):
        for x in range(map_wdt):
            print(mapa[y][x], end='')
        print()

##############################

while True:
    clear_map()
    x = int(map_wdt/2)
    y = int(map_hgh/2)
    w = int(map_wdt*2/9)
    h = int(map_hgh*2/9)
    generate_room(x,y,w,h,3)
    add_walls()
    draw_map()
    print("\n\n")
    time.sleep(1);