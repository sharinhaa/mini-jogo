import pygame
import random
from config import *

class jogador (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(amarelo_carro)

        pygame.draw.rect(self.image, (0, 0, 0), (16, 0, 8, 60))

        self.rect == self.image.get_rect()
        self.rect.centerx = largura_tela // 2
        self.rect.bottom = altura_tela - 20

        self.velocidade = 7
        self.vidas = 3
        self.cooldown_tiro = 300
        self.ultimo_tiro = pygame.time.get_ticks()

    def update(self. todos_sprites, projeteis):
        teclas = pygame.key.get_pressed()

#movimentação lateral travada dentro da pista
        if teclas[pygame.K_LEFT] and self.rect.left > 150:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] and self.rect.right < largura_tela - 150:
            self.rect.x += self.velocidade

        if teclas[pygame.K_SPACE]:
            self.atirar(todos_sprites, projeteis)

    def atirar(self, todos_sprites, projeteis):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro >= self.cooldown_tiro:
            self.ultimo_tiro = agora
            #disparo vindo das laterais do carro
            projatil_esq = Projatil(self.rect.left, self.rect.top)
            projatil_dir = Projatil(self.rect.right - 6, self.rect.top)
            todos_sprites.add(projatil_esq, projatil_dir)
            projeteis.add(projatil_esq, projatil_dir)

    def CarroInimigo(pygame.sprite.Sprite):
        def __init__(self, velocidade_base):
            super().__init__()
            self.image = pygame.Surface((40, 60))

            #sorteia exclusivamente entre vermelho, verde e azul
            cor = random.choice([verde_carro, vermelho_carro, azul_carro])
            self.image.fill(cor)

            self.rect = self.image.rect()
            self.rect.x = random.randint(160, largura_tela - 200)
            self.rect.y = random.randint(-100, -40)
            self.velocidade = self.velocidade_base + random.randint(1, 2)

        def update(self):
            self.rect.y += self.velocidade 
            if self.rect.top > altura_tela:
                self.kill()

class ObstaculoBomba(pygame.sprite.Sprite):
    def __init__(self, velocidade_base):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(vermelho_carro)
        pygame.draw.rect(self.image, (0, 0, 0), (5, 10, 20, 10)) #relogio digital 

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(160, largura_tela - 190)
        self.rect.y = random.randint(-80, -30)
        self.velocidade = velocidade_base

    def update(self):
        self.rect.y += self.velocidade 
        if self.rect.top > altura_tela:
            self.kill()

class CaixaMadeira(pygame.sprite.Sprite):
    def __init__(self, velocidade_base):
        super().__init__()
        self.image = pygame.Surface((35, 35))
        self.image.fill(castanho_caixa)
        pygame.draw.rect(self.image, (60, 30, 10), (0, 0, 35, 35), 3)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(160, largura_tela - 195)
        self.rect.y = random.randint(-100, -40)
        self.velocidade = velocidade_base

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > altura_tela:
            self.kill

