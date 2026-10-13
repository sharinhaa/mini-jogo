import pygame
import random
import math
from config import LARGURA_TELA, ALTURA_TELA, AMARELO_CARRO, VERMELHO_CARRO, CIANO_NEON


class Jogador (pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            img = pygame.image.load("assets/imagens/carro amarelo.png").convert_alpha()
            self.image = pygame.transform.scale(img, (40, 70))
        except Exception:
            self.image = pygame.Surface((40, 70))
            self.image.fill(AMARELO_CARRO)
     

        self.rect = self.image.get_rect()
        self.rect.centerx = LARGURA_TELA // 2
        self.rect.bottom = ALTURA_TELA - 20
        self.velocidade = 6
        self.vidas = 3
    
        self.cooldown_tiro = 250
        self.ultimo_tiro = pygame.time.get_ticks()


    def update(self, todos_sprites, projeteis, som_tiro=None):
        teclas = pygame.key.get_pressed()
#movimentacao lateral travada dentro da pista
        if teclas[pygame.K_LEFT] and self.rect.left > 150:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_RIGHT] and self.rect.right < LARGURA_TELA - 150:
            self.rect.x += self.velocidade

        if teclas[pygame.K_SPACE]:
            self.atirar(todos_sprites, projeteis, som_tiro)


    def atirar(self, todos_sprites, projeteis, som_tiro=None):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro >= self.cooldown_tiro:
            self.ultimo_tiro = agora
            #disparo vindo das laterais do carro
            projatil_esq = Projatil(self.rect.left, self.rect.top)
            projatil_dir = Projatil(self.rect.right - 6, self.rect.top)
            todos_sprites.add(projatil_esq, projatil_dir)
            projeteis.add(projatil_esq, projatil_dir)

            if som_tiro:
                som_tiro.play()

class CarroInimigo(pygame.sprite.Sprite):
        def __init__(self, velocidade_base):
            super().__init__()
            opcoes_carro = ["carro vermelho.png", "Carro azul.png", "carro verde.png"]
            imagem_escolhida = random.choice(opcoes_carro)

            try:
                img = pygame.image.load(f"assets/imagens/{imagem_escolhida}").convert_alpha()
                self.image = pygame.transform.scale(img, (40, 70))
            except Exception:
                self.image = pygame.Surface((40, 70))
                self.image.fill(VERMELHO_CARRO)

            self.rect = self.image.get_rect()
            self.rect.x = random.randint(160, LARGURA_TELA - 200)
            self.rect.y = random.randint(-150, -70)
            self.velocidade_y = velocidade_base + random.uniform(0.5, 2.0)

            #movimento em zig-zag
            self.faz_zig_zag = random.random() < 0.35
            self.angulo = random.uniform(0, 360)

        def update(self):
            self.rect.y += self.velocidade_y

            if self.faz_zig_zag:
                self.angulo += 0.08
                self.rect.x += math.sin(self.angulo) * 2.5
                self.rect.x = max(155, min(LARGURA_TELA - 195, self.rect.x))

            if self.rect.top > ALTURA_TELA:
                self.kill()

class ObstaculoBomba(pygame.sprite.Sprite):
    def __init__(self, velocidade_base):
        super().__init__()
        try:
            img = pygame.image.load("assets/imagens/tnt_minijogo.png").convert_alpha()
            self.image = pygame.transform.scale(img, (35, 35))
        except Exception:
            self.image = pygame.Surface((35, 35))
            self.image.fill(VERMELHO_CARRO)

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(160, LARGURA_TELA - 195)
        self.rect.y = random.randint(-100, -40)
        self.velocidade = velocidade_base

    def update(self):
        self.rect.y += self.velocidade 
        if self.rect.top > ALTURA_TELA:
            self.kill()

class CaixaMadeira(pygame.sprite.Sprite):
    def __init__(self, velocidade_base):
        super().__init__()
        try:
            img = pygame.image.load("assets/imagens/caixa_suprice.png").convert_alpha()
            self.image = pygame.transform.scale(img, (35, 35))
        except Exception:
            self.image = pygame.Surface((35, 35))
            self.image.fill((139, 69, 19))

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
        self.image = pygame.Surface((6, 16))
        self.image.fill(CIANO_NEON)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.velocidade = -14

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.bottom < 0:
            self.kill()


class ChavedeFenda(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((16, 26))
        self.image.fill((192, 192, 192))
        pygame.draw.rect(self.image, AMARELO_CARRO, (0, 13, 16, 13))
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
        self.image.fill(random.choice([VERMELHO_CARRO, AMARELO_CARRO, (255, 140, 0)]))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        self.vel_x = random.uniform(-4, 4)
        self.vel_y = random.uniform(-4, 4)
        self.tempo_vida = 18  # frames

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.tempo_vida -= 1
        if self.tempo_vida <= 0:
            self.kill()