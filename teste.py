import pygame as py
import random
from settings import BASE_DIR

# Build paths inside the project like this: BASE_DIR / 'subdir'.

# INICIANDO PYGAME
py.init()

# PONTOS
pontos = 3
fonte = py.font.SysFont('fonts/PixelGameFont.ttf', 50)

# TAMANHO DA TELA
x = 1280
y = 720

# ABRIR JOGO+NOME DO JOGO
screen = py.display.set_mode((x, y))
py.display.set_caption("ABSUS")

# CARREGAR E CONVERTER IMAGEM PARA TAMANHO DA TELA
JOG = py.image.load(f'{BASE_DIR}/IMG/FUNDO.jpg').convert_alpha()
JOG = py.transform.scale(JOG, (x, y))

# CARREGAR IMAGEM OVNI
OVNI = py.image.load(f'{BASE_DIR}/IMG/OVNI.png').convert_alpha()
OVNI = py.transform.scale(OVNI, (50, 50))

# CARREGAR IMAGEM PLAYER
PLAYER = py.image.load(f'{BASE_DIR}/IMG/nave.png').convert_alpha()
PLAYER = py.transform.scale(PLAYER, (50, 50))

# CARREGAR IMAGEM TIRO
TIRO = py.image.load(f'{BASE_DIR}/IMG/tiro.png').convert_alpha()
TIRO = py.transform.scale(TIRO, (25, 25))

# LOCALIZAÇAO INICIAL
OVNI_y = 200
OVNI_x = 580

y_PLAYER = 600
x_PLAYER = 580

velocidade_y_tiro = 0
y_TIRO = 605
x_TIRO = 585

# VARIAVEL
atirar = False
rodando = True

# TRANFORMAR EM OBJETO/COLIZAO
player_obj = PLAYER.get_rect()
ovni_obj = OVNI.get_rect()
missil_obj = TIRO.get_rect()

# RESPAWNAR


def respawn():
    x = random.randint(50, 1200)
    y = 1
    return [x, y]


def respawn_misil():
    atirar = False
    reset_misil_x = x_PLAYER + 5
    reset_misil_y = y_PLAYER + 5
    velocidade_y_tiro = 0
    return[reset_misil_x, reset_misil_y, atirar, velocidade_y_tiro]


def colisa():
    global pontos
    if missil_obj.colliderect(ovni_obj):
        pontos += 1
        return True
    elif player_obj.colliderect(ovni_obj) or OVNI_y == 665:
        pontos -= 1
        return True
    else:
        return False


# LOOP PARA MANTER TERMINAL+JOGO
while rodando:
    for event in py.event.get():
        if event.type == py.QUIT:
            rodando = False
    screen.blit(JOG, (0, 0))

    # MOVIMENTANDO O FUNDO

    aux_y = y % JOG.get_rect().height
    screen.blit(JOG, (0, aux_y - JOG.get_rect().height))
    if aux_y < 720:
        screen.blit(JOG, (0, aux_y))
    # MOVIMENTO EM SI
    y += 1

    # TECLAS
    TECLA = py.key.get_pressed()
    if TECLA[py.K_UP] and y_PLAYER > 1:
        y_PLAYER = y_PLAYER - 2
        if not atirar:
            y_TIRO = y_TIRO - 2
    if TECLA[py.K_DOWN] and y_PLAYER < 665:
        y_PLAYER = y_PLAYER + 2
        if not atirar:
            y_TIRO = y_TIRO + 2
    if TECLA[py.K_RIGHT] and x_PLAYER < 1220:
        x_PLAYER = x_PLAYER + 2
        if not atirar:
            x_TIRO += 2
    if TECLA[py.K_LEFT] and x_PLAYER > 1:
        x_PLAYER -= 2
        if not atirar:
            x_TIRO -= 2

    if TECLA[py.K_SPACE]:
        atirar = True
        velocidade_y_tiro = 2

    # RESET OVNI/TIRO
    if OVNI_y == 665:
        OVNI_y = respawn()[1]
        OVNI_x = respawn()[0]
    OVNI_y = OVNI_y + 1
    if colisa():
        OVNI_x = respawn()[0]
        OVNI_y = respawn()[1]
    if y_TIRO == 1:
        x_TIRO, y_TIRO, atirar, velocidade_y_tiro = respawn_misil()

    y_TIRO -= velocidade_y_tiro

    # REGRAS
    if pontos == -1:
        rodando = False

    # RECT
    player_obj.x = x_PLAYER
    player_obj.y = y_PLAYER

    ovni_obj.x = OVNI_x
    ovni_obj.y = OVNI_y

    missil_obj.x = x_TIRO
    missil_obj.y = y_TIRO

    score = fonte.render(f'Pontos: {int(pontos)}', True, (255, 0, 0))
    screen.blit(score, (50, 50))

    # CRIANDO IMAGEM
    screen.blit(OVNI, (OVNI_x, OVNI_y))
    screen.blit(PLAYER, (x_PLAYER, y_PLAYER))
    screen.blit(TIRO, (x_TIRO, y_TIRO))

    # CARREGAR IMAGEM CONTINUAMENTE
    py.display.update()
