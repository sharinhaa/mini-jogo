import pygame
import random
import sys


from config import (
    LARGURA_TELA, ALTURA_TELA, VERMELHO_CARRO, AMARELO_CARRO, CIANO_NEON, 
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

# --- CARREGAMENTO DAS IMAGENS DE FUNDO ---
# 1. Fundo do Jogo / Pista
try:
    fundo = pygame.image.load("assets/imagens/background.png").convert()
    fundo = pygame.transform.scale(fundo, (LARGURA_TELA, ALTURA_TELA))
except Exception:
    fundo = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
    fundo.fill(cor_fundo)

# 2. Fundo do Menu
try:
    fundo_menu = pygame.image.load("assets/imagens/Menu.png").convert()
    fundo_menu = pygame.transform.scale(fundo_menu, (LARGURA_TELA, ALTURA_TELA))
except Exception:
    fundo_menu = fundo

# 3. Fundo do Game Over
try:
    fundo_gameover = pygame.image.load("assets/imagens/Game_over.png").convert()
    fundo_gameover = pygame.transform.scale(fundo_gameover, (LARGURA_TELA, ALTURA_TELA))
except Exception:
    fundo_gameover = fundo


# CARREGAMENTO DOS SONS
def carregar_som(caminho):
    try:
       s = pygame.mixer.Sound(caminho)
       return s
    except Exception:
        return None

som_tiro = carregar_som("assets/sons/tiro.wav")
som_explosao = carregar_som("assets/sons/explosao.wav")
som_item = carregar_som("assets/sons/item.wav")

if som_tiro:
    som_tiro.set_volume(0.3)
if som_explosao:
    som_explosao.set_volume(0.4)
if som_item:
    som_item.set_volume(0.5)

try:
    sound_musica = pygame.mixer.Sound("assets/sons/musica.wav")
    sound_musica.set_volume(0.25)
    sound_musica.play(-1)
except Exception as e:
    print("Aviso: Música de fundo não encontrada.", e)

# ESTADOS DO JOGO: 'MENU', 'PLAYING', 'CREDITS', 'GAMEOVER'
estado_jogo = 'MENU'
menu_index = 0  # 0: Jogar, 1: Créditos, 2: Sair

# GRUPOS DE SPRITES
todos_sprites = pygame.sprite.Group()
inimigos = pygame.sprite.Group()
bombas = pygame.sprite.Group()
caixas = pygame.sprite.Group()
projeteis = pygame.sprite.Group()
itens = pygame.sprite.Group()

jogador = None
pontuacao = 0
tempo_inicio = 0
ultimo_spawn = 0

# CONFIGURAÇÃO DE VELOCIDADE
VELOCIDADE_INICIAL = 4.0
velocidade_base = VELOCIDADE_INICIAL
intervalo_spawn = 1200


def criar_explosao(x, y):
    pass


def desenhar_hud():
    texto_vidas = fonte_HUD.render(f"VIDAS: {jogador.vidas}", True, CIANO_NEON)
    texto_score = fonte_HUD.render(f"PONTOS: {pontuacao}", True, ROXO_NEON)
    tempo_corrido = (pygame.time.get_ticks() - tempo_inicio) // 1000
    texto_tempo = fonte_HUD.render(f"TEMPO: {tempo_corrido}s", True, cor_texto)

    tela.blit(texto_vidas, (20, 20))
    tela.blit(texto_score, (20, 50))
    tela.blit(texto_tempo, (20, 80))


def iniciar_novo_jogo():
    global pontuacao, velocidade_base, intervalo_spawn, tempo_inicio, ultimo_spawn, jogador, estado_jogo
    
    todos_sprites.empty()
    inimigos.empty()
    bombas.empty()
    caixas.empty()
    projeteis.empty()
    itens.empty()

    jogador = Jogador()
    todos_sprites.add(jogador)
    
    pontuacao = 0
    velocidade_base = VELOCIDADE_INICIAL
    intervalo_spawn = 1200
    tempo_inicio = pygame.time.get_ticks()
    ultimo_spawn = pygame.time.get_ticks()
    estado_jogo = 'PLAYING'


def desenhar_menu():
    tela.blit(fundo_menu, (0, 0))
    
    overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
    overlay.set_alpha(20)
    overlay.fill((0, 0, 0))
    tela.blit(overlay, (0, 0))

    posicoes_botoes = [
        (145, 205),  # JOGAR 
        (150, 315),  # CRÉDITOS 
        (150, 430)   # SAIR 
    ]

    opcoes = ["JOGAR", "CRÉDITOS", "SAIR"]

    for i, opt in enumerate(opcoes):
        cor = AMARELO_CARRO if i == menu_index else cor_texto
        prefixo = "> " if i == menu_index else ""
        
        txt_surf = fonte_HUD.render(f"{prefixo}{opt}", True, cor)
        
        centro_x, centro_y = posicoes_botoes[i]
        txt_rect = txt_surf.get_rect(center=(centro_x, centro_y))
        
        tela.blit(txt_surf, txt_rect)


def desenhar_creditos():
    tela.fill((15, 15, 25))
    
    tit = fonte_titulo.render("CRÉDITOS", True, CIANO_NEON)
    tela.blit(tit, (LARGURA_TELA // 2 - tit.get_width() // 2, 80))

    c1 = fonte_HUD.render("Minijogo: Retro Chase Neon Fury", True, cor_texto)
    c2 = fonte_HUD.render("Desenvolvido em Pygame", True, cor_texto)
    c3 = fonte_HUD.render("[ESPAÇO] ou [ESC] para voltar", True, AMARELO_CARRO)

    tela.blit(c1, (LARGURA_TELA // 2 - c1.get_width() // 2, 220))
    tela.blit(c2, (LARGURA_TELA // 2 - c2.get_width() // 2, 260))
    tela.blit(c3, (LARGURA_TELA // 2 - c3.get_width() // 2, 360))


def desenhar_game_over():
    # 1. Imagem de fundo do Game Over
    tela.blit(fundo_gameover, (0, 0))

    # 2. Overlay leve
    overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
    overlay.set_alpha(30)
    overlay.fill((0, 0, 0))
    tela.blit(overlay, (0, 0))

    # 3. Pontuação Final 
    txt_score = fonte_HUD.render(f"Pontuação Final: {pontuacao}", True, cor_texto)
    rect_score = txt_score.get_rect(center=(LARGURA_TELA // 2, 310))
    tela.blit(txt_score, rect_score)

    # 4. Textos dentro das placas metálicas
    txt_reiniciar = fonte_HUD.render("[R] REINICIAR", True, cor_texto)
    rect_reiniciar = txt_reiniciar.get_rect(center=(294, 390)) # Placa esquerda

    txt_menu = fonte_HUD.render("[Q] MENU", True, cor_texto)
    rect_menu = txt_menu.get_rect(center=(505, 390)) # Placa direita

    tela.blit(txt_reiniciar, rect_reiniciar)
    tela.blit(txt_menu, rect_menu)


# LOOP PRINCIPAL
rodando = True
while rodando:
    relogio.tick(fps)
    agora = pygame.time.get_ticks()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            # CONTROLES DO MENU
            if estado_jogo == 'MENU':
                if evento.key in [pygame.K_UP, pygame.K_w]:
                    menu_index = (menu_index - 1) % 3
                elif evento.key in [pygame.K_DOWN, pygame.K_s]:
                    menu_index = (menu_index + 1) % 3
                elif evento.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    if menu_index == 0:
                        iniciar_novo_jogo()
                    elif menu_index == 1:
                        estado_jogo = 'CREDITS'
                    elif menu_index == 2:
                        rodando = False

            # CONTROLES DOS CRÉDITOS
            elif estado_jogo == 'CREDITS':
                if evento.key in [pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN]:
                    estado_jogo = 'MENU'

            # CONTROLES DO GAMEOVER
            elif estado_jogo == 'GAMEOVER':
                if evento.key in [pygame.K_r, pygame.K_SPACE]:
                    iniciar_novo_jogo()
                elif evento.key in [pygame.K_q, pygame.K_ESCAPE]:
                    estado_jogo = 'MENU'

            # VOLTAR AO MENU TECLANDO ESC NO JOGO
            elif estado_jogo == 'PLAYING':
                if evento.key == pygame.K_ESCAPE:
                    estado_jogo = 'MENU'

    # LÓGICA DA PARTIDA (APENAS EM PLAYING)
    if estado_jogo == 'PLAYING':
        tempo_decorrido_segundos = (agora - tempo_inicio) / 1000.0
        
        velocidade_base = VELOCIDADE_INICIAL + (tempo_decorrido_segundos * 0.03)
        intervalo_spawn = max(500, 1200 - int(tempo_decorrido_segundos * 4))

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

        # COLISÕES
        for inimigo in pygame.sprite.groupcollide(inimigos, projeteis, True, True):
            pontuacao += 100
            criar_explosao(inimigo.rect.centerx, inimigo.rect.centery)
            if som_explosao:
                som_explosao.play()

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
                estado_jogo = 'GAMEOVER'

        for item in pygame.sprite.spritecollide(jogador, itens, True):
            jogador.vidas += 1
            if som_item:
                som_item.play()

    # RENDERIZAÇÃO
    if estado_jogo == 'MENU':
        desenhar_menu()
    elif estado_jogo == 'CREDITS':
        desenhar_creditos()
    elif estado_jogo == 'PLAYING':
        tela.blit(fundo, (0, 0))
        todos_sprites.draw(tela)
        desenhar_hud()
    elif estado_jogo == 'GAMEOVER':
        desenhar_game_over()

    pygame.display.flip()

pygame.quit()
sys.exit()