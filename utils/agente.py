from numpy.linalg import inv  # Inversa
from tabulate import tabulate
import numpy as np
import pygame

BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Jugador(pygame.sprite.Sprite):
	def __init__(self, color, width, height, sigma_P, sigma_V):
		"""
		Inicializar el Sprite para pintar al jugador.
		"""
		super().__init__()
		self.image = pygame.Surface([width, height])
		self.image.fill(BLACK)
		self.image.set_colorkey(BLACK)
		pygame.draw.rect(self.image, color, [0, 0, width, height])
		self.rect = self.image.get_rect()

		"""
		Inicializar algoritmo de la predicción
		"""
		self.H = np.array(
			[
				[1, 0, 0, 0],
				[0, 1, 0, 0]
			]
		)
		self.I = np.array(
			[
				[1, 0, 0, 0],
				[0, 1, 0, 0],
				[0, 0, 1, 0],
				[0, 0, 0, 1]
			]
		)  # Matriz de identidad
		self.Q = np.array(
			[
				[sigma_P, 0, 0, 0],
				[0, sigma_P, 0, 0],
				[0, 0, sigma_V, 0],
				[0, 0, 0, sigma_V]
			]
		)

		self.P = np.array(
			[
				[sigma_P, 0, 0, 0],
				[0, sigma_P, 0, 0],
				[0, 0, sigma_V, 0],
				[0, 0, 0, sigma_V]
			]
		)

		self.Xt_dado_t_menos_1 = None

	def pretty_print(self, matrix, header='Vector'):
		headers = [header]
		table = tabulate(matrix, headers, tablefmt="fancy_grid")
		print(table)
		print('\n\n')
	
	def predecir_movimiento(self, sigma_p, sigma_v, F, Xt):
		V0 = np.array(
			[
				[np.random.normal(0, sigma_p)],  # X
				[np.random.normal(0, sigma_p)]  # Y
			]
		)
		V1 = np.array(
			[
				[np.random.normal(0, sigma_p)],  # X
				[np.random.normal(0, sigma_p)]  # Y
			]
		)

		Gz = np.array(
			[
				[np.random.normal(0, sigma_p)],
				[np.random.normal(0, sigma_p)]
			]
		)
		R = np.dot(Gz, np.transpose(Gz))

		# Observación
		# Zt = H * Xt + V
		Zt0 = np.dot(self.H, Xt) + V0
		Zt1 = np.dot(self.H, Xt) + V1


		"""
		t | t-1 SIGNIFICA => Predicción o predicha
		t | t   SIGNIFICA => Estimada
		"""

		Wt = np.array(
			[
				[np.random.normal(0, sigma_p)],
				[np.random.normal(0, sigma_p)],
				[np.random.normal(0, sigma_v)],
				[np.random.normal(0, sigma_v)]
			]
		)
		"""
		X estimada
		X t|t = [
					[ Zt1.x ],
					[ Zt1.y ],
					[ Zt1.x - Zt0.x / delta_t ],
					[ Zt1.y - Zt0.y / delta_t ],
				] + Wt
		"""
		X_estimada = np.array(
			[
				[ Zt1[0][0] ]
			]
		)
		self.pretty_print(Zt0, header='Z[0]')
		self.pretty_print(Zt1, header='Z[1]')
		return 0, 0 # X, Y
