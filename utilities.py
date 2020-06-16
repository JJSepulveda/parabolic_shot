import numpy as np

class PVector(object):
	"""
	Crea a un objeto para manipular vectores.

	Parametros
	----------
	x: componente x del vector
	y: componente y del vector

	Retorna
	----------
	Retorna un objeto vector.

	"""
	def __init__(self,x,y):
		self.x = float(x)
		self.y = float(y)
		pass

	def set(self,x,y):
		"""
		Metodo para reasignar las componentes del vector

		Parametros
		----------
		x: componente x del vector
		y: componente y del vector

		Retorna
		----------
		N/A

		"""
		self.x = x
		self.y = y
	
	def mag(self):
		"""
		Metodo para calcular la magnitud del vector

		Parametros
		----------
		usa los valores previamente asignados con set, o cuando se inicializo.

		Retorna
		----------
		float

		"""
		magnitude = (self.x**2 + self.y**2)**0.5

		return magnitude

	def add(self, vector2):
		"""
		Suma los valores de otro vector a las componentes del 
		objeto vector actual.

		Parametros
		----------
		vector2: otro objeto vector

		Retorna
		----------
		N/A

		"""
		self.x += vector2.x
		self.y += vector2.y

	def substract(self, vector2):
		self.x -= vector2.x
		self.y -= vector2.y

	def div(self, d):
		self.x /= d
		self.y /= d

	def multiplication(self, mult):
		self.x *= mult
		self.y *= mult

	def normalize(self):
		magnitude = self.mag()
		self.div(magnitude)

	def limit(self, lim):
		"""
		En caso de superar el limite el vector se iguala al limite meximo establecido.
		Este metodo se tiene que llamar cada vez que se quiera limitar el vector.

		Parametros
		----------
		lim: limite en magnitud al cual el vector puee llegar.

		Retorna
		-----------
		N/A
		"""
		magnitude = self.mag()
		if(magnitude > lim):
			self.normalize()
			self.multiplication(lim)
	def Get_components(self):
		return self.x, self.y
