import numpy as np
import ann
import AG
import pandas as pd
from utilities import *
#############
# Model
#############
class player(object):
	def __init__(self, normalize_value = 1):
		inputs = 2
		hidden = 4
		outputs = 2
		self.nn = ann.neuronal_network_regression(inputs, hidden, outputs)
		self.normalize_value = normalize_value
	def Set_brain(self, W):
		self.nn.set_weights_and_bias(W)
	def Get_brain(self):
		return self.nn.get_weights_and_bias()
	def Predict(self, target_x, source_x):
		#falta normalizar las entradas.
		p = self.nn.predict([target_x / self.normalize_value, source_x / self.normalize_value])

		degrees = p[0]
		force = p[1]
		
		if(degrees < 0):
			degrees = 0
		elif(degrees > 90):
			degrees = 90

		if(force < 0):
			force = 0
		elif(force > 360):
			force = 360
		else:
			pass

		return degrees, force

# 1.- crear población.
# 2.- tomar fitenes para cada uno
# 3.- ordenar dado el fitness
class trainer(object):
	def __init__(self, population):
		self.population = population
		self.genetic = AG.AG(population)
		self.players = []
		self.fitness = [0] * self.population
		self.Make_populations()
	def Make_populations(self):
		
		if(len(self.players) >= self.population):
			return

		for i in range(self.population):
			model = player()
			view = player_view()
			controller = player_controller(model, view)
			self.players.append(controller)

		print(self.players[0])

	def Population_duty(self):
		degrees_matrix = []
		force_matriz = []

		for i in range(self.population):
			degree, force = self.Get_predictions()
			degrees_matrix.append(degree)
			force_matriz.append(force)

		return degrees_matrix, force_matriz
	def Get_single(self, index):
		return self.players[index]
	def Set_population_fitness(self, target_x, target_y, source_x, source_y, index):
		target = PVector(target_x, target_y)
		source = PVector(source_x, source_y)
		distance = source - target
		fit = distance.mag()
		self.fitness[index] = fit
	def Get_population_fitness(self):
		return self.fitness
	def Make_new_generation(self):
		brain_values = []
		for i in range(self.population):
			brain_values.append(self.players[i].Get_brain())
		
		data = {'cromosomas': brain_values , 'fitness': self.fitness}

		dataframe = pd.DataFrame(data)
		dataframe = dataframe.sort_values('fitness')
		print(dataframe['fitness'])
		cromosomas = dataframe['cromosomas'].values
		# print(len(cromosomas))
		# print(type(cromosomas))
		# print(cromosomas[0])

		childs = self.genetic.new_generation(cromosomas)

		# print(len(childs))
		# print(type(childs))
		# print(childs[0])

		for i in range(self.population):
			self.players[i].Set_brain(childs[i])


#############
# View
#############
class player_view(object):
	def __init__(self):
		pass
	def print_status(self):
		pass

#############
# Controller
#############
class player_controller(object):
	def __init__(self, model, view):
		self.model = model
		self.view = view
		pass
	def Get_predictions(self, target_x, source_x):
		return self.model.Predict(target_x, source_x)
	def Get_brain(self):
		return self.model.Get_brain()
	def Set_brain(self, brain):
		self.model.Set_brain(brain)