import pygame
import random
import math

from config import (
    LARGURA_TELA, ALTURA_TELA, 
    PISTA_ESQUERDA, PISTA_DIREITA,
    AMARELO_CARRO, VERMELHO_CARRO, CIANO_NEON
)

def carregar_e_dimensionar_carro(caminho_imagem, largura_desejada=50, cor_fallback=AMARELO_CARRO):
    """Carrega uma imagem e redimensiona mantendo a proporção original para não ficar 'fina'."""
    try:
        img_orig = pygame.image.load(caminho_imagem).convert_alpha()
        largura_orig, altura_orig = img_orig.get_size()
        
        # Mantém a proporção do aspecto (Aspect Ratio)
        proporcao = largura_desejada / float(largura_orig)
        altura_desejada = int(altura_orig * proporcao)
        
        return pygame.transform.scale(img_orig, (largura_desejada, altura_desejada))
    except Exception:
        surface = pygame.Surface((largura_desejada, 80))
        surface.fill(cor_fallback)
        return surface


class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Carrega a imagem ajustando a proporção (largura = 50px)
        self.image = carregar_e_dimensionar_carro("assets/imagens/carro amarelo.png", largura_desejada=50, cor_fallback=AMARELO_CARRO)

        self.rect = self.image.get_rect()
        self.rect.centerx = LARGURA_TELA // 2
        self.rect.bottom = ALTURA_TELA - 20
        self.velocidade = 6
        self.vidas = 3
        
        # Cooldown de disparo (em milissegundos)
        self.cooldown_tiro = 220
        self.ultimo_tiro = pygame.time.get_ticks()

    def update(self, todos_sprites, projeteis, som_tiro=None):
        teclas = pygame.key.get_pressed()
        
        # --- MOVIMENTAÇÃO LATERAL (Esquerda / Direita) ---
        if (teclas[pygame.K_LEFT] or teclas[pygame.K_a]) and self.rect.left > PISTA_ESQUERDA:
            self.rect.x -= self.velocidade
        if (teclas[pygame.K_RIGHT] or teclas[pygame.K_d]) and self.rect.right < PISTA_DIREITA:
            self.rect.x += self.velocidade

        # --- MOVIMENTAÇÃO VERTICAL (Frente / Trás) ---
        if (teclas[pygame.K_UP] or teclas[pygame.K_w]) and self.rect.top > ALTURA_TELA // 3:
            self.rect.y -= self.velocidade
        if (teclas[pygame.K_DOWN] or teclas[pygame.K_s]) and self.rect.bottom < ALTURA_TELA - 10:
            self.rect.y += self.velocidade

        # Disparo
        if teclas[pygame.K_SPACE]:
            self.atirar(todos_sprites, projeteis, som_tiro)

    def atirar(self, todos_sprites, projeteis, som_tiro=None):
        agora = pygame.time.get_ticks()
        if agora - self.ultimo_tiro >= self.cooldown_tiro:
            self.ultimo_tiro = agora
            
            p_esq = Projetil(self.rect.left + 5, self.rect.top)
            p_dir = Projetil(self.rect.right - 11, self.rect.top)
            
            todos_sprites.add(p_esq, p_dir)
            projeteis.add(p_esq, p_dir)
            
            if som_tiro:
                som_tiro.play()


class CarroInimigo(pygame.sprite.Sprite):
    def __init__(self, velocidade_base):
        super().__init__()
        opcoes_carro = ["carro vermelho.png", "Carro azul.png", "carro verde.png"]
        imagem_escolhida = random.choice(opcoes_carro)

        # Carrega com proporção preservada
        self.image = carregar_e_dimensionar_carro(
            f"assets/imagens/{imagem_escolhida}", 
            largura_desejada=50, 
            cor_fallback=VERMELHO_CARRO
        )

        self.rect = self.image.get_rect()
        self.rect.x = random.randint(PISTA_ESQUERDA, PISTA_DIREITA - self.rect.width)
        self.rect.y = random.randint(-150, -70)
        self.velocidade_y = velocidade_base + random.uniform(0.5, 2.0)
        
        self.faz_zig_zag = random.random() < 0.30
        self.angulo = random.uniform(0, 360)

    def update(self):
        self.rect.y += self.velocidade_y

        if self.faz_zig_zag:
            self.angulo += 0.08
            self.rect.x += math.sin(self.angulo) * 2
            self.rect.x = max(PISTA_ESQUERDA, min(PISTA_DIREITA - self.rect.width, self.rect.x))

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
        self.rect.x = random.randint(PISTA_ESQUERDA, PISTA_DIREITA - self.rect.width)
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
        self.rect.x = random.randint(PISTA_ESQUERDA, PISTA_DIREITA - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.velocidade = velocidade_base

    def update(self):
        self.rect.y += self.velocidade
        if self.rect.top > ALTURA_TELA:
            self.kill()


class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((6, 14))
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
        self.tempo_vida = 18

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.tempo_vida -= 1
        if self.tempo_vida <= 0:
            self.kill()