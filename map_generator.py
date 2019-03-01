from cellular_automata import CA_CaveFactory 

class generator:
	def __init__(self):

		self.screen_size = width, height = 50, 50
		caf = CA_CaveFactory(self.screen_size[0],self.screen_size[1],0.4)
		caf.gen_map()
		self.ar = caf.format_grid()
