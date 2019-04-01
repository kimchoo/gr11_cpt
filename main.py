from cellular_automata import CA_CaveFactory
from file_manager import f_manager
from pygame.locals import *
import scipy.interpolate
import pygame
import math

resize_factor = 75
block_loading_size = 1500
width = 1920   
height = 1080


def lerp(p, p1, factor):
    return ((p1 - p) * factor)

def distance(x,y,x1,y1):
    return math.sqrt(((x-x1)**2) +((y-y1)**2))

class point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class chunck:
    def __init__(self, ar):
        self.dimensions = 10
        self.ar = ar    #Post initialization this var becomes the filled chuncks ar
        self.player_pos = point(None,None)

        self.perf_div = {"row": None, "column": None}

    def gen_chuncks(self, ar):

      rtn_ar = []

      if len(ar) % self.dimensions == 0:
        c_ar_height = len(ar) // self.dimensions + 1
        self.perf_div["row"] = False
      else:
        c_ar_height = len(ar) // self.dimensions
        self.perf_div["row"] = True

      if len(ar[0]) % self.dimensions == 0 :
        c_ar_width = len(ar) // self.dimensions + 1
        self.perf_div["column"] = False
      else:
        c_ar_width = len(ar) // self.dimensions
        self.perf_div["column"] = True

      for r in range(0, c_ar_height):
        rtn_ar.append([])

        for c in range(0, c_ar_width):
          rtn_ar[r].append([])

      return rtn_ar

    def current_multiple(self,value):

      if value % self.dimensions == 0:
        return value // self.dimensions

      else:
        return value // self.dimensions +1 

    def extrapol_pos(self, chunck_r, chunck_c, r, c):
        x = chunck_c * self.dimensions + c
        y = chunck_r * self.dimensions + r

        return point(x,y)

    def filled(self):

        ar = self.gen_chuncks(self.ar)

        for r in range(0, len(ar)):
            c_counter = self.current_multiple(r)

            for c in range(0, len(ar[0])):
                r_counter = self.current_multiple(c)

                ar[r_counter][c_counter].append(ar[r][c])
                print ar[r][c]
        return(ar)

class camera:
    def __init__(self,x,y):
        self.pos = point(x, y)
        self.follow_point = None

    def world_screen(self, p):
        return point(p.x + width/2 - self.pos.x, -p.y + height/2 + self.pos.y)

    def screen_world(self):
        pass

    def follow(self, obj):
        self.follow_point = obj

    def update(self):
        if self.follow_point != None:
            self.pos.x += lerp(self.pos.x, self.follow_point.x, 0.2)
            self.pos.y += lerp(self.pos.y, self.follow_point.y, 0.2)

class terrain:
    def __init__(self, _width, _height ,read, ar):

        self.colors = {"black": (0,0,0), "white": (255,255,255), "red": (255,0,0), "green": (0,255,0), "blue":(0,0,255), "violet": (155,155,255)}

        if read == True:
            self.point_ar = f_manager.csv_str_convert(ar)
            self.height = len(ar)
            self.width = len(ar[0])

        if read == False:
            self.width = _width
            self.height = _height
            caf = CA_CaveFactory(self.height, self.width,0.45)
            caf.gen_map()
            self.point_ar = caf.format_grid()
            self.smooth_terrain()

    def draw(self):
        for chunck_r in range(0,len(chuncks.ar)):
            for chunck_c in range(0, len(chuncks.ar[chunck_r])):
                pos = chuncks.extrapol_pos(chunck_r, chunck_c, 0, 0)

                #if distance(player.x, player.y, pos.x, pos.y) <= 10:
                print chuncks.ar[chunck_r]
                for r in range(0, len(chuncks.ar[chunck_r][chunck_c])):
                    
                    for c in range(0, len(chuncks.ar[chunck_r][chunck_c][r])):
                        block_pos = chuncks.extrapol_pos(chunck_r, chunck_c, r , c)
                        self.draw_block(self.point_ar[block_pos.y][block_pos.x][r][c], block_pos.x, block_pos.y)

    def draw_block(self, b_type, x, y):
        world_point = point(x * resize_factor,y * resize_factor)
        screen_point = cam.world_screen(world_point)
        if b_type == 1:
            if screen_point.x >= -resize_factor and screen_point.x <= width + resize_factor:
                if screen_point.y >= -resize_factor and screen_point.y <= height + resize_factor:
                    pygame.draw.rect(screen, self.colors["black"],((screen_point.x, screen_point.y),(resize_factor,resize_factor)))

    def smooth_terrain(self):

        for r in range(0, self.height):
            for c in range(0,self.width):
                if self.point_ar[r][c] == 0 : pass

                elif self.touch_points(self.point_ar, r, c) <= 2.25:
                    self.point_ar[r][c] = 0

    def touch_points(self, ar, row, column):
        c = 0.0
        if ((row>0) == (row<self.height -1)) and ((column>0) == (column<self.width -1)):
            if (ar[row][column] == 1):
                if (ar[row][column -1] == 1): c+=1
                if (ar[row][column +1] == 1): c+=1
                if (ar[row -1][column] == 1): c+=1
                if (ar[row +1][column] == 1): c+=1
                if (ar[row +1][column +1] == 1): c+=.25
                if (ar[row -1][column +1] == 1): c+=.25
                if (ar[row +1][column -1] == 1): c+=.25
                if (ar[row -1][column +1] == 1): c+=.25
        return (c)

class input_manager:
    def __init__(self):
        self.w = False
        self.a = False
        self.s = False
        self.d = False
        self.h = False
        self.g = False

    def update(self):
        keys=pygame.key.get_pressed()
        self.w = keys[pygame.K_w]
        self.a = keys[pygame.K_a]
        self.s = keys[pygame.K_s]
        self.d = keys[pygame.K_d]
        self.h = keys[pygame.K_h]
        self.g = keys[pygame.K_g]

__run__ = True
pygame.init()
player_input = input_manager()
f_manager = f_manager()

flags = DOUBLEBUF
screen = pygame.display.set_mode((width,height), flags)
screen.set_alpha(None)
clock = pygame.time.Clock()
clock.tick(1000)

cam = camera(0,0)
player = point(100,100)
cam.follow(player)
speed = 5

screen.fill((0,0,0))
print("g to generate new world")
print("h to load file")

while __run__ == True:   #Menu Session
    for event in pygame.event.get():  
        if event.type == pygame.QUIT: 
            pygame.quit()

    player_input.update()

    if player_input.g == True:
        gameworld = terrain(100, 100, False, None) #width, height
        f_manager.create_save_file(gameworld.point_ar)
        break
    if player_input.h == True:
        gameworld = terrain(None, None, True, f_manager.read_save_file("/home/kimchoo/Code/Python/cs11_cpt/world.csv"))
        break

chuncks = chunck(gameworld.point_ar)
chuncks.ar = chuncks.filled()

while __run__ == True:   #Game session
    for event in pygame.event.get():  
        if event.type == pygame.QUIT: 
            pygame.quit()

    player_input.update() 

    if player_input.a:
        player.x -= speed
    if player_input.d:
        player.x += speed
    if player_input.w:
        player.y += speed
    if player_input.s:
        player.y -= speed

    screen_point = cam.world_screen(player)
    pygame.draw.rect(screen, (255,255,255),((screen_point.x, screen_point.y),(10,10)))

    cam.update()
    gameworld.draw()

    pygame.display.update()

    screen.fill((155,155,255))
