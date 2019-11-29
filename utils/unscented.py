import numpy as np
import math
import copy

class Unscented:
	"""
	Clase que contiene los métodos que la extensión Unscented del
	filtro de Kalman requiere
	"""
	def __init__(self):
		print("=== Filtro de Kalman Unscented ===")
	
	def obtener_puntos_sigma(self, X0, Px):
		"""
		Calcular los puntos sigma dada una matriz X y una matriz de covarianza.

		Parameters:
		X0 (list): Estado en el tiempo t
		Px (list): Vector de covarianzas

		Returns:
		Media de los puntos sigma
		"""
		matriz_sigmas = copy.deepcopy(X0)
		for index, x in enumerate(X0[0]):
			_sigma = Px[index][index]
			punto_sigma = x + math.sqrt(_sigma)
			if(index%2 == 0):
				# X
				try:
					matriz_sigmas.append([punto_sigma, X0[0][index+1]])
				except Exception as e:
					print(e)
					pass
			else:
				# Y
				try:
					matriz_sigmas.append([X0[0][index-1], punto_sigma])
				except Exception as e:
					print(e)
					pass

		for index, x in enumerate(X0[0]):
			_sigma = Px[index][index]
			punto_sigma = x - math.sqrt(_sigma)
			if(index%2 == 0):
				# X
				try:
					matriz_sigmas.append([punto_sigma, X0[0][index+1]])
				except Exception as e:
					print(e)
					pass
			else:
				# Y
				try:
					matriz_sigmas.append([X0[0][index-1], punto_sigma])
				except Exception as e:
					print(e)
					pass
		
		"""
		Una vez que se obtienen los puntos sigma, se procede
		a calcular S(x), donde S(x) =
		[ atan(x/y) ]  -------------> Ángulo
		[ raiz(X^2 + Y^2) ] --------> Distancia
		"""
		angulos_s = []
		distancias_s = []

		for index, punto_sigma in enumerate(matriz_sigmas):
			_x = punto_sigma[0]
			_y = punto_sigma[1]
			angulo = math.degrees(math.atan(_x/_y))
			angulos_s.append(angulo)
			distancia = math.sqrt((math.pow(_x, 2) + math.pow(_y, 2)))
			distancias_s.append(distancia)
		
		"""
		Finalmente se calcula la media del vector S(x)
		"""
		_media_angulos = 0
		_media_distancias = 0

		for angulo in angulos_s:
			_media_angulos += angulo
		print(f'Media angulos = {_media_angulos}')
		print(f'Length Media angulos = {len(angulos_s)}')
		_media_angulos = _media_angulos/len(angulos_s)

		for distancia in distancias_s:
			_media_distancias += distancia
		print(f'Media distancias = {_media_distancias}')
		print(f'Length Media distancias = {len(distancias_s)}')
		_media_distancias = _media_distancias/len(distancias_s)
		return [_media_angulos, _media_distancias]