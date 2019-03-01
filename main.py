from graphics import graphic
import pygame

__run__ = True
gr = graphic()

while __run__  == True:

	for event in pygame.event.get():  
		if event.type == pygame.QUIT: 
			__run__ = False

	gr.initialize()
	gr.draw_map()

	gr.update()
