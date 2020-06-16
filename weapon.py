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
		return self.window_surface
	def Get_mySurface(self):
		return self.my_surface
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
	def Weapon_draw(self, x, y, w, h, weapon_surface, window_surface):
		weapon_surface.fill((255, 255, 255))
		points = [(0, 0), (w, 0), (w, h), (0 , h)]
		pygame.draw.polygon(weapon_surface, (0, 0, 100), points, 0)

		window_surface.blit(weapon_surface, (x, y))
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
		weapon_surface = self.model.Get_mySurface()

		self.view.Weapon_draw(x, y, w, h, weapon_surface, surface)