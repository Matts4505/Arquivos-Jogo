import random

import pygame


pygame.init()

pygame.mixer.music.set_volume(0.09)
musica_de_fundo = pygame.mixer.music.load('animation-master/musicafundo.mp3')
pygame.mixer.music.play(-1)

xarope = pygame.mixer.Sound('animation-master/xaropinho.wav')
encostovini= pygame.mixer.Sound('animation-master/encostanovni.wav')
acertaovini = pygame.mixer.Sound('animation-master/batovni.wav')
atirando = pygame.mixer.Sound('animation-master/saindotiro.wav')
ponto_ganho = pygame.mixer.Sound('animation-master/ponto ganho.wav')
x = 1280
y = 720

screen = pygame.display.set_mode((x,y))
pygame.display.set_caption('Space War')


bg = pygame.image.load('animation-master/fundo.jpg').convert_alpha()
bg = pygame.transform.scale(bg, (x,y))

etzin = pygame.image.load('animation-master/inimiganave.png').convert_alpha()
etzin = pygame.transform.scale(etzin, (50,50))

jogador = pygame.image.load('animation-master/nave.png').convert_alpha()
jogador = pygame.transform.scale(jogador, (50,50))
jogador = pygame.transform.rotate(jogador, -90)

missil = pygame.image.load('animation-master/missel.png').convert_alpha()
missil = pygame.transform.scale(missil, (25,25))
missil = pygame.transform.rotate(missil, - 10)

pos_etzin_x = 500
pos_etzin_y = 360

pos_jogador_x = 200
pos_jogador_y = 300

pontos = 4
vel_x_missil = 0
pos_missil_x = 200
pos_missil_y = 300
triggered = False
rodando = True
font = pygame.font.SysFont('fonts/PixelGameFont.ttf',50)

retangulo_jogador = jogador.get_rect()
retangulo_etzin = etzin.get_rect()
retangulo_missil = missil.get_rect()

#função
def ressurgir():
    x = 1350
    y = random.randint(1,640)
    return [x,y]

def ressurgir_missel():
    triggered = False
    ressurgir_missel_x = pos_jogador_x
    ressurgir_missel_y = pos_jogador_y
    vel_x_missil = 0
    return [ressurgir_missel_x,ressurgir_missel_y,triggered,vel_x_missil]



def colisao():
    global pontos
    if retangulo_jogador.colliderect(retangulo_etzin) or retangulo_etzin.x == 60:
        encostovini.play()
        pontos -= 1
        return True
    elif retangulo_missil.colliderect(retangulo_etzin):
        acertaovini.play()
        pontos += 1
        ponto_ganho.play()
        return True
    else:
        return False



def exibir_mensagem(msg,tam,cor):
    fonte = pygame.font.SysFont('comicsansms',tam, True,False)
    mensagem = f'{msg}'
    texto_formatado = fonte.render(mensagem,True,cor)
    return texto_formatado



def reiniciar_jogo():
    global pontos,rodando,triggered
    pontos = 0
    rodando = False
    triggered = False








while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    screen.blit(bg, (0,0))

    rel_x = x % bg.get_rect().width
    screen.blit(bg, (rel_x - bg.get_rect().width,0))  #criar brackground
    if rel_x < 1280:
        screen.blit(bg, (rel_x , 0))


    #teclado
    tecla = pygame.key.get_pressed()
    if tecla[pygame.K_w] and pos_jogador_y > 1:
        pos_jogador_y -= 1

        if not triggered:
            pos_missil_y  -= 1

    if tecla[pygame.K_s] and pos_jogador_y < 665:
        pos_jogador_y += 1

        if not triggered:
            pos_missil_y  += 1

    if tecla[pygame.K_SPACE]:
        atirando.play()
        triggered = True
        vel_x_missil = 2

    if tecla[pygame.K_r] and rodando == True and pontos == 0 :
        reiniciar_jogo()

    # ressurgiralien

    if pos_etzin_x == 50 :
        pos_etzin_x = ressurgir()[0]
        pos_etzin_y = ressurgir()[1]

    if pos_missil_x == 1300:
        pos_missil_x, pos_missil_y, triggered, vel_x_missil = ressurgir_missel()

    if pos_etzin_x == 50 or colisao():
        pos_etzin_x = ressurgir()[0]
        pos_etzin_y = ressurgir()[1]

    if pontos <1:
        rodando = True
        game_over = exibir_mensagem('GAME OVER!!!', 40, (0,0,0))
        screen.blit(game_over,(1280//2,720//2))
        reimsg = exibir_mensagem('Atire em um ovni para reiniciar!!!',20,(0,0,0))
        slameo = exibir_mensagem('Ou colida com um deles para fechar!!!',20,(255,0,0))
        screen.blit(reimsg,(1280//2, (720//2)+60))
        screen.blit(slameo,(1280//2, (720//2)+100))
    if pontos <0:
        break



    #posições rect

    retangulo_jogador.y = pos_jogador_y
    retangulo_jogador.x = pos_jogador_x

    retangulo_missil.y = pos_missil_y
    retangulo_missil.x = pos_missil_x

    retangulo_etzin.y = pos_etzin_y
    retangulo_etzin.x = pos_etzin_x
    #movimento
    x -= 2
    pos_etzin_x -= 1
    pos_missil_x += vel_x_missil
    score = font.render(f'Pontos: {int(pontos)}', True, (0,0,0))
    screen.blit(score, (50,50))

    #mobs do jogo
    screen.blit(etzin, (pos_etzin_x, pos_etzin_y))

    screen.blit(missil, (pos_missil_x, pos_missil_y))

    screen.blit(jogador, (pos_jogador_x, pos_jogador_y))

    pygame.display.update()
print(pontos)