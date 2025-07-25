import sdl2
import sdl2.ext
import sdl2.ext.ttf
import numpy as np
import Tips

class Button:
	x : int
	y : int
	wdt : int
	hgh : int
	r : int
	g : int
	b : int
	tip_str : str

	hide_tex : sdl2.SDL_Texture = None
	high_tex : sdl2.SDL_Texture = None
	curr_tex : sdl2.SDL_Texture = None

	def __init__(self, renderer, tip_str : str, x : int, y : int, width: int, height: int, hide_texture : str, high_texture : str):
		self.tip_str = tip_str
		
		self.x = x
		self.y = y
		self.wdt = width
		self.hgh = height

		self.set_color(64, 64, 64)

		surface_hide = sdl2.ext.load_image(hide_texture)
		self.hide_tex = sdl2.SDL_CreateTextureFromSurface(renderer.sdlrenderer, surface_hide)
		sdl2.SDL_FreeSurface(surface_hide)

		surface_hgh = sdl2.ext.load_image(high_texture)
		self.high_tex = sdl2.SDL_CreateTextureFromSurface(renderer.sdlrenderer, surface_hgh)
		sdl2.SDL_FreeSurface(surface_hgh)

		self.onclick_func = None
		self.hover_func = None

	def destroy(self):

		if hasattr(self, "hide_tex") and self.hide_tex:
			sdl2.SDL_DestroyTexture(self.hide_tex)
			self.hide_tex = None

		if hasattr(self, "high_tex") and self.high_tex:
			sdl2.SDL_DestroyTexture(self.high_tex)
			self.high_tex = None

		if hasattr(self, "curr_tex") and self.curr_tex:
			sdl2.SDL_DestroyTexture(self.curr_tex)
			self.curr_tex = None

	def set_color(self, r : int, g : int, b : int):
		self.r = r
		self.g = g
		self.b = b

	def click(self):
		if(self.onclick_func):
			self.onclick_func()

	def cursorHover(self, renderer, mouse_x : int, mouse_y : int) -> Tips.Tip | None :
		if( mouse_x >= self.x and mouse_y >= self.y and mouse_x <= self.x + self.wdt and mouse_y <= self.y + self.hgh):
			self.set_color(80, 80, 80)
			self.curr_tex = self.high_tex
			x = self.x + self.wdt
			y = self.y + self.hgh//2
			return Tips.Tip(renderer, self.tip_str, x, y)
		else:
			self.set_color(64, 64, 64)
			self.curr_tex = self.hide_tex
			return None

	def draw(self, renderer):

		renderer.color = sdl2.ext.Color(32, 32, 32)
		outer_rect = sdl2.SDL_Rect(self.x, self.y, self.wdt, self.hgh)
		renderer.fill(outer_rect)

		margin = 4
		renderer.color = sdl2.ext.Color(self.r, self.g, self.b)
		inner_rect = sdl2.SDL_Rect(self.x + margin, self.y + margin, self.wdt - 2*margin, self.hgh-2*margin)
		renderer.fill(inner_rect)

		sdl2.SDL_RenderCopy(renderer.sdlrenderer, self.curr_tex, None, inner_rect)



class ButtonWithText:
	x : int
	y : int
	wdt : int
	hgh : int
	r : int
	g : int
	b : int
	txt : str
	font_manager : sdl2.ext.FontManager

	def __init__(self, renderer, text : str, x : int, y : int, width: int, height: int):
		
		self.txt = text
		self.font_manager = sdl2.ext.FontManager("C:/Windows/Fonts/arial.ttf", 16);

		self.x = x
		self.y = y
		self.wdt = width
		self.hgh = height

		self.set_color(64, 64, 64)


	def set_color(self, r : int, g : int, b : int):
		self.r = r
		self.g = g
		self.b = b

	def set_text(self, text : str):
		self.txt = text

	def cursorHover(self, mouse_x : int, mouse_y : int) -> bool:
		if( mouse_x >= self.x and mouse_y >= self.y and mouse_x <= self.x + self.wdt and mouse_y <= self.y + self.hgh):
			self.set_color(80, 80, 80)
			return True
		else:
			self.set_color(64, 64, 64)
			return False;

	def draw(self, renderer):

		renderer.color = sdl2.ext.Color(32, 32, 32)
		outer_rect = sdl2.SDL_Rect(self.x, self.y, self.wdt, self.hgh)
		renderer.fill(outer_rect)

		margin = 4
		renderer.color = sdl2.ext.Color(self.r, self.g, self.b)
		inner_rect = sdl2.SDL_Rect(self.x + margin, self.y + margin, self.wdt - 2*margin, self.hgh-2*margin)
		renderer.fill(inner_rect)

		surface = self.font_manager.render(self.txt, color=sdl2.ext.Color(255, 255, 255))
		texture = sdl2.SDL_CreateTextureFromSurface(renderer.sdlrenderer, surface)
		w = sdl2.c_int()
		h = sdl2.c_int()
		sdl2.SDL_QueryTexture(texture, None, None, w, h)

		dstrect = sdl2.SDL_Rect(
            self.x + (self.wdt - w.value) // 2,
            self.y + (self.hgh - h.value) // 2,
            w.value, h.value
        )

		sdl2.SDL_RenderCopy(renderer.sdlrenderer, texture, None, dstrect)
		sdl2.SDL_DestroyTexture(texture)
		sdl2.SDL_FreeSurface(surface)