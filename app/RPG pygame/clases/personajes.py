import pygame

class personajes():
    def __init__(self, x, y):
        self.forma = pygame.Rect(0, 0, 20, 20)
        self.forma.center = (x, y)

        def dibujar(self, interfaz):
            pygame.draw.rect(interfaz, (255, 0, 0), self.forma)