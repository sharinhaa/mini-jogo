import pygame

pygame.font.init()

# CONFIGURAÇÕES DA TELA E FRAMERATE
LARGURA_TELA = 800
ALTURA_TELA = 600
fps = 60

# LIMITES DA PISTA DE ASFALTO (Para evitar que entidades saiam para a grama)
PISTA_ESQUERDA = 180
PISTA_DIREITA = 620

# CORES
VERDE_CARRO = (34, 139, 34)
VERMELHO_CARRO = (220, 20, 60)
AZUL_CARRO = (30, 144, 255)
AMARELO_CARRO = (255, 215, 0)
CASTANHO_CAIXA = (139, 69, 19)

CIANO_NEON = (0, 255, 255)
ROXO_NEON = (180, 0, 255)
COR_CHAVE_DE_FENDA = (192, 192, 192)

cor_fundo = (15, 5, 25)
cor_texto = (255, 255, 255)

# FONTES
fonte_HUD = pygame.font.SysFont("Consolas", 20, bold=True)
fonte_titulo = pygame.font.SysFont("Consolas", 40, bold=True)