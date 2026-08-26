import pygame
import random
from config import *

class jogador (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(amarelo_carro)

        