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

class weapon_bar (object):
	def __init__(self, x, y, surface):
		self.x = x
		self.y = y
		self.w = 0
		self.h = 30
		self.color = (0,0,0)
		self.surface = surface
		self.max_bar_width = 200
		self.vector_magnitude = 0
		self.max_magnitude = 50
	
	def Get_surface(self):
		return self.surface

	def Get_position(self):
		return self.x, self.y

	def Get_dimensions(self):
		return self.x, self.y, self.w, self.h

	def Set_width(self, new_width):
		if(new_width < self.max_bar_width):
			self.w = new_width
		else:
			self.w = self.max_bar_width

	def Set_color(self, new_color):
		self.color = new_color

	def Get_width(self):
		return self.w

	def Get_max_bar_width(self):
		return self.max_bar_width

	def Get_vector_magnitude(self):
		return self.vector_magnitude

	def Set_vector_magnitude(self, new_magnitude):
		if(new_magnitude < self.max_magnitude):
			self.vector_magnitude = new_magnitude
		else:
			self.vector_magnitude = self.max_magnitude

	def Interpolated_width(self, magnitude):
		new_width = (magnitude * self.max_bar_width)/ self.max_magnitude

		self.Set_width(new_width)

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

class weapon_bar_view (object):
	def __init__(self):
		pass
	def Bar_draw(self, x, y, w, h, surface):
		points = [(x, y), (x + w, y), (x + w, y + h), (x , y + h)]
		pygame.draw.polygon(surface, (0, 0, 100), points, 0)

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

class weapon_bar_controller (object):
	def __init__(self, model, view):
		self.model = model
		self.view = view
	
	def Update_view(self):
		x, y, w, h = self.model.Get_dimensions()
		surface = self.model.Get_surface()
		self.view.Bar_draw(x, y, w, h, surface)
	
	def Update_bar(self, update_status):
		magnitude = self.model.Get_vector_magnitude()
		self.model.Interpolated_width(magnitude)
		if(not update_status):
			return
		magnitude += 0.5
		self.model.Set_vector_magnitude(magnitude)

	def Get_magnitude(self):
		return self.model.Get_vector_magnitude()

	def Reset_bar(self):
		self.model.Set_vector_magnitude(0)
		self.model.Set_width(0)

