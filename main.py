import numpy as np
import pygame
from pygame.locals import *
import sys
import parabolic
import world
import weapon
import math
import ia_player
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
POST_EXPLOSION_STATE = 2
EXPLOSION_STATE = 3
AIMING_IA_STATE = 4


pygame.init()
window = pygame.display.set_mode((FINAL_WIDTH,FINAL_HEIGHT))
pygame.display.set_caption("Parabolic shot")
fpsClock = pygame.time.Clock()

change_state_flag = False
holding_up_ball_flag = True

weapon_vector_position = PVector(WEAPON_X, WEAPON_Y)
mouse_vector_position = PVector(0, 0)

def get_degrees(weapon_w, weapon_h):
	global weapon_vector_position
	global mouse_vector_position
	weapon_vector_position.set(WEAPON_X + weapon_w/2, WEAPON_Y + weapon_h/2)
	x, y = pygame.mouse.get_pos()
	mouse_vector_position.set(x, y)
	#pygame.draw.line(window, (0, 0, 0), (weapon_vector_position.x, weapon_vector_position.y), (mouse_vector_position.x, mouse_vector_position.y))
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

def projectile_position(x, y, w_x, w_y, w_w, w_h):
	magnitude = 60
	vector = PVector(x, -y)
	vector.normalize()
	vector.multiplication(magnitude)
	vector.add_scalar(w_x+w_w/2, w_y +w_h/2)
	return vector.x, vector.y

def get_time_ms():
	return fpsClock.get_time()

def weapon_and_projectile_update(degree, weapon_controller, projectile_controller):
	weapon_w, weapon_h = weapon_controller.Get_size()
	projectile_new_x, projectile_new_y = get_shoot_components(degree)
	weapon_x, weapon_y = weapon_controller.Get_position()
	projectile_new_x, projectile_new_y = \
		projectile_position(projectile_new_x, projectile_new_y, weapon_x, weapon_y, weapon_w, weapon_h)

	weapon_controller.Update_view(degree)
	projectile_controller.Set_position(projectile_new_x, projectile_new_y)

def events ():
	for event in pygame.event.get():
		if (event.type == QUIT):
			pygame.quit()
			sys.exit()
		elif(event.type == pygame.KEYDOWN):
			if(event.key == pygame.K_o):
				global change_state_flag
				change_state_flag = True
				pass
			elif (event.key == pygame.K_p):
				pass

def background():
	window.fill((BACKGROUND_COLOR))
	#points = [(0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT)]
	#pygame.draw.polygon(window, (0, 0, 0), points, 3)

def text(txt,x,y, textColor = (0, 0, 0)):
	font = pygame.font.Font("C:/Windows/Fonts/COOPBL.TTF",14)
	text = font.render(txt, True, textColor)
	window.blit(text, (x, y))

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

	referee_model = world.rules(projectile_controller, world_controller, WIDTH, HEIGHT)
	referee_view = world.rules_view()
	referee_controller = world.rules_controller(referee_model, referee_view)

	weapon_model = weapon.weapon(50, 400, window)
	weapon_view = weapon.weapon_view()
	weapon_controller = weapon.weapon_controller(weapon_model, weapon_view)

	weapon_bar = weapon.weapon_bar(10, HEIGHT + 10, window)
	weapon_bar_view = weapon.weapon_bar_view()
	weapon_bar_controller = weapon.weapon_bar_controller(weapon_bar, weapon_bar_view)

	target_model = world.target(500, HEIGHT - 35, 10, window)
	target_view = world.target_view()
	target_controller = world.target_controller(target_model, target_view)

	player_model = ia_player.player()
	player_view = ia_player.player_view()
	player_controller = ia_player.player_controller(player_model, player_view)

	actual_state = AIMING_IA_STATE
	IA_mode = True if (actual_state == AIMING_IA_STATE) else False

	shoot_x = 0
	shoot_y = 0
	degree = 0

	global change_state_flag
	global holding_up_ball_flag

	status_bar = False
	actual_time = 0

	explosion_delay = 1000
	magnitude = 0
	shoot_x = 0
	shoot_Y = 0

	while(True):		

		background()

		target_controller.Update_view()

		if(not holding_up_ball_flag):
			projectile_controller.Update_model()

		projectile_controller.Update_view()

		world_controller.Update_view()

		referee_controller.Check_edges()

		weapon_bar_controller.Update_view()

		weapon_bar_controller.Update_bar(status_bar)

		fps = np.floor(fpsClock.get_fps())

		text("FPS: {}".format(fps), 400, HEIGHT + 10)

		text("Wind: no", 10, HEIGHT + 40)

		shoot_angle = np.floor(degree)

		text("angle: {}".format(shoot_angle), 400, HEIGHT + 25)

		#state machine
		if(actual_state == AIMING_IA_STATE):
			target_x, target_y = target_controller.Get_pos()
			degree, magnitude = player_controller.Get_predictions(target_x, target_y)			
			degree = limit_degrees(degree)
			weapon_and_projectile_update(degree, weapon_controller, projectile_controller)

			shoot_x, shoot_y = get_shoot_components(degree)

			force = shoot_force(shoot_x, -shoot_y, magnitude)
			projectile_controller.Apply_force(force)
			holding_up_ball_flag = False

			actual_state = EXPLOSION_STATE

			print("degrees and force: {}, {}".format(degree, magnitude))

		if(actual_state == AIMING_STATE):
			#set new position of the weapon
			weapon_w, weapon_h = weapon_controller.Get_size()
			degree = get_degrees(weapon_w, weapon_h)
			degree = limit_degrees(degree)
			weapon_and_projectile_update(degree, weapon_controller, projectile_controller)

			if(change_state_flag):
				change_state_flag = False
				shoot_x, shoot_y = get_shoot_components(degree)
				actual_state = SHOOT_STATE
				status_bar = True
				print("change state")

		elif(actual_state == SHOOT_STATE):
			
			weapon_controller.Update_view(degree)
			
			if(change_state_flag):
				magnitude = weapon_bar_controller.Get_magnitude()
				#negativo porque la y crece hacia abajo, y el angulo
				#esta hacia arriba
				force = shoot_force(shoot_x, -shoot_y, magnitude)
				projectile_controller.Apply_force(force)
				change_state_flag = False
				actual_state = EXPLOSION_STATE
				status_bar =  False
				holding_up_ball_flag = False
				#print("componenetes de la fuerza: {}, {}".format(force.x, force.y))
				#print(magnitude)
				print("change state")
		
		elif(actual_state == EXPLOSION_STATE):
			weapon_controller.Update_view(degree)

			actual_time += get_time_ms()

			projectile_controller.Set_time(actual_time)

			if(actual_time > explosion_delay):
				#obtenemos el daño si es que hay
				target_x, target_y = target_controller.Get_pos()
				damage = projectile_controller.Get_damage(target_x, target_y)
				print(damage)
				target_controller.Update_HP(damage)
				projectile_controller.Set_explosion()
				actual_state = POST_EXPLOSION_STATE

		elif(actual_state == POST_EXPLOSION_STATE):
			weapon_controller.Update_view(degree)

			if(change_state_flag or IA_mode):
				change_state_flag = False
				projectile_controller.Reset()
				weapon_bar_controller.Reset()
				target_controller.Reset()
				actual_state = AIMING_IA_STATE if (IA_mode) else AIMING_STATE
				holding_up_ball_flag = True
				actual_time = 0
				print("change state")
		
		#p_x, p_y = pygame.mouse.get_pos()
		#print(projectile_controller.Get_damage(p_x, p_y))

		events()

		update_surface_task()

if(__name__ == "__main__"):
	main()