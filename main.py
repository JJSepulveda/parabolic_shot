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

pygame.init()
window = pygame.display.set_mode((FINAL_WIDTH,FINAL_HEIGHT))
pygame.display.set_caption("Parabolic shot")
fpsClock = pygame.time.Clock()

fire_flag = False

def events ():
	for event in pygame.event.get():
		if (event.type == QUIT):
			pygame.quit()
			sys.exit()
		elif(event.type == pygame.KEYDOWN):
			if(event.key == pygame.K_o):
				global fire_flag
				fire_flag = True
				print("evento")
				pass

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
	
	

	projectile_model = parabolic.projectile(20, 400, 10, window)
	projectile_view = parabolic.projectile_view()
	projectile_controller = parabolic.projectile_controller(projectile_model, projectile_view)

	world_model = world.world(WIDTH, HEIGHT, window)
	world_view = world.world_view()
	world_controller = world.world_controller(world_model, world_view)

	referee_model = world.rules(projectile_controller, WIDTH, HEIGHT)
	referee_view = world.rules_view()
	referee_controller = world.rules_controller(referee_model, referee_view)

	weapon_model = weapon.weapon(0, 0, surf)
	weapon_view = weapon.weapon_view()
	weapon_controller = weapon.weapon_controller(weapon_model, weapon_view)


	global fire_flag

	while(True):
		background()

		projectile_controller.Update_model()
		projectile_controller.Update_view()

		world_controller.Update_view()

		referee_controller.Check_edges()

		weapon_controller.Update_view()

		if(fire_flag):
			force = PVector(50,-50)
			projectile_controller.Apply_force(force)
			fire_flag = False

		events()
		update_surface_task()
		pass

if(__name__ == "__main__"):
	main()