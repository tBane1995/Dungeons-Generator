import sys
import os
import sdl2
import sdl2.ext
import time

import Mapa
import Tips
import Button


def main() :
	# window parameters
	WINDOW_COLOR = sdl2.ext.Color(48,48,48)
	WINDOW_SIZE = (800,600)
	
	# init sdl and renderer
	sdl2.ext.init()
	window = sdl2.ext.Window("Dungeons Generator", WINDOW_SIZE)
	window.show()
	renderer = sdl2.ext.Renderer(window)
	
	# map parameters
	tile_size = 8
	map_width = int(WINDOW_SIZE[0] / tile_size)
	map_height = int(WINDOW_SIZE[1] / tile_size)

	mapa = Mapa.Map(map_width, map_height)
	mapa.generate()

    # Tip
	tip : Tips.Tip
	tip = None

	# Button
	margin = 16
	btn_wdt = 40
	btn_hgh = 40

	btn_size = Button.ButtonWithText(
		renderer,
		str(map_width) + "x" + str(map_height),
		0 + margin,
		0 + margin,
		80,
		40)


	btn_generate = Button.Button(
		renderer,
		"generate map",
		margin,
		0 + btn_hgh + 2* margin,
		btn_wdt,
		btn_hgh,
		"tex\\btn_generate_hide.bmp",
		"tex\\btn_generate_high.bmp"
		)
	btn_generate.onclick_func = lambda: mapa.generate()

	btn_copy = Button.Button(
		renderer,
		"copy to clipboard",
		margin,
		0 + 2*btn_hgh + 3* margin,
		btn_wdt,
		btn_hgh,
		"tex\\btn_copy_hide.bmp",
		"tex\\btn_copy_high.bmp"
		)
	btn_copy.onclick_func = lambda: sdl2.SDL_SetClipboardText(mapa.as_string().encode('utf-8'))

	while True:

		mouse_x = sdl2.Sint32()
		mouse_y = sdl2.Sint32()
		sdl2.SDL_GetMouseState(mouse_x, mouse_y)

		tip = btn_generate.cursorHover(renderer, mouse_x.value, mouse_y.value) or \
			btn_copy.cursorHover(renderer, mouse_x.value, mouse_y.value)		

		# handle events
		events = sdl2.ext.get_events()
		for event in events:
			if event.type == sdl2.SDL_QUIT:
				sdl2.ext.quit()
				sys.exit(0)

			if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
				if btn_generate.cursorHover(renderer, mouse_x.value, mouse_y.value):
					btn_generate.click()

				if btn_copy.cursorHover(renderer, mouse_x.value, mouse_y.value):
					btn_copy.click()
    
		# update
		

		# render
		renderer.color = WINDOW_COLOR
		renderer.clear()
		mapa.draw(renderer, tile_size)
		btn_generate.draw(renderer)
		btn_copy.draw(renderer)
		btn_size.draw(renderer)
		if tip:
			tip.draw(renderer)

		renderer.present()

if __name__ == '__main__':
	main()