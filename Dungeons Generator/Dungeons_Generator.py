import sys
import os
os.environ["PYSDL2_DLL_PATH"] = r"..\SDL2-2.32.2-win32-x64"
import sdl2
import sdl2.ext

import numpy as np
import heapq
import time

class Map :
    wdt : int
    hgh : int
    tiles = []

    empty_char = '.'
    wall_char = '#'
    floor_char = '+'
    corridor_char = '@'

    def __init__(self, width: int, height: int):
        self.wdt = width
        self.hgh = height
        self.tiles = np.empty((self.hgh, self.wdt), dtype=str)

    def generate_north_corridor(self, x1 : int, y1 : int, x2 : int, y2 : int):
        low = min(y1, y2)
        high = max(y1, y2)
        if high - low > 6:
            cy = np.random.randint(low + 3, high - 3)
        else:
            cy = (y1 + y2) // 2
        
        cy = int(cy)
    
        for i in range(int(min(y2, cy)), int(max(y2, cy) + 1)):
            self.tiles[i][x2] = self.corridor_char

        for i in range(int(min(x1, x2)), int(max(x1, x2) + 1)):
            self.tiles[cy][i] = self.corridor_char

        for i in range(int(min(cy, y1)), int(max(cy, y1) + 1)):
            self.tiles[i][x1] = self.corridor_char


    def generate_east_corridor(self, x1 : int, y1 : int, x2 : int, y2 : int):
        low = min(x1, x2)
        high = max(x1, x2)

        if high - low > 6:
            cx = np.random.randint(low + 3, high - 3)
        else:
            cx = (x1 + x2) // 2
        
        cx = int(cx)
    
        for i in range(int(min(x1, cx)), int(max(x1, cx)) + 1):
            self.tiles[y1][i] = self.corridor_char

        for i in range(int(min(y1, y2)), int(max(y1, y2) + 1)):
            self.tiles[i][cx] = self.corridor_char

        for i in range(int(min(cx, x2)), int(max(cx, x2) + 1)):
            self.tiles[y2][i] = self.corridor_char
        
        
    def generate_south_corridor(self, x1 : int, y1 : int, x2 : int, y2 : int):

        low = min(y1, y2)
        high = max(y1, y2)
        if high - low > 6:
            cy = np.random.randint(low + 3, high - 3)
        else:
            cy = (y1 + y2) // 2

        cy = int(cy)

        for i in range(int(min(y1, cy)), int(max(y1, cy) + 1)):
            self.tiles[i][x1] = self.corridor_char

        for i in range(int(min(x1, x2)), int(max(x1, x2) + 1)):
            self.tiles[cy][i] = self.corridor_char

        for i in range(int(min(cy, y2)), int(max(cy, y2) + 1)):
            self.tiles[i][x2] = self.corridor_char
        
    def generate_west_corridor(self, x1 : int, y1 : int, x2 : int, y2 : int):
        low = min(x1, x2)
        high = max(x1, x2)
        if high - low > 6:
            cx = np.random.randint(low + 3, high - 3)
        else:
            cx = (x1 + x2) // 2
        
        cx = int(cx)

        for i in range(int(min(x1, cx)), int(max(x1, cx) + 1)):
            self.tiles[y1][i] = self.corridor_char

        for i in range(int(min(y1, y2)), int(max(y1, y2) + 1)):
            self.tiles[i][cx] = self.corridor_char

        for i in range(int(min(cx, x2)), int(max(cx, x2) + 1)):
            self.tiles[y2][i] = self.corridor_char


    def generate_room(self, x : int, y : int, w : int, h : int, iteration : int):
        if iteration > 0 and w>=4 and h>=4:
            sx = int(x-w/2)
            sy = int(y-h/2)

            if sx < 0 or sy < 0 or sx+int(w)>=self.wdt or sy+int(h)>=self.hgh:
                return False

            for yy in range(sy, sy+int(h)):
                for xx in range(sx, sx+int(w)):
                    if self.tiles[yy][xx] == self.floor_char:
                        return False

            for yy in range(sy, sy+int(h)):
                for xx in range(sx, sx+int(w)):
                    self.tiles[yy][xx] = self.floor_char

            neighbours = []
            n_count = np.random.randint(2,3)
            tries = 0
            while(n_count > 0 and tries<10):
                n = np.random.choice([1,2,3,4])
                if n not in neighbours:
                    neighbours.append(n)
                    n_count = n_count-1
                tries = tries+1

            for i in neighbours:
          
                rw = np.random.uniform(w*3/4, w*5/6)
                rh = np.random.uniform(h*3/4, h*5/6)
                xx : int
                yy : int
            
                if i == 1:
                    # top neighbour 
                    xx = np.random.randint(-4,4)
                    yy = -np.random.randint((h+rh)/2*5/4, (h+rh)/2*6/4) - 2
                if i == 2:
                    # right neighbour 
                    xx = np.random.randint((w+rw)/2*5/4, (w+rw)/2*6/4) + 2
                    yy = np.random.randint(-4,4)
                if i == 3:
                    # bottom neighbour 
                    xx = np.random.randint(-4,4)
                    yy = np.random.randint((h+rh)/2*5/4, (h+rh)/2*6/4) + 2
                if i == 4:
                    # left neighbour 
                    xx = -np.random.randint((w+rw)/2*5/4, (w+rw)/2*6/4) - 2
                    yy = np.random.randint(-4,4)

                rx = x + xx
                ry = y + yy

                if rx-rw/2>=0 and ry-rh/2>=0 and rx-rw/2+rw<self.wdt and ry-rh/2+rh<self.hgh:
                    if not self.generate_room(rx, ry, rw, rh, iteration-1) :
                        continue
                
                    x1 : int
                    y1 : int
                    x2 : int
                    y2 : int
                
                    if i == 1:
                        x1 = sx + np.random.randint(w-2) + 1
                        y1 = sy
                        x2 = int(rx - rw/2) + np.random.randint(rw-2) + 1
                        y2 = int(ry - rh/2) + int(rh) -1
              
                        self.generate_north_corridor(x1, y1, x2, y2)
                    
                    if i == 2:
                        x1 = sx + w - 1
                        y1 = sy + np.random.randint(h-2) + 1
                        x2 = int(rx - rw/2)
                        y2 = int(ry - rh/2) + np.random.randint(rh-2) + 1

                        self.generate_east_corridor(x1,y1,x2,y2)

                    if i == 3:
                        x1 = sx + np.random.randint(w-2) + 1
                        y1 = sy + h - 1
                        x2 = int(rx - rw/2) + np.random.randint(rw-2) + 1
                        y2 = int(ry - rh/2)

                        self.generate_south_corridor(x1,y1,x2,y2)
                
                    if i == 4:
                        x1 = sx
                        y1 = sy + np.random.randint(h-2) + 1
                        x2 = int(rx - rw/2) + int(rw) - 1
                        y2 = int(ry - rh/2) + np.random.randint(rh-2) + 1

                        self.generate_west_corridor(x1,y1,x2,y2)
                    
                    
            return True
        return True # add the empty corridors

    def char_in_range(self, char, r : int, x : int, y : int):
        for yy in range(y-r, y+r+1):
            for xx in range(x-r, x+r+1):
                if xx>=0 and yy>=0 and xx<self.wdt and yy<self.hgh and self.tiles[yy][xx] == char:
                    return True

        return False

    def add_walls(self):
        for y in range(self.hgh):
           for x in range(self.wdt):
               if self.tiles[y][x] == self.floor_char and self.char_in_range(self.empty_char, 1, x, y):
                    self.tiles[y][x] = self.wall_char
               elif self.tiles[y][x] == self.empty_char and self.char_in_range(self.corridor_char, 1, x, y):
                    self.tiles[y][x] = self.wall_char
                    
        for y in range(self.hgh):
           for x in range(self.wdt):
               if self.tiles[y][x] == self.corridor_char:
                    self.tiles[y][x] = self.floor_char
    
    def clear(self):
        for y in range(self.hgh):
            for x in range(self.wdt):
                self.tiles[y][x] = self.empty_char

    def draw(self, renderer, tile_size):
        for y in range(self.hgh):
            for x in range(self.wdt):
                tile = self.tiles[y][x]

                if tile == self.empty_char:
                    renderer.color = sdl2.ext.Color(32, 32, 32)
                
                if tile == self.wall_char:
                    renderer.color = sdl2.ext.Color(48, 48, 48)

                if tile == self.floor_char:
                    renderer.color = sdl2.ext.Color(64, 64, 64)

                if tile == self.corridor_char:
                    renderer.color = sdl2.ext.Color(64, 64, 64)

                rect = sdl2.SDL_Rect(tile_size*x, tile_size*y, tile_size, tile_size)
                renderer.fill(rect)



def main() :
    # window parameters
    WINDOW_COLOR = sdl2.ext.Color(48,48,48)
    WINDOW_SIZE = (600,480)
	
    # init sdl and renderer
    sdl2.ext.init()
    window = sdl2.ext.Window("Island Generator", WINDOW_SIZE)
    window.show()
    renderer = sdl2.ext.Renderer(window)
	
    # map parameters
    tile_size = 8
    map_width = int(WINDOW_SIZE[0] / tile_size)
    map_height = int(WINDOW_SIZE[1] / tile_size)

    mapa = Map(map_width, map_height)

    while True:
        
        x = int(mapa.wdt/2)
        y = int(mapa.hgh/2)
        w = int(mapa.wdt*2/9)
        h = int(mapa.hgh*2/9)

        mapa.clear()
        mapa.generate_room(x, y, w, h, 3)
        mapa.add_walls()

		# render
        renderer.color = WINDOW_COLOR
        renderer.clear()
        mapa.draw(renderer, tile_size)
        renderer.present()

        time.sleep(1);

if __name__ == '__main__':
	main()