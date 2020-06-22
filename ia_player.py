import numpy as np
import ann
import AG
import pandas as pd
#############
# Model
#############
class player(object):
	def __init__(self):
		inputs = 2
		hidden = 4
		outputs = 2
		self.nn = ann.neuronal_network_regression(inputs, hidden, outputs)
	def Set_brain(self, W):
		self.nn.set_weights_and_bias(W)
	def Get_brain(self):
		return self.nn.get_weights_and_bias()
	def Predict(self, target_x, target_y):
		p = self.nn.predict([target_x, target_y])

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

	def Population_duty(self):
		degrees_matrix = []
		force_matriz = []

		for i in range(self.population):
			degree, force = self.Get_predictions()
			degrees_matrix.append(degree)
			force_matriz.append(force)

		return degrees_matrix, force_matriz

	def Set_population_fitness(self, target_x, target_y, source_x, source_y, index):
		target = PVector(target_x, target_y)
		source = PVector(source_x, source_y)
		distance = source - target
		fit = distance.mag()
		self.fitness[index] = fit
	def Make_new_generation(self):
		data = {'cromosomas': self.players.Get_brain(), 'fitness': self.fitness}

		dataframe = pd.DataFrame(data)
		print(dataframe)




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
	def Get_predictions(self, target_x, target_y):
		return self.model.Predict(target_x, target_y)

