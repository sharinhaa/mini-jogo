import pygame

largura_tela = 800
altura_tela = 600
fps = 60

cor_fundo = (15, 5, 25)
cor_tela = (30, 20, 45)
cor_texto = (255, 255, 255)

amarelo_carro = (255, 215, 0)
vermelho_carro = (220, 20, 60)
verde_carro = (34, 139, 34)
azul_carro = (30, 144, 255)

pygame.font.init()
fonte_HUD = pygame.font.SysFont("Consolas", 20, bold= True)
fonte_titulo = pygame.font.SysFont("Consolas", 40, bold= True)
