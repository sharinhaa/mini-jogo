import pygame
import random
import sys

from config import LARGURA_TELA, ALTURA_TELA, VERDE_CARRO, VERMELHO_CARRO, AZUL_CARRO, AMARELO_CARRO, CASTANHO_CAIXA, CIANO_NEON, ROXO_NEON, fonte_HUD, fonte_titulo, cor_fundo, cor_texto, cor_tela, fps, COR_CHAVE_DE_FENDA

from person import Jogador, CarroInimigo, ObstaculoBomba, CaixaMadeira, ChavedeFenda

pygame.init()

tela = pygame.display.set_mode ((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Retro Chase: Neon Fury")
relogio = pygame.time.Clock()

#GRUPO DE SPRITES
todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
bombas = pygame.sprite.Group()
caixas = pygame.sprite.Group()
projeteis = pygame.sprite.Group()
itens = pygame.sprite.Group()

jogador = Jogador()
todos_sprites.add(jogador)

pontuacao = 0
tempo_inicio = pygame.time.get_ticks()
ultimo_spawn = pygame.time.get_ticks()
intervalo_spawn = 1200
velocidade_base = 4
game_over = False 

def desenhar_hud():
    texto_vidas = fonte_HUD.render(f"VIDAS: {jogador.vidas}", True, CIANO_NEON)
    texto_score = fonte_HUD.render(f"PONTOS: {pontuacao}", True, ROXO_NEON)
    tempo_corrido = (pygame.time.get_ticks() - tempo_inicio) // 1000
    texto_tempo = fonte_HUD.render(f"TEMPO: {tempo_corrido}s", True, cor_texto)

    tela.blit(texto_vidas, (20, 20))
    tela.blit(texto_score, (20, 50))
    tela.blit(texto_tempo, (20, 80))

def desenhar_pista():
    pygame.draw.rect(tela, cor_tela, (150, 0, LARGURA_TELA - 300, ALTURA_TELA))
    pygame.draw.line(tela, ROXO_NEON, (150, 0), (150, ALTURA_TELA), 5)
    pygame.draw.line(tela, ROXO_NEON, (LARGURA_TELA - 150, 0), (LARGURA_TELA - 150, ALTURA_TELA), 5)

def reiniciar_jogo():
    global game_over, pontuacao, velocidade_base, intevalo_spwan, tempo_inicio, jogador
    game_over = False
    todos_sprites.empty()
    inimigos.empty()
    bombas.empty()
    caixas.empty()
    projeteis.empty()
    itens.empty()

    jogador = Jogador()
    todos_sprites.add(jogador)
    todos_sprites.add(jogador)
    pontuacao = 0
    velocidade_base = 4
    intervalo_spawn = 1200
    tempo_inicio = pygame.time.get_ticks()

    #LOOP PRINCIPAL
rodando = True
while rodando:
     relogio.tick(fps)
     agora = pygame.time.get_ticks()

     for evento in pygame.event.get():
         if evento.type == pygame.QUIT:
             rodando = False
         if game_over and evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_r:
                 reiniciar_jogo()

     if not game_over:
         tempo_decorrido = (agora - tempo_inicio) // 1000
         if tempo_decorrido > 0 and tempo_decorrido % 30 ==0:
             velocidade_base += 0.005
             intervalo_spawn = max(400, intervalo_spawn - 0.05)

         if agora - ultimo_spawn > intervalo_spawn:
                sorteio = random.random()
                if sorteio <0.5:
                    obj = CarroInimigo(velocidade_base)
                    inimigos.add(obj)
                elif sorteio < 0.8:
                    obj = CaixaMadeira(velocidade_base)
                    caixas.add(obj)
                else:
                    obj = ObstaculoBomba(velocidade_base)
                    bombas.add(obj)

                todos_sprites.add(obj)
                ultimo_spawn = agora


            #ATUALIZAÇÕES
         jogador.update(todos_sprites, projeteis)
         inimigos.update()
         bombas.update()
         caixas.update()
         projeteis.update()
         itens.update()

        # COLISÕES
        # 1. Projétil destroi Carros Inimigos
     for inimigo in pygame.sprite.groupcollide(inimigos, projeteis, True, True):
            pontuacao += 100

        # 2. Projétil destroi Caixa (40% de chance de dropar Chave de Fenda)
     colisoes_caixa = pygame.sprite.groupcollide(caixas, projeteis, True, True)
     for caixa in colisoes_caixa:
            pontuacao += 50
            if random.random() < 0.4:
                chave = chave(COR_CHAVE_DE_FENDA, caixa.rect.centerx, caixa.rect.centery)
                todos_sprites.add(chave)
                itens.add(chave)

         # 3. Jogador colide com Inimigos, Bombas ou Caixas
     if (pygame.sprite.spritecollide(jogador, inimigos, True) or
            pygame.sprite.spritecollide(jogador, bombas, True) or
            pygame.sprite.spritecollide(jogador, caixas, True)):
            jogador.vidas -= 1
            if jogador.vidas <= 0:
                game_over = True

        # 4. Jogador coleta Chave de Fenda
     for item in pygame.sprite.spritecollide(jogador, itens, True):
            jogador.vidas += 1


     tela.fill(cor_fundo)
     desenhar_pista()
     todos_sprites.draw(tela)
     desenhar_hud()

     if game_over:
        txt_go = fonte_titulo.render("GAME OVER", True, VERMELHO_CARRO)
        txt_reiniciar = fonte_HUD.render("Pressione 'R' para Reiniciar", True, cor_texto)
        tela.blit(txt_go, (LARGURA_TELA // 2 - 110, ALTURA_TELA // 2 - 40))
        tela.blit(txt_reiniciar, (LARGURA_TELA // 2 - 150, ALTURA_TELA // 2 + 10))

     pygame.display.flip()

pygame.quit()
