import numpy as np
import pygame
from pygame.locals import *
from utilities import *
""" first time using the MVC pattron """
###################
## Consts
###################
GRAVITY_ACCELERATION = 0.1

###################
## Global varaibles
###################


###################
## model
###################
class projectile(object):
	def __init__(self, x, y, r, surface):
		self.backup_x = x
		self.backup_y = y
		self.projectile_position = PVector(x, y)
		self.projectile_velocity = PVector(0, 0)
		self.projectile_acceleration = PVector(0, 0)
		#self.projectile_size = {'width': w, 'height': h}
		self.projectile_radius = r
		self.mass = 10
		self.velocity_limit = 50
		self.projectile_color = (0, 0, 0)
		self.surface = surface
	def Set_position(self, x, y):
		self.projectile_position.set(x, y)
	def Get_position(self):
		x, y = self.projectile_position.Get_components()
		return x, y
	def Get_init_position(self):
		return self.backup_x, self.backup_y
	def Set_velocity(self, x, y):
		self.projectile_velocity.set(x, y)
	def Get_velocity(self):
		x = self.projectile_velocity.x
		y = self.projectile_velocity.y
		return x, y
	def Set_radius(self, r):
		self.projectile_radius = r
	def Get_radius(self):
		return self.projectile_radius
	def Set_color(self, color):
		self.projectile_color = color
	def Get_color(self):
		return self.projectile_color
	def Set_surface(self, surface):
		self.surface = surface
	def Get_surface(self):
		return self.surface
	def Set_mass(self, m):
		self.mass = m
	def Set_velocity_limit(self, v):
		self.velocity_limit = v
	def Update_position(self):
		self.projectile_velocity.add(self.projectile_acceleration)
		self.projectile_velocity.limit(self.velocity_limit)
		self.projectile_position.add(self.projectile_velocity)
		self.projectile_acceleration.set(0,0)
	def Apply_force(self, force_vector):
		# f = ma -> a = f/m
		#print("force_vector: {}, {}".format(force_vector.x, force_vector.y))		
		aceleration_vector = force_vector
		aceleration_vector.div(self.mass)
		self.projectile_acceleration.add(aceleration_vector)
	def Friction_force(self):
		#Coeficiente de friccion
		c = 0.3
		normal = 1
		friction_mag = c * normal
		velocity_mag = self.projectile_velocity.mag()
		if(velocity_mag > 0):
			friction_vector = PVector(self.projectile_velocity.x, self.projectile_velocity.y)
			friction_vector.multiplication(-1)
			friction_vector.normalize()
			friction_vector.multiplication(friction_mag)
			friction_vector.limit(velocity_mag)
			self.Apply_force(friction_vector)
	def Apply_gravity(self):
		#velocity_y = self.projectile_velocity.y
		#is_velocity_magnitude_inverse_of_gravity = velocity_y < 0
		#if(is_velocity_magnitude_inverse_of_gravity):
		gravity_vector = PVector(0, GRAVITY_ACCELERATION * self.mass)
		self.Apply_force(gravity_vector)

###################
## view
###################
class projectile_view(object):
	def __init__(self):
		pass
	def Projectile_draw(self, x, y, radius, color, surface):
		x = np.int32(x)
		y = np.int32(y)
		pygame.draw.circle(surface, color, (x,y), radius)

###################
## controller
###################
class projectile_controller(object):
	def __init__(self, model, view):
		self.model = model
		self.view = view
	def Apply_force(self, force_vector):
		self.model.Apply_force(force_vector)
	def Reset (self):
		x, y = self.model.Get_init_position()
		self.model.Set_position(x, y)
		self.model.Set_velocity(0,0)
		pass
	def Update_model(self):
		self.model.Apply_gravity()
		self.model.Friction_force()
		self.model.Update_position()
	def Update_view(self):
		x, y = self.model.Get_position()
		r = self.model.Get_radius()
		color = self.model.Get_color()
		surface = self.model.Get_surface()
		self.view.Projectile_draw(x, y, r, color, surface)
	def Ground_colision(self, h):
		v_x, v_y = self.model.Get_velocity()
		v_y *= -1
		self.model.Set_velocity(v_x, v_y)
		fix_y = h - self.model.Get_radius()
		x, _ = self.model.Get_position()
		self.model.Set_position(x , fix_y)
	def Get_dimensions(self):
		x, y = self.model.Get_position()
		r = self.model.Get_radius()
		return x, y, r
	def Set_position(self, x, y):
		self.model.Set_position(x, y)
