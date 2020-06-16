import numpy as np
import pygame
from pygame.locals import *

###################
## Consts
###################

###################
## Global varaibles
###################

###################
## model
###################
class world (object):
	def __init__(self, screen_width, screen_height, surface):
		self.screen_size = {"width": screen_width, "height": screen_height}
		self.ground = {"x": 0, "y": 550}
		self.surface = surface
		pass
	def Get_ground_dimensions(self):
		x = self.ground['x']
		y = self.ground['y']
		w = self.screen_size['width']
		h = 25
		return x, y, w, h
	def Get_surface(self):
		return self.surface

class rules(object):
	def __init__(self, entitie_controller, screen_width, screen_height):
		self.screen_size = {"width": screen_width, "height": screen_height}
		self.entitie = entitie_controller
		pass
	def Up_limit(self):
		pass
	def Down_limit(self):
		self.entitie.Ground_colision(self.screen_size['height'])
	def Left_limit(self):
		pass
	def Right_limit(self):
		#self.entitie.Wall_colision()
		pass
	def Check_edges(self):
		colision = False
		max_y = self.screen_size['height']
		max_x = self.screen_size['width']
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

###################
## View
###################
class world_view (object):
	def __init__(self):
		pass
	def world_draw(self, x, y, w, h, surface):
		points = [(x, y), (x + w, y), (x + w, y + h), (x , y + h)]
		pygame.draw.polygon(surface, (0, 0, 0), points, 0)
		pass

class rules_view(object):
	def __init__(self):
		pass
	def Colision_print(self, colision_status):
		print("colision: {}".format(colision_status))

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

class rules_controller(object):
	def __init__(self, model, view):
		self.model = model
		self.view = view
	def Check_edges(self):
		colision = self.model.Check_edges()
		#self.view.Colision_print(colision)
