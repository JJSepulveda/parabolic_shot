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
class weapon (object):
	def __init__(self, x, y, surface):
		self.x = x
		self.y = y
		self.h = 30
		self.w = 90
		self.window_surface = surface
		self.my_surface = pygame.Surface((100, 100))
	def Get_surface(self):
		return self.surface
	def Get_dimensions(self):
		return self.x, self.y, self.w, self.h
	def Set_position(self, x, y):
		self.x = x
		self.y = y


###################
## view
###################

class weapon_view (object):
	def __init__(self):
		pass
	def Weapon_draw(self, x, y, w, h, surface):
		self.my_surface.fill((255, 255, 255))
		points = [(x, y), (x + w, y), (x + w, y + h), (x , y + h)]
		pygame.draw.polygon(self.my_surface, (0, 0, 100), points, 0)

		surface.blit(self.my_surface, (x, y))
		pass

###################
## Controller
###################

class weapon_controller(object):
	def __init__(self, model, view):
		self.model = model
		self.view = view
	def Update_view(self):
		x, y, w, h = self.model.Get_dimensions()
		surface = self.model.Get_surface()

		self.view.Weapon_draw(x, y, w, h, surface)