import numpy as np
import ann

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

		return degrees, force

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

