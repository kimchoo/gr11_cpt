from map_generator import generator
import pygame

mg = generator()

class graphic:
	def __init__(self):

		self.colors = {"black": (0,0,0), "white": (255,255,255), "red": (255,0,0), "green": (0,255,0), "blue":(0,0,255), "violet": (155,155,255)}

		self.screen_size = mg.screen_size
		self.screen = pygame.display.set_mode(self.screen_size,0,32)
		self.point_ar = mg.ar

		self.QUIT = pygame.QUIT

	def draw_block(self,b_type,px,py):
		if b_type == 0:
			pygame.draw.rect(self.screen, self.colors["violet"],[px,py,1,1],1)
		elif b_type == 1:
			pygame.draw.rect(self.screen, self.colors["black"],[px,py,1,1],1)

	def initialize(self):
		pygame.init()

	def draw_map(self):
		self.smooth_terrain()
		for r in range(0,self.screen_size[0]):
			for c in range(0, self.screen_size[1]):
				self.draw_block(self.point_ar[c][r], [c], [r])

	def resize_map(self):
		pass

	def smooth_terrain(self):
		for r in range(0,self.screen_size[1]):
			for c in range(0,self.screen_size[0]):
				if self.touch_points(self.point_ar, r, c, 2) == False:
					self.point_ar[c][r] = 0

	def touch_points(self, ar, row, column, contacts):
		c = 0
		if ((row>0) == (row<self.screen_size[1] -1)) and ((column>0) == (column<self.screen_size[0] -1)):
			if (ar[row][column] == 1) and (ar[row][column -1] == 1): c+=1
			if (ar[row][column] == 1) and (ar[row][column +1] == 1): c+=1
			if (ar[row][column] == 1) and (ar[row -1][column] == 1): c+=1
			if (ar[row][column] == 1) and (ar[row +1][column] == 1): c+=1

		return (c >= contacts)

	def events(self):
		return [pygame.event.get(), pygame.QUIT]

	def testing(self):
		self.screen.fill(gr.colors["violet"])

	def update(self):
		pygame.display.update()
