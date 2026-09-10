import pygame
import random
import math
from config import AMARELO_CARRO,  VERMELHO_CARRO, VERDE_CARRO, AZUL_CARRO, LARGURA_TELA, ALTURA_TELA, CASTANHO_CAIXA, COR_ESCUDO, AMARELO_FAISCA


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
        self.cooldown_tiro = 250
        self.ultimo_tiro = pygame.time.get_ticks()

        self.escudo_ativo = False
        self.tempo_escudo = 0
        self.duracao_escudo = 5000

    def ativar_escudo(self):
        self.escudo_ativo = True
        self.tempo_escudo = pygame.time.get_ticks()

    def update(self, todos_sprites, projeteis):
        agora = pygame.time.get_ticks()

        #atualiza o estado do escudo 
        if self.escudo_ativo:
            if agora - self.tempo_escudo > self.duracao_escudo:
                self.escudo_ativo = False
                self.image = self.image_base.copy()
            else:
                self.imgae = self.image_base.copy()
                pygame.draw.rect(self.image, COR_ESCUDO, (0, 0, 40, 60), 4)


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

            self.rect = self.image.get_rect()
            self.rect.x = random.randint(160, LARGURA_TELA - 200)
            self.rect.y = random.randint(-100, -40)
            self.velocidade_y = velocidade_base + random.uniform(0.5, 2.0)
            #movimento em zig-zag
            self.faz_zig_zag = random.random() < 0.30
            self.angulo = 0

        def update(self):
            self.rect.y += self.velocidade_y

            if self.faz_zig_zag:
                self.angulo += 0.08
                self.rect.x += math.sin(self.angulo) * 2
                self.rect.x = max(155, min(LARGURA_TELA - 195, self.rect.x))

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
            self.kill()


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

            
class ParticulaExplosao(pygame.sprite.Sprite):
    """ Efeito visual de explosão ao destruir alvos """
    def __init__(self, x, y):
        super().__init__()
        tamanho = random.randint(4, 8)
        self.image = pygame.Surface((tamanho, tamanho))
        self.image.fill(random.choice([VERMELHO_CARRO, AMARELO_FAISCA, (255, 140, 0)]))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        self.vel_x = random.uniform(-4, 4)
        self.vel_y = random.uniform(-4, 4)
        self.tempo_vida = 20  # frames

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.tempo_vida -= 1
        if self.tempo_vida <= 0:
            self.kill()