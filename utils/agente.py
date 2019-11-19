from numpy.linalg import inv  # Inversa
from tabulate import tabulate
import numpy as np
import pygame
import copy
import math

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

        self.delta_t = 1
        self.sigma_p = sigma_P
        self.sigma_v = sigma_V

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

        # Variables para el algoritmo, como son las iniciales serán None
        # P t|t es igual a Q en la 1ra iteración [ Estimada ]
        self.Pt_t = self.Q
        self.Pt_t_menos_1 = None  # Para la 2da iteración, será P t-1|t-1
        self.Xt_t = None  # Para la 2da iteración, se convierte en x t|t-1
        self.Xt_t_menos_1 = None  # Para la 2da iteración se convierte en Xt-1|t-1
        self.Zt_t_menos_1 = None

    def pretty_print(self, matrix, header=['Vector']):
        """
        Mostrar una tabla en la terminal
        """
        headers = header
        table = tabulate(matrix, headers, tablefmt="fancy_grid")
        print(table)
        print('\n\n')

    def predecir_movimiento(self, sigma_p, sigma_v, F, Xt):
        # print("XT")
        # self.pretty_print(Xt, header=['X', 'Y', 'Vx', 'Vy'])
        # print('--------------------------------------------')
        # print('Xt | t')
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

        Zt0 = np.dot(self.H, Xt) + V0
        Zt1 = np.dot(self.H, Xt) + V1
        """
		t | t-1 SIGNIFICA => Predicción o predicha
		t | t   SIGNIFICA => Estimada
		"""

        # self.Pt_t_menos_1 = None  # Para la 2da iteración, será P t-1|t-1
        # self.Xt_t = None  # Para la 2da iteración, se convierte en x t|t-1
        # self.Xt_t_menos_1 = None  # Para la 2da iteración se convierte en Xt-1|t-1

        if self.Xt_t_menos_1 is None:
            Wt = np.array([
                [np.random.normal(0, sigma_p)],
                [np.random.normal(0, sigma_p)],
                [np.random.normal(0, sigma_v)],
                [np.random.normal(0, sigma_v)]
            ])
            x0 = np.array([
                [Zt1[0][0]],
                [Zt1[1][0]],
                [(Zt1[0][0] - Zt0[0][0])/self.delta_t],
                [(Zt1[1][0] - Zt0[1][0])/self.delta_t]]) + Wt
            # X t | t-1 = F * Xt-1|t-1
            self.Xt_t_menos_1 = np.dot(F, x0)
        else:
            # X t|t-1 = F * X t-1|t-1
            self.Xt_t_menos_1 = np.dot(F, self.Xt_t_menos_1)

        if self.Pt_t_menos_1 is None:
            self.Pt_t_menos_1 = np.dot(
                F, np.dot(self.P, np.transpose(F))) + self.Q
        else:
            self.Pt_t_menos_1 = np.dot(
                F, np.dot(self.Pt_t, np.transpose(F))) + self.Q

        # Observación
        # Zt = H * Xt + V
        self.Zt = np.dot(self.H, Xt) + V0
        self.Zt_t_menos_1 = np.dot(self.H, self.Xt_t_menos_1)
        Yt = self.Zt - self.Zt_t_menos_1
        K = (self.Pt_t_menos_1 @ np.transpose(self.H)) @ inv(
            self.H @ self.Pt_t_menos_1 @ np.transpose(self.H) + R)
        self.Xt_t = self.Xt_t_menos_1 + np.dot(K, Yt)
        self.Pt_t = np.dot(
            self.I - np.dot(K, self.H),
            self.Pt_t_menos_1
        )
        # self.pretty_print(self.Pt_t)

        # Fórmula de la pendiente
        Y2 = self.Xt_t[1][0]
        Y1 = self.Xt_t_menos_1[1][0]

        X2 = self.Xt_t[0][0]
        X1 = self.Xt_t_menos_1[0][0]

        print('Pendiente:')
        print(Y2)
        print(Y1)
        print(X2)
        print(X1)

        pendiente = (Y2-Y1)/(X2-X1)
        print('Resultado:')
        print(pendiente)
        angulo_inclinacion = math.degrees(math.atan(pendiente))
        print('Angulo:')
        print(angulo_inclinacion)
        # Si `pendiente` es > 0 quiere decir que el vector va hacia arriba
        # Si `pendiente` es < 0 quiere decir que el vector va hacia abajo
        return self.Xt_t[0][0], self.Xt_t[1][0]
