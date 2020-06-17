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
		self.degree = 0
		#self.main_center = (self.w/2, self.h/2)
	def Get_surface(self):
		return self.window_surface
	def Set_weapon_surface(self, new_surface):
		self.my_surface = new_surface
	def Get_mySurface(self):
		return self.my_surface
	def Get_dimensions(self):
		return self.x, self.y, self.w, self.h
	def Get_size(self):
		return self.w, self.h
	def Set_position(self, x, y):
		self.x = x
		self.y = y
	def Set_degree(self, new_degree):
		if(new_degree > 270):
			self.degree = 0
		elif(new_degree > 90):
			self.degree = 90
		else:
			self.degree = new_degree

	def Get_degree(self):
		return self.degree
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
		self.max_magnitude = 100
	
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
		pass
	def Weapon_draw(self, x, y, w, h, weapon_surface, window_surface, new_degree):
		weapon_surface.fill((255, 255, 255))
		weapon_surface.set_colorkey((255, 0, 0))
		points = [(w/2, 0), (w, 0), (w, h), (w/2 , h)]
		pygame.draw.polygon(weapon_surface, (0, 0, 0), points, 0)
		#blitted_surface = window_surface.blit(weapon_surface, (x, y))
		main_center = self.Calculate_weapon_position(x, y, w, h, weapon_surface)
		rotated_surface = pygame.transform.rotate(weapon_surface, new_degree)
		rotRect = rotated_surface.get_rect()
		rotRect.center = main_center
		window_surface.blit(rotated_surface, rotRect)

	def Calculate_weapon_position(self, x, y, w, h, weapon_surface):
		center_x = weapon_surface.get_width()/2
		center_y = weapon_surface.get_height()/2
		new_x = x + center_x 
		new_y = y + center_y 

		position = (new_x, new_y)

		return position

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
		self.model.Set_degree(degree)
		new_degree = self.model.Get_degree()
		self.view.Weapon_draw(x, y, w, h, weapon_surface, surface, new_degree)
	def Get_size(self):
		return self.model.Get_size()

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

	def Reset(self):
		self.model.Set_vector_magnitude(0)
		self.model.Set_width(0)

