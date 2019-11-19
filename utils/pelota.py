from tabulate import tabulate
import numpy as np
import pygame
import time
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)


class Pelota(pygame.sprite.Sprite):
    def __init__(self, x, y, vx, vy, delta_t, sigma_p, sigma_v, color, width, height):
        """
        Pintar la pelota
        """
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        # self.image.set_colorkey(BLACK)
        # self.rect = pygame.draw.rect(self.image, WHITE, [x, y, width, height])
        pygame.draw.rect(self.image, WHITE, [x, y, width, height])
        # pygame.draw.rect(self.image, WHITE, [x, y, width, height])
        self.velocity = [vx, vy]
        self.rect = self.image.get_rect()

        """
		Inicializar algoritmo de la real
		"""
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.sigma_p = sigma_p
        self.sigma_v = sigma_v
        self.sigma_x = np.array(
            [
                [np.random.normal(0, sigma_p)],
                [np.random.normal(0, sigma_p)],
                [np.random.normal(0, sigma_v)],
                [np.random.normal(0, sigma_v)]
            ]
        )
        self.Q = np.array(
            [
                [sigma_p, 0, 0, 0],
                [0, sigma_p, 0, 0],
                [0, 0, sigma_p, 0],
                [0, 0, 0, sigma_p]
            ]
        )
        self.W = np.array(
            [
                [np.random.normal(0, sigma_p)],
                [np.random.normal(0, sigma_p)],
                [np.random.normal(0, sigma_v)],
                [np.random.normal(0, sigma_v)]
            ]
        )
        self.Xt = np.array(
            [
                [x],
                [y],
                [vx],
                [vy]
            ]
        )
        self.F = np.array(
            [
                [1, 0, delta_t, 0],
                [0, 1, 0, delta_t],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ]
        )
        self.G = np.array(
            [
                [0],
                [0],
                [0],
                [0]
            ]
        )

        self.iteracion = 1

    def choca_con(self, sprite):
        return self.image.get_rect().colliderect(sprite.rect)

    def rebote(self):
        print('rebote')

    def pretty_print(self, matrix):
        headers = ['x', 'y', 'Vx', 'Vy']
        table = tabulate(np.transpose(matrix), headers, tablefmt="fancy_grid")
        print(table)

    def calcular_Xt(self, jugador):
        W = np.array(
            [
                [np.random.normal(0, self.sigma_p)],
                [np.random.normal(0, self.sigma_p)],
                [np.random.normal(0, self.sigma_v)],
                [np.random.normal(0, self.sigma_v)]
            ]
        )
        self.G = np.array(
            [
                [0],
                [0],
                [0],
                [0]
            ]
        )
        if self.rect.x >= 590:
            self.G = np.array(
                [
                    [0],
                    [0],
                    [-self.vx],
                    [0]
                ]
            )
        elif self.rect.x <= 0:
            self.G = np.array(
                [
                    [0],
                    [0],
                    [self.vx],
                    [0]
                ]
            )
        if self.rect.y >= 790:
            self.G = np.array(
                [
                    [0],
                    [0],
                    [0],
                    [-self.vy]
                ]
            )
        elif self.rect.y <= 0:
            self.G = np.array(
                [
                    [0],
                    [0],
                    [0],
                    [self.vy]
                ]
            )
        self.Xt = np.dot(self.F, self.Xt) + self.G + W
        # self.Xt = (self.F @ self.Xt) + self.G + W
        # self.pretty_print(W)
        # self.pretty_print(self.Xt)
        self.iteracion += 1
        return self.Xt
