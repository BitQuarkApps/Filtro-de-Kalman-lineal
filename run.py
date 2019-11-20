# Diseño de Sistemas Inteligentes
# Corte 2
# Universidad Politécnica de Chiapas
# Creado por Luis Fernando Hernández Morales
from utils.agente import Jugador
from utils.pelota import Pelota
import matplotlib.pyplot as plt
import numpy as np
import pygame
import time


"""
Variables para pygame
"""
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
(width, height) = (600, 800)  # Dimensiones de la ventana de pygame
running = True

"""
Arreglos para las graficas
"""
REAL_X = []
REAL_Y = []
PREDICHA_X = []
PREDICHA_Y = []

if __name__ == "__main__":

    x = 20
    y = 200

    vx = 1
    vy = 1

    delta_t = 1
    sigma_posicion = 0.08
    sigma_velocidad = 0.05

    jugador1 = Jugador(WHITE, 10, 20, sigma_posicion, sigma_velocidad)
    jugador2 = Jugador(WHITE, 10, 20, sigma_posicion, sigma_velocidad)
    pelota = Pelota(x, y, vx, vy, delta_t, sigma_posicion,
                    sigma_velocidad, WHITE, 10, 10)

    """
	Iniciar animaciones
	"""
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Filtro de Kalman")
    clock = pygame.time.Clock()

    jugador1.rect.x = 20
    jugador1.rect.y = 220

    jugador2.rect.x = 590
    jugador2.rect.y = 200

    all_sprites_list = pygame.sprite.Group()

    all_sprites_list.add(jugador1)
    all_sprites_list.add(jugador2)
    all_sprites_list.add(pelota)

    """
	Loop de pygame para pintar la pelota
	"""
    iteraciones = 0
    turno_jugador_1 = True
    while running:
        ev = pygame.event.get()
        # Controlar cuando cierren la ventana
        for event in ev:
            if event.type == pygame.QUIT:
                running = False

        # Actualizar la ventana
        # all_sprites_list.update()

        # Calcular Xt
        if turno_jugador_1:
            xt_pelota = pelota.calcular_Xt(jugador2)
        else:
            xt_pelota = pelota.calcular_Xt(jugador1)
        pelota.rect.x += xt_pelota[2][0]
        pelota.rect.y += xt_pelota[3][0]

        REAL_X.append(xt_pelota[0][0])
        REAL_Y.append(xt_pelota[1][0])

        # 60 FPS
        clock.tick(60)
        """
		Cuando el jugador 1 tira, el jugador 2 predice

		Agregar lógica del rebote
		"""
        if turno_jugador_1:
            x, y = jugador2.predecir_movimiento(
                sigma_posicion, sigma_velocidad, pelota.F, xt_pelota
            )
            jugador2.rect.y = y

            PREDICHA_X.append(x)
            PREDICHA_Y.append(y)
        else:
            x, y = jugador1.predecir_movimiento(
                sigma_posicion, sigma_velocidad, pelota.F, xt_pelota
            )
            jugador1.rect.y = y
        if turno_jugador_1:
            if pelota.choca_con(jugador2):
                print('Chocaaaa con 2')
                turno_jugador_1 = not turno_jugador_1
        else:
            if pelota.choca_con(jugador1):
                print('Chocaaaa con 1')
                turno_jugador_1 = not turno_jugador_1
        iteraciones += 1
        # screen.fill(BLACK)
        # all_sprites_list.draw(screen)
        # pygame.display.flip()

    # Salir cuando todo termine
    """
	pintar las graficas
	"""
    plt.plot(REAL_X, REAL_Y, "-", label="Real")
    plt.plot(PREDICHA_X, PREDICHA_Y, ":", label="Predicha")
    plt.title('Filtro de Kalman lineal')
    plt.legend()
    plt.show()
    pygame.quit()
