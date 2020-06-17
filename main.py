import numpy as np
import pygame
from pygame.locals import *
import sys
import parabolic
import world
import weapon
from utilities import *

WIDTH = 700
HEIGHT = 500
WIDTH_PANEL = 0
HEIGHT_PANEL = 85
FPS = 60
BACKGROUND_COLOR = (255, 255, 255)
FINAL_WIDTH = WIDTH_PANEL + WIDTH
FINAL_HEIGHT = HEIGHT_PANEL + HEIGHT
RIGHT_BUTTON = 2
LEFT_BUTTON = 0
WEAPON_X = 50
WEAPON_Y = 400

pygame.init()
window = pygame.display.set_mode((FINAL_WIDTH,FINAL_HEIGHT))
pygame.display.set_caption("Parabolic shot")
fpsClock = pygame.time.Clock()

fire_flag = False

status_bar = False

weapon_vector_position = PVector(WEAPON_X, WEAPON_Y)
mouse_vector_position = PVector(0, 0)

def get_degrees(weapon_w, weapon_h):
	global weapon_vector_position
	global mouse_vector_position
	weapon_vector_position.set(WEAPON_X + weapon_w/2, WEAPON_Y + weapon_h/2)
	x, y = pygame.mouse.get_pos()
	mouse_vector_position.set(x, y)
	pygame.draw.line(window, (0, 0, 0), (weapon_vector_position.x, weapon_vector_position.y), (mouse_vector_position.x, mouse_vector_position.y))
	weapon_vector_position.substract(mouse_vector_position)
	degree = weapon_vector_position.Get_angle()
	#print("degree: {}, x: {}, y: {}".format(degree, weapon_vector_position.x, weapon_vector_position.y))
	return degree

def shoot_force(x, y, magnitude):
	force = PVector(x, y)
	force.normalize()
	force.multiplication(magnitude)
	return force

def events ():
	for event in pygame.event.get():
		if (event.type == QUIT):
			pygame.quit()
			sys.exit()
		elif(event.type == pygame.KEYDOWN):
			if(event.key == pygame.K_o):
				global fire_flag
				global degree
				fire_flag = True
				pass
			elif (event.key == pygame.K_p):
				global status_bar
				status_bar = not status_bar

def background():
	window.fill((BACKGROUND_COLOR))
	#points = [(0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT)]
	#pygame.draw.polygon(window, (0, 0, 0), points, 3)

def update_surface_task():
	pygame.display.update()
	fpsClock.tick(FPS)

##################################################
# Tiro parabolico
# 1.- crear el lanzador
#	1.1- como sera la interacción
#	1.2- como se define la potencia	y dirección
# 2.- Movimiento del proyectil
#	2.1- asignar los parametros anteriores
##################################################

def main():
	# tiempo de retraso en milisegundos en la primera repetición
	delay = 101
	# intervalo de tiempo en milisegundos entre repeticiones
	interval = 100
	# habilita la repetición de teclas
	pygame.key.set_repeat(delay, interval)
	
	projectile_model = parabolic.projectile(20, 400, 10, window)
	projectile_view = parabolic.projectile_view()
	projectile_controller = parabolic.projectile_controller(projectile_model, projectile_view)

	world_model = world.world(WIDTH, HEIGHT, window)
	world_view = world.world_view()
	world_controller = world.world_controller(world_model, world_view)

	referee_model = world.rules(projectile_controller, WIDTH, HEIGHT)
	referee_view = world.rules_view()
	referee_controller = world.rules_controller(referee_model, referee_view)

	weapon_model = weapon.weapon(50, 400, window)
	weapon_view = weapon.weapon_view()
	weapon_controller = weapon.weapon_controller(weapon_model, weapon_view)

	weapon_bar = weapon.weapon_bar(100, 100, window)
	weapon_bar_view = weapon.weapon_bar_view()
	weapon_bar_controller = weapon.weapon_bar_controller(weapon_bar, weapon_bar_view)


	global fire_flag

	while(True):
		background()

		projectile_controller.Update_model()

		projectile_controller.Update_view()

		world_controller.Update_view()

		referee_controller.Check_edges()

		weapon_bar_controller.Update_view()

		weapon_bar_controller.Update_bar(status_bar)

		if(fire_flag):
			#force = shoot_force(x, y, magnitude)
			#projectile_controller.Apply_force(force)
			fire_flag = False
			#weapon_controller.Update_view(degree)
		weapon_w, weapon_h = weapon_controller.Get_size()
		degree = get_degrees(weapon_w, weapon_h)
		weapon_controller.Update_view(degree)

		events()
		update_surface_task()
		pass

if(__name__ == "__main__"):
	main()