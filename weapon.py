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
		padding = 50
		self.my_surface = pygame.Surface((self.w, self.h))
	def Get_surface(self):
		return self.window_surface
	def Set_weapon_surface(self, new_surface):
		self.my_surface = new_surface
	def Get_mySurface(self):
		return self.my_surface
	def Get_dimensions(self):
		return self.x, self.y, self.w, self.h
	def Set_position(self, x, y):
		self.x = x
		self.y = y

class weapon_link (object):
	def __init__(self):
		pass

###################
## view
###################

class weapon_view (object):
	def __init__(self):
		#self.r_weapon_surface = 0
		pass
	def Weapon_draw(self, x, y, w, h, weapon_surface, window_surface,degree):
		weapon_surface.fill((200, 0, 0))
		points = [(40, 0), (w, 0), (w, h), (40 , h)]
		pygame.draw.polygon(weapon_surface, (0, 0, 100), points, 0)
		blitted_surface = window_surface.blit(weapon_surface, (x, y))

		old_center = blitted_surface.center
		rotated_surface = pygame.transform.rotate(weapon_surface, degree)
		rotRect = rotated_surface.get_rect()
		print(rotRect)
		rotRect.center = old_center
		window_surface.blit(rotated_surface, rotRect)

	def Weapon_rotate(self,surface, blitted_surface, degree):
		old_center = blitted_surface.get_rect().center
		rotated_surface = pygame.transform.rotate(blitted_surface, degree)
		rotRect = rotated_surface.get_rect()
		print(rotRect)
		rotRect.center = old_center
		surface.blit(rotated_surface, rotRect)

class weapon_link_view (object):
	def __init__(self):
		pass
###################
## Controller
###################

class weapon_controller(object):
	def __init__(self, model, view):
		self.model = model
		self.view = view
	def Update_view(self, degree):
		x, y, w, h = self.model.Get_dimensions()
		surface = self.model.Get_surface()
		weapon_surface = self.model.Get_mySurface()

		self.view.Weapon_draw(x, y, w, h, weapon_surface, surface, degree)
	def Rotate_weapon(self, degree):
		my_surface =  self.model.Get_mySurface()
		surface = self.model.Get_surface()
		self.view.Weapon_rotate(surface, my_surface,degree)
		#self.model.Set_weapon_surface(rotated_surface)

class weapon_link_controller (object):
	def __init__(self):
		pass