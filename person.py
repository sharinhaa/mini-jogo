import pygame
import random
from config import AMARELO_CARRO,  VERMELHO_CARRO, VERDE_CARRO, AZUL_CARRO, LARGURA_TELA, ALTURA_TELA, CASTANHO_CAIXA


class Jogador (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(AMARELO_CARRO)

        pygame.draw.rect(self.image, (0, 0, 0), (16, 0, 8, 60))

        self.rect = self.image.get_rect()
        self.rect.centerx = LARGURA_TELA // 2
        self.rect.bottom = ALTURA_TELA - 20

        self.velocidade = 7
        self.vidas = 3
        self.cooldown_tiro = 300
        self.ultimo_tiro = pygame.time.get_ticks()

    def update(self, todos_sprites, projeteis):
        teclas = pygame.key.get_pressed()

#movimentacao lateral travada dentro da pista
        if teclas[pygame.K_LEFT] and self.rect.left > 150:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] and self.rect.right < LARGURA_TELA - 150:
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

class CarroInimigo(pygame.sprite.Sprite):
        def __init__(self, velocidade_base):
            super().__init__()
            self.image = pygame.Surface((40, 60))

            #sorteia exclusivamente entre vermelho, verde e azul
            cor = random.choice([VERDE_CARRO, VERMELHO_CARRO, AZUL_CARRO])
            self.image.fill(cor)

            self.rect = self.image.rect()
            self.rect.x = random.randint(160, LARGURA_TELA - 200)
            self.rect.y = random.randint(-100, -40)
            self.velocidade = self.velocidade_base + random.randint(1, 2)

        def update(self):
            self.rect.y += self.velocidade 
            if self.rect.top > ALTURA_TELA:
                self.kill()

class ObstaculoBomba(pygame.sprite.Sprite):
    def __init__(self, velocidade_base):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(VERMELHO_CARRO)
        pygame.draw.rect(self.image, (0, 0, 0), (5, 10, 20, 10)) #relogio digital 

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(160, LARGURA_TELA - 190)
        self.rect.y = random.randint(-80, -30)
        self.velocidade = velocidade_base

    def update(self):
        self.rect.y += self.velocidade 
        if self.rect.top > ALTURA_TELA:
            self.kill()

class CaixaMadeira(pygame.sprite.Sprite):
    def __init__(self, velocidade_base):
        super().__init__()
        self.image = pygame.Surface((35, 35))
        self.image.fill(CASTANHO_CAIXA)
        pygame.draw.rect(self.image, (60, 30, 10), (0, 0, 35, 35), 3)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(160, LARGURA_TELA - 195)
        self.rect.y = random.randint(-100, -40)
        self.velocidade = velocidade_base

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > ALTURA_TELA:
            self.kill


class Projatil(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((6, 15))
        self.image.fill(AMARELO_CARRO)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.velocidade = -12

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.bottom < 0:
            self.kill()


class ChavedeFenda(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 25))
        self.image.fill((192, 192, 192))
        pygame.draw.rect(self.image, AMARELO_CARRO, (0, 12, 15, 13))

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.velocidade = 3

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > ALTURA_TELA:
            self.kill()



