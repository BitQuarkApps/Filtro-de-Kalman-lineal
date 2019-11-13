from numpy.linalg import inv  # Inversa
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

	def predecir_movimiento(self, sigma_p, sigma_v, F, Xt):
		V = np.array(
			[
				[np.random.normal(0, sigma_v)],  # X
				[np.random.normal(0, sigma_v)]  # Y
			]
		)

		Gz = np.array(
			[
				[np.random.normal(0, sigma_p)],
				[np.random.normal(0, sigma_p)]
			]
		)
		R = np.dot(Gz, np.transpose(Gz))

		# Predicción
		# X t|0 = F * X 0|0
		if self.Xt_dado_t_menos_1 is None:
			self.Xt_dado_t_menos_1 = Xt
		predicha = np.dot(F, self.Xt_dado_t_menos_1)
		# Observación
		# Zt = H * Xt + V
		Z = np.dot(self.H, self.Xt_dado_t_menos_1) + V  # XZ

		# Confiabilidad
		# P t|0 = F * P 0|0 + F^t + Q
		confiabilidad = np.dot(F, np.dot(self.P, np.transpose(F))) + self.Q

		# Observación predicha
		# Fórmula de la ganancia K
		K = confiabilidad @ np.transpose(self.H) @ inv(
			self.H @ confiabilidad @ np.transpose(self.H) + R)

		# Cálculo de la innovación Y
		Y = Z - np.dot(self.H, predicha)
		# Filtrada
		# X t|t = X t|t-1 + K * Yt
		filtrada = predicha + np.dot(K, Y)
		Pt_t = np.dot(
			confiabilidad,
			(self.I - np.dot(K, self.H))
		)

		# Actualización
		V_z0 = np.array(
			[
				[np.random.normal(0, sigma_v)],  # X
				[np.random.normal(0, sigma_v)]  # Y
			]
		)
		V_z1 = np.array(
			[
				[np.random.normal(0, sigma_v)],  # X
				[np.random.normal(0, sigma_v)]  # Y
			]
		)
		z0 = np.dot(self.H, Xt) + V_z0  # Z0
		z1 = np.dot(self.H, Xt) + V_z1  # Z1
		wt = np.array(
			[
				[np.random.normal(0, sigma_p)],
				[np.random.normal(0, sigma_p)],
				[np.random.normal(0, sigma_v)],
				[np.random.normal(0, sigma_v)]
			]
		)
		self.Xt_dado_t_menos_1 = np.array(
			[
				[z1[0][0]],
				[z1[1][0]],
				[(z1[0][0]-z0[0][0])/1],
				[(z1[1][0]-z0[1][0])/1],
			]
		) + wt
		return filtrada[0][0], filtrada[1][0]
