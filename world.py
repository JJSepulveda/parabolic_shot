import numpy as np
import pygame
from pygame.locals import *

###################
## Consts
###################

MAX_TARGET_BAR_WIDTH = 80
MAX_HP_POINTS = 100

###################
## Global varaibles
###################

###################
## model
###################
class world (object):
	def __init__(self, screen_width, screen_height, surface):
		self.screen_size = {"width": screen_width, "height": screen_height}
		self.h = 25
		self.ground = {"x": 0, "y": screen_height - self.h}
		self.surface = surface
		pass
	def Set_ground_height(self, height):
		self.h = height
	def Get_ground_dimensions(self):
		x = self.ground['x']
		y = self.ground['y']
		w = self.screen_size['width']
		h = self.h
		return x, y, w, h
	def Get_ground_sizes(self):
		return self.screen_size['width'], self.h
	def Get_surface(self):
		return self.surface

class rules(object):
	def __init__(self, entitie_controller, world_controller, screen_width, screen_height):
		self.screen_size = {"width": screen_width, "height": screen_height}
		self.entitie = entitie_controller
		self.world = world_controller
		self.offsets = {'ground_height': 0, 'wall_width': 0}
		pass
	def Set_offsets (self, wall_width, ground_height):
		self.offsets['ground_height'] = ground_height
		self.offsets['wall_width'] = wall_width
	def Up_limit(self):
		pass
	def Down_limit(self):
		self.entitie.Ground_colision(self.screen_size['height']-self.offsets['ground_height'])
	def Left_limit(self):
		pass
	def Right_limit(self):
		#self.entitie.Wall_colision()
		pass
	def Check_edges(self):
		colision = False
		max_y = self.screen_size['height'] - self.offsets['ground_height']
		max_x = self.screen_size['width'] - self.offsets['wall_width']
		x, y, r = self.entitie.Get_dimensions()
		condition_up = y < 0
		condition_down = y + r >= max_y
		condition_right = x + r > max_x
		condition_left = x < 0
		
		if(condition_up):
			self.Up_limit()
			colision = True
		elif(condition_down):
			self.Down_limit()
			colision = True
		elif(condition_right):
			self.Right_limit()
			colision = True
		elif(condition_left):
			self.Left_limit()
			colision = True
		else: 
			pass

		return colision

class target(object):
	"""docstring for target"""
	def __init__(self, x, y, r, surface):
		self.x = x
		self.y = y
		self.r = r
		self.surface = surface
		self.HP_points = MAX_HP_POINTS
		self.bar_width = MAX_TARGET_BAR_WIDTH
		self.bar_height = 13
		self.color = (0, 0, 255)
		self.bar_color = (255, 0, 0)
	def Get_pos(self):
		return self.x, self.y
	def Get_HP(self):
		return self.HP_points
	def Set_HP(self, HP):
		if(HP > MAX_HP_POINTS):
			self.HP_points = self.HP_points
		elif(HP < 0):
			self.HP_points = 0
		else:
			self.HP_points = HP
	def Update_bar(self):
		self.bar_width = self.HP_points * MAX_TARGET_BAR_WIDTH / MAX_HP_POINTS
	def Get_bar_size(self):
		return self.bar_width, self.bar_height
	def Get_radius(self):
		return self.r
	def Get_color(self):
		return self.color
	def Get_bar_color(self):
		return self.bar_color
	def Get_surface(self):
		return self.surface
	def Random_position(self):
		self.x = np.random.randint(200, 600)
	def Reset(self):
		self.HP_points = MAX_HP_POINTS
		self.Update_bar()
		self.Random_position()

		

###################
## View
###################
class world_view (object):
	def __init__(self):
		pass
	def world_draw(self, x, y, w, h, surface):
		points = [(x, y), (x + w, y), (x + w, y + h), (x , y + h)]
		pygame.draw.polygon(surface, (0, 0, 0), points, 0)

class rules_view(object):
	def __init__(self):
		pass
	def Colision_print(self, colision_status):
		print("colision: {}".format(colision_status))

class target_view(object):
	"""target view"""
	def __init__(self):
		pass
	def Draw_target(self, x, y, r, color, surface):
		x = np.int32(x)
		y = np.int32(y)
		pygame.draw.circle(surface, color, (x,y), r)
	def Draw_HP_points(self, x, y, w, h, max_w, color, surface):
		x -= max_w/2
		y -= 30
		points = [(x, y), (x + w, y), (x + w, y + h), (x , y + h)]
		pygame.draw.polygon(surface, color, points, 0)
		points = [(x, y), (x + max_w, y), (x + max_w, y + h), (x , y + h)]
		pygame.draw.polygon(surface, (0, 0, 0), points, 3)

###################
## Controller
###################
class world_controller(object):
	def __init__(self, model, view):
		self.model = model
		self.view = view
		pass
	def Update_view(self):
		x, y, w, h = self.model.Get_ground_dimensions()
		surface = self.model.Get_surface()
		self.view.world_draw(x, y, w, h, surface)
	def Get_ground_sizes(self):
		return self.model.Get_ground_sizes()

class rules_controller(object):
	def __init__(self, model, view):
		self.model = model
		self.view = view

		_, height = self.model.world.Get_ground_sizes()
		self.model.Set_offsets(0, height)

	def Check_edges(self):
		colision = self.model.Check_edges()
		#self.view.Colision_print(colision)

class target_controller(object):
	def __init__(self, model, view):
		self.model = model
		self.view = view
	def Get_pos(self):
		return self.model.Get_pos()
	def Update_HP(self, damage):
		new_hp = self.model.Get_HP()
		new_hp -= damage
		self.model.Set_HP(new_hp)
		self.model.Update_bar()
	def Update_view(self):
		x, y = self.model.Get_pos()
		r = self.model.Get_radius()
		surface = self.model.Get_surface()
		color = self.model.Get_color()
		self.view.Draw_target(x, y, r, color, surface)

		bar_w, bar_h = self.model.Get_bar_size()
		bar_color = self.model.Get_bar_color()
		self.view.Draw_HP_points(x, y, bar_w, bar_h, MAX_TARGET_BAR_WIDTH, bar_color, surface)
	def Reset(self):
		self.model.Reset()
