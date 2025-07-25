import sdl2
import sdl2.ext
import sdl2.ext.ttf
import numpy as np
import time

class Tip:
	x : int
	y : int
	r : int
	g : int
	b : int
	txt : str
	font_manager : sdl2.ext.FontManager

	def __init__(self, renderer, text : str, x : int, y : int):
		
		self.txt = text
		self.font_manager = sdl2.ext.FontManager("C:/Windows/Fonts/arial.ttf", 16);

		self.x = x
		self.y = y

		self.set_color(64, 64, 64)

		self.timer_start = time.time()


	def set_color(self, r : int, g : int, b : int):
		self.r = r
		self.g = g
		self.b = b

	def set_text(self, text : str):
		self.txt = text

	def draw(self, renderer):
		if self.txt != "":

			surface = self.font_manager.render(self.txt, color=sdl2.ext.Color(255, 255, 255))
			texture = sdl2.SDL_CreateTextureFromSurface(renderer.sdlrenderer, surface)
			w = sdl2.c_int()
			h = sdl2.c_int()
			sdl2.SDL_QueryTexture(texture, None, None, w, h)

			border = 2
			margin = 4

			renderer.color = sdl2.ext.Color(32, 32, 32)
			outer_rect = sdl2.SDL_Rect(self.x, self.y, w.value + 2*(margin+border), h.value+2*(margin+border))
			renderer.fill(outer_rect)
			
			renderer.color = sdl2.ext.Color(self.r, self.g, self.b)
			inner_rect = sdl2.SDL_Rect(self.x+border, self.y + border, w.value + 2*margin, h.value + 2*margin)
			renderer.fill(inner_rect)

			dstrect = sdl2.SDL_Rect(self.x+margin+border, self.y+margin + border ,w.value, h.value)

			sdl2.SDL_RenderCopy(renderer.sdlrenderer, texture, None, dstrect)
			sdl2.SDL_DestroyTexture(texture)
			sdl2.SDL_FreeSurface(surface)