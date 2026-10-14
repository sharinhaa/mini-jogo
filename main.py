import pygame
import random
import sys

from config import (
    LARGURA_TELA, ALTURA_TELA, VERMELHO_CARRO, CIANO_NEON, 
    ROXO_NEON, fonte_HUD, fonte_titulo, cor_fundo, cor_texto, fps
)
from person import (
    Jogador, CarroInimigo, ObstaculoBomba, CaixaMadeira, 
    ChavedeFenda, ParticulaExplosao
)

# INICIALIZAÇÃO DE VÍDEO E ÁUDIO
pygame.init()
pygame.mixer.init()

tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Retro Chase: Neon Fury")
relogio = pygame.time.Clock()

# TELA DE FUNDO
try:
    fundo = pygame.image.load("assets/imagens/background.png").convert()
    fundo = pygame.transform.scale(fundo, (LARGURA_TELA, ALTURA_TELA))
except Exception:
    fundo = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
    fundo.fill(cor_fundo)

# CARREGAMENTO DOS SONS (COM SUPORTE A WAV/MP3)
def carregar_som(caminho):
    try:
        return pygame.mixer.Sound(caminho)
    except Exception:
        return None

som_tiro = carregar_som("assets/sons/tiro.wav")
som_explosao = carregar_som("assets/sons/explosao.wav")
som_item = carregar_som("assets/sons/item.wav")

# TENTATIVA DE CARREGAMENTO DA MÚSICA DE FUNDO
try:
    sound_musica = pygame.mixer.Sound("assets/sons/musica.wav")
    sound_musica.set_volume(0.3)
    sound_musica.play(-1)
except Exception:
    pass

# GRUPOS DE SPRITES
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


def criar_explosao(x, y):
    for _ in range(10):
        p = ParticulaExplosao(x, y)
        todos_sprites.add(p)


def desenhar_hud():
    texto_vidas = fonte_HUD.render(f"VIDAS: {jogador.vidas}", True, CIANO_NEON)
    texto_score = fonte_HUD.render(f"PONTOS: {pontuacao}", True, ROXO_NEON)
    tempo_corrido = (pygame.time.get_ticks() - tempo_inicio) // 1000
    texto_tempo = fonte_HUD.render(f"TEMPO: {tempo_corrido}s", True, cor_texto)

    tela.blit(texto_vidas, (20, 20))
    tela.blit(texto_score, (20, 50))
    tela.blit(texto_tempo, (20, 80))


def reiniciar_jogo():
    global game_over, pontuacao, velocidade_base, intervalo_spawn, tempo_inicio, jogador
    game_over = False
    
    todos_sprites.empty()
    inimigos.empty()
    bombas.empty()
    caixas.empty()
    projeteis.empty()
    itens.empty()

    jogador = Jogador()
    todos_sprites.add(jogador)
    
    pontuacao = 0
    velocidade_base = 4
    intervalo_spawn = 1200
    tempo_inicio = pygame.time.get_ticks()


# LOOP PRINCIPAL
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
        # DIFICULDADE PROGRESSIVA (A CADA 30 SEGUNDOS)
        tempo_decorrido = (agora - tempo_inicio) // 1000
        if tempo_decorrido > 0 and tempo_decorrido % 30 == 0:
            velocidade_base += 0.003
            intervalo_spawn = max(350, intervalo_spawn - 0.03)

        # SPAWN RESTRIÇÃO À PISTA
        if agora - ultimo_spawn > intervalo_spawn:
            sorteio = random.random()
            if sorteio < 0.50:
                obj = CarroInimigo(velocidade_base)
                inimigos.add(obj)
            elif sorteio < 0.78:
                obj = CaixaMadeira(velocidade_base)
                caixas.add(obj)
            else:
                obj = ObstaculoBomba(velocidade_base)
                bombas.add(obj)

            todos_sprites.add(obj)
            ultimo_spawn = agora

        # ATUALIZAÇÕES
        jogador.update(todos_sprites, projeteis, som_tiro)
        inimigos.update()
        bombas.update()
        caixas.update()
        projeteis.update()
        itens.update()

        # TRATAMENTO DE COLISÕES
        # 1. Projéteis x Inimigos
        for inimigo in pygame.sprite.groupcollide(inimigos, projeteis, True, True):
            pontuacao += 100
            criar_explosao(inimigo.rect.centerx, inimigo.rect.centery)
            if som_explosao:
                som_explosao.play()

        # 2. Projéteis x Caixas (40% de chance de dropar Chave de Fenda)
        colisoes_caixa = pygame.sprite.groupcollide(caixas, projeteis, True, True)
        for caixa in colisoes_caixa:
            pontuacao += 50
            criar_explosao(caixa.rect.centerx, caixa.rect.centery)
            if som_explosao:
                som_explosao.play()
                
            if random.random() < 0.40:
                chave = ChavedeFenda(caixa.rect.centerx, caixa.rect.centery)
                todos_sprites.add(chave)
                itens.add(chave)

        # 3. Jogador x Inimigos, Bombas ou Caixas
        colisao_fatal = (
            pygame.sprite.spritecollide(jogador, inimigos, True) or
            pygame.sprite.spritecollide(jogador, bombas, True) or
            pygame.sprite.spritecollide(jogador, caixas, True)
        )
        if colisao_fatal:
            jogador.vidas -= 1
            criar_explosao(jogador.rect.centerx, jogador.rect.centery)
            if som_explosao:
                som_explosao.play()
                
            if jogador.vidas <= 0:
                game_over = True

        # 4. Jogador x Item de Vida (Chave de Fenda)
        for item in pygame.sprite.spritecollide(jogador, itens, True):
            jogador.vidas += 1
            if som_item:
                som_item.play()

    # RENDERIZAÇÃO NA TELA
    tela.blit(fundo, (0, 0))
    todos_sprites.draw(tela)
    desenhar_hud()

    if game_over:
        txt_go = fonte_titulo.render("GAME OVER", True, VERMELHO_CARRO)
        txt_reiniciar = fonte_HUD.render("Pressione 'R' para Reiniciar", True, cor_texto)
        tela.blit(txt_go, (LARGURA_TELA // 2 - 110, ALTURA_TELA // 2 - 40))
        tela.blit(txt_reiniciar, (LARGURA_TELA // 2 - 150, ALTURA_TELA // 2 + 10))

    pygame.display.flip()

pygame.quit()
sys.exit()