import numpy as np
import pygame
from pygame.locals import *
import sys
import parabolic
import world
import weapon
import math
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
AIMING_STATE = 0
SHOOT_STATE = 1
POST_SHOOT_STATE = 3 

pygame.init()
window = pygame.display.set_mode((FINAL_WIDTH,FINAL_HEIGHT))
pygame.display.set_caption("Parabolic shot")
fpsClock = pygame.time.Clock()

fire_flag = False

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

def get_shoot_components(degree):
	rad = math.radians(degree)
	x = math.cos(rad)
	y = math.sin(rad)
	return x, y

def limit_degrees(degrees):
	r = 0
	if(degrees > 270):
		r = 0
	elif(degrees > 90):
		r = 90
	else:
		r = degrees
	return r

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
				fire_flag = True
				pass
			elif (event.key == pygame.K_p):
				pass

def background():
	window.fill((BACKGROUND_COLOR))
	#points = [(0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT)]
	#pygame.draw.polygon(window, (0, 0, 0), points, 3)

def update_surface_task():
	pygame.display.update()
	fpsClock.tick(FPS)

def srpites_test(cols, rows):
	total_cells = cols * rows
	sheet = pygame.image.load('sprites/balah.png')
	sheet_scale = pygame.transform.scale(sheet, (200, 200))

	rect = sheet_scale.get_rect()
	w = rect.width/cols
	h = rect.height/rows
 
	center = (w/2, h/2)

	rect_position = (0 + center[0], 0 + center[1])

	#window.blit(sheet_scale, rect_position, (0, 0, w, h))

	cells = get_cells_dimensions_array(cols, rows, w, h)
	print(cells[0])
	print(cells[1])

	n = 1
	return sheet_scale, rect_position, cells, (w, h)

def get_cells_dimensions_array(cols, rows, w, h):
	cells = []
	for r in range(rows):
		for c in range(cols):
			x1 = c*w
			y1 = r*h

			frame_data = {'x1': x1, 'y1': y1}

			#print(frame_data)
			cells.append(frame_data)

	return cells


def change_sprite():
	pass


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

	actual_state = AIMING_STATE

	shoot_x = 0
	shoot_y = 0
	degree = 0

	sprt_surf, pos, cells, size = srpites_test(3, 3)

	global fire_flag
	status_bar = False

	#srpit update frames
	actual_time = 0
	next_frame = 80
	print("clock: {}".format(fpsClock.get_rawtime))
	frame = 0

	while(True):
		actual_time += fpsClock.get_time()
		#print("clock: {}".format(fpsClock.get_fps()))
		background()

		projectile_controller.Update_model()

		projectile_controller.Update_view()

		world_controller.Update_view()

		referee_controller.Check_edges()

		weapon_bar_controller.Update_view()

		weapon_bar_controller.Update_bar(status_bar)

		#state machine
		if(actual_state == AIMING_STATE):
			weapon_w, weapon_h = weapon_controller.Get_size()
			degree = get_degrees(weapon_w, weapon_h)
			weapon_controller.Update_view(degree)

			if(fire_flag):
				fire_flag = False
				degree = limit_degrees(degree)
				shoot_x, shoot_y = get_shoot_components(degree)
				actual_state = SHOOT_STATE
				status_bar = True
				print("change state")

		elif(actual_state == SHOOT_STATE):
			weapon_controller.Update_view(degree)
			if(fire_flag):
				magnitude = weapon_bar_controller.Get_magnitude()
				force = shoot_force(shoot_x, shoot_y, magnitude)
				projectile_controller.Apply_force(force)
				fire_flag = False
				actual_state = POST_SHOOT_STATE
				status_bar =  False
				print("change state")
		elif(actual_state == POST_SHOOT_STATE):
			weapon_controller.Update_view(degree)
			if(fire_flag):
				fire_flag = False
				projectile_controller.Reset()
				weapon_bar_controller.Reset()
				actual_state = AIMING_STATE
				print("change state")


		if(actual_time > next_frame):
			frame = (frame + 1) % 7
			actual_time = 0

		window.blit(sprt_surf, pos)

		window.blit(sprt_surf, (pos[0], pos[1] +200), (cells[frame]['x1'], cells[frame]['y1'], size[0], size[1]))
		
		events()

		update_surface_task()
		pass

if(__name__ == "__main__"):
	main()