import pygame
from pygame.locals import *
from configuracion import *


def dameTeclaApretada(key):
    if key == K_UP or key == K_k or key == K_w or key == K_KP8:
        return "up"
    elif key == K_DOWN or key == K_j or key == K_s or key == K_KP2:
        return "down"
    elif key == K_RIGHT or key == K_l or key == K_d or key == K_KP6:
        return "right"
    elif key == K_LEFT or key == K_h or key == K_a or key == K_KP4:
        return "left"
    else:
        return ""


def dibujar(screen, letra, posicion, letrasEnPantalla, ocupadosX, ocupadosY, puntos, segundos, imagen, sigletra): #agregue un parametro (sigletra) para mostrarlo en pantalla
    screen.blit(imagen,(0,0))
    defaultFont = pygame.font.Font(pygame.font.get_default_font(), TAMANO_LETRA)
    defaultFontGRANDE = pygame.font.Font(pygame.font.get_default_font(), TAMANO_LETRA_GRANDE)

    pygame.draw.line(screen, (255, 255, 255), (0, ALTO - 70), (ANCHO, ALTO - 70), 5)

    ren1 = defaultFont.render("Puntos: " + str(puntos), 1, COLOR_TEXTO)
    ren2 = defaultFont.render("Tiempo: " + str(int(segundos)), 1, COLOR_TIEMPO_FINAL if segundos < 15 else COLOR_TEXTO)
    ren3 = defaultFontGRANDE.render(letra, 1, COLOR_LETRA)
    ren4 = defaultFont.render("Siguiente: ", 1, COLOR_BLANCO)  #muestra Siguiente en la pantalla
    ren5 = defaultFont.render(sigletra,1,COLOR_BLANCO)

    i = 0
    while i < len(letrasEnPantalla):
        if letrasEnPantalla[i] =="I":
            screen.blit(defaultFontGRANDE.render(letrasEnPantalla[i], 1, COLOR_TEXTO), (ocupadosX[i]+8, ocupadosY[i]))
        else:
            screen.blit(defaultFontGRANDE.render(letrasEnPantalla[i], 1, COLOR_TEXTO), (ocupadosX[i], ocupadosY[i]))
        i += 1

    screen.blit(ren1, (ANCHO - 120, 10))
    screen.blit(ren2, (10, 10))
    screen.blit(ren3, (posicion[0], posicion[1]))
    screen.blit(ren4, (280,570))   #muestra Siguiente en la pantalla
    screen.blit(ren5, (390,570))
    pygame.display.update()
