#esta es la de marco
#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Jonathan
#
# Created:     06/11/2017
# Copyright:   (c) Jonathan 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sys,pygame
import math, os, random
from pygame.locals import *
from configuracion import *
from funcionesVACIAS import *
from extras import *


textoParaDiccionario=""
puntosParaTxt=0

def menu():
    # centrar la ventana y despues inicializar pygame
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    #Prepara la ventana de menu
    screen=pygame.display.set_mode((420,600))
    pygame.display.set_caption("Letris 2017")
    imagen=pygame.image.load("menu.png")
    imagen3=pygame.image.load("diccionariogeneral.png")
    imagen4=pygame.image.load("diccionarionombres.png")

    fondonegro=pygame.image.load("fondonegro.png")

    global textoParaDiccionario

    variable=True
    while variable:
        global fondonegro
        screen.blit(imagen,(0,0))
        screen.blit(fondonegro,(100,330))
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN:
                if event.key==K_RIGHT:
                    fondonegro=imagen3
                    textoParaDiccionario="diccionario.txt"
                if event.key==K_LEFT:
                    fondonegro=imagen4
                    textoParaDiccionario="nombres.txt"
                if event.key==K_RETURN:
                    if textoParaDiccionario!="":
                        variable=False
        pygame.display.update()

def juego():
    global puntosParaTxt
    global TIEMPO_MAX
    bandera2=0

    # centrar la ventana y despues inicializar pygame
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    # pygame.mixer.init()

    # preparar la ventana
    pygame.display.set_caption("LETRIS 2017")
    screen = pygame.display.set_mode((ANCHO, ALTO))

    fondoran=random.randint(1,2)  #fondos random
    if fondoran==1:
        imagen=pygame.image.load("flappy.jpg")
    else:
        imagen=pygame.image.load("montanas.png")

    #Musica en la ventana de juego
    #pygame.mixer.pre_init(44100, 16, 2, 4096)
    #pygame.init()
    #pygame.mixer.music.load("Patakas World.wav")
    #pygame.mixer.music.set_volume(0.5)
    #pygame.mixer.music.play(-1)

    # Tiempo total del juego
    gameClock = pygame.time.Clock()
    timeTicksInicial= pygame.time.get_ticks()
    totaltime = 0
    segundos = TIEMPO_MAX

    timeTicksTranscurrido= pygame.time.get_ticks() - timeTicksInicial
    segundos = TIEMPO_MAX - timeTicksTranscurrido / 1000

    fps = FPS_INICIAL

    puntos = 0
    candidata = ""


    #Cargar diccionario
    diccionario = ["CAR"]
    #archivo=open("nombres.txt","r")
    #lectura(diccionario,archivo)
    #print(diccionario)
    posicion = [0, 0]
    listaux=[0,30,60,90,120,150,180,210,240,270,300,330,360,390] #uso para las funciones de recorroAQuitar, contiene las posiciones de las columnas X
    ocupadosX = []
    ocupadosY = []
    letrasEnPantalla = []

    test=True

    band=False
    cont=1
    aux=0   #bandera para mostrar la siguiente letra
    letra=nuevaLetra()   #esto tambien agregue para mostrar la letra siguiente
    nuevaPosicion(posicion)

    #Ciclo infinito hasta que se acaba el tiempo. Mas abajo, dentro de una condicion
    #es posible conseguir mas tiempo cada vez que se forma una palabra
    while test:#segundos > fps / 1000:
        if segundos<=0:
            test=False


        # 1 frame cada 1/fps segundos
        gameClock.tick(fps)
        totaltime += gameClock.get_time()

        fps = 15

        # buscar la tecla presionada del modulo de eventos de pygame
        for e in pygame.event.get():
            if e.type == QUIT or bandera2==1:
                puntosParaTxt=puntos
                pygame.quit()
                return
            # ver si se presiona alguna tecla
            if e.type == KEYDOWN:
                direccion = dameTeclaApretada(e.key)
                moverLetra(posicion, direccion,ocupadosX,ocupadosY)

                if e.key == pygame.K_p:
                    pausa()



        segundos = TIEMPO_MAX - pygame.time.get_ticks() / 1000

        bandera = actualizar(letra, posicion, letrasEnPantalla, ocupadosX, ocupadosY)
        bandera2 = techo(letra, posicion, letrasEnPantalla, ocupadosX, ocupadosY, bandera2)

        if aux==0 : #if que agregue para mostrar la siguiente letra
            letranue=nuevaLetra()
            aux=1

        if bandera:
            letra = letranue
            nuevaPosicion(posicion)
            inicio=buscoinicio(ocupadosX,ocupadosY,ocupadosX[len(ocupadosX)-1],ocupadosY[len(ocupadosY)-1])
            candidata=armarPalabra(ocupadosX,ocupadosY,ocupadosX[len(ocupadosX)-1],letrasEnPantalla,ocupadosY[len(ocupadosY)-1],inicio)
            print("candidata:",candidata)
            for elemento in diccionario:
                if elemento in candidata:
                    puntos += puntuar(elemento)
                    #Remueve elementos o palabras dentro del archivo del diccionario
                    #para que no vuelva a contarlos.
                    #diccionario.remove(elemento)
                    band=True
                    recorroAQuitar(ocupadosX,ocupadosY,letrasEnPantalla,listaux,ocupadosY[len(ocupadosY)-1])

            #Suma segundos al armar una palabra que contenga una cantidad par de letras

            if band:
                if cont%2==0 and cont!=0:
                    print("Se suman 20 segundos")
                    TIEMPO_MAX+=20
                cont+=1
                band=False

            aux=0 #agregue para mostrar siguiente


        # limpiar pantalla anterior
        screen.fill(COLOR_FONDO)

        dibujar(screen, letra, posicion, letrasEnPantalla, ocupadosX, ocupadosY, puntos, segundos, imagen, letranue)
        pygame.display.flip()

    puntosParaTxt=puntos
    pygame.quit()


def pausa():
    global TIEMPO_MAX
    pausa = True
    imagenFondo = pygame.image.load("montanas.png")
    screen=pygame.display.set_mode((ANCHO,ALTO))
    gameClock = pygame.time.Clock()
    gameClock.tick(15)
    fuente = pygame.font.SysFont("Futura",100)
    fuente2 = pygame.font.SysFont("Arial", 30)
    texto = "Pausa"
    texto2 = "Presione P para continuar"
    texto3 = "Presione Q para salir"

    screen.blit(imagenFondo, (0,0))
    textoEnPantalla = fuente.render(texto, 0, (COLOR_PAUSA))
    screen.blit(textoEnPantalla, (100, 150))
    textoEnPantalla2 = fuente2.render(texto2, 0, (COLOR_PAUSA))
    screen.blit(textoEnPantalla2, (60,300))
    textoEnPantalla3 = fuente2.render(texto3, 0, (COLOR_PAUSA))
    screen.blit(textoEnPantalla3, (90, 350))

    var=pygame.time.get_ticks()+1000
    while pausa:
        var2=pygame.time.get_ticks()
        if var==var2:
            TIEMPO_MAX+=1
            var+=1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_p:
                    pausa = False
                elif event.key == K_q:
                    pygame.quit()
                    quit()

        pygame.display.update()



def puntaje():
    # centrar la ventana y despues inicializar pygame
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.init()
    #Prepara la ventana de menu
    screen=pygame.display.set_mode((420,600))
    pygame.display.set_caption("Letris 2017")
    imagen=pygame.image.load("puntaje.png")
    ###########El nombre del usuario########
    nombre=""
    mifuente=pygame.font.SysFont("Arial",30)

    isn="Ingrese su nombre o un alias:"
    mitextosecundario=mifuente.render(isn,0,(255,255,255))
    ########################################
    ##########el texto principal############
    textoParaPuntaje="Su puntaje fue de: "+str(puntosParaTxt)+" puntos"
    mitextoprincipal=mifuente.render(textoParaPuntaje,0,(255,255,255))
    ########################################
    textofinal="presione la tecla ENTER para continuar"
    mifuente2=pygame.font.SysFont("Arial",18)
    miultimotexto=mifuente2.render(textofinal,0,(255,255,255))

    var2=True
    while var2:
        screen.fill((0,0,0))
        mitexto=mifuente.render(nombre,0,(255,255,255))
        screen.blit(mitextoprincipal,(40,20))
        screen.blit(mitextosecundario,(40,150))
        screen.blit(miultimotexto,(70,550))
        screen.blit(mitexto,(150,200))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
            if event.type == KEYDOWN:
                if event.key == K_q:
                    nombre+="q"
                if event.key == K_w:
                    nombre+="w"
                if event.key == K_e:
                    nombre+="e"
                if event.key == K_r:
                    nombre+="r"
                if event.key == K_t:
                    nombre+="t"
                if event.key == K_y:
                    nombre+="y"
                if event.key == K_u:
                    nombre+="u"
                if event.key == K_i:
                    nombre+="i"
                if event.key == K_o:
                    nombre+="o"
                if event.key == K_p:
                    nombre+="p"
                if event.key == K_a:
                    nombre+="a"
                if event.key == K_s:
                    nombre+="s"
                if event.key == K_d:
                    nombre+="d"
                if event.key == K_f:
                    nombre+="f"
                if event.key == K_g:
                    nombre+="g"
                if event.key == K_h:
                    nombre+="h"
                if event.key == K_j:
                    nombre+="j"
                if event.key == K_k:
                    nombre+="k"
                if event.key == K_l:
                    nombre+="l"
                if event.key == K_z:
                    nombre+="z"
                if event.key == K_x:
                    nombre+="x"
                if event.key == K_c:
                    nombre+="c"
                if event.key == K_v:
                    nombre+="v"
                if event.key == K_b:
                    nombre+="b"
                if event.key == K_n:
                    nombre+="n"
                if event.key == K_m:
                    nombre+="m"
                if event.key == K_BACKSPACE:
                    var=""
                    for i in range(len(nombre)-1):
                        var+=nombre[i]
                    nombre=var
                if event.key == K_RETURN:
                    var2=False
        pygame.display.update()

    archivo=open("guardarPuntos.txt","a")
    archivo.write(str(nombre)+"\n")
    archivo.write(str(puntosParaTxt)+"\n")
    archivo.close()

        #puntajes y alias

    listaNombres=["AAA","AAA","AAA","AAA","AAA"]
    listaPuntaje=["0","0","0","0","0"]
    contador=2

    archivo2=open("guardarPuntos.txt","r")
    for i in archivo2:
        var=""
        if contador%2==0:
            for e in range(len(i)-1):
                var+=i[e]

            listaNombres.append(var)
            contador+=1
        else:
            for e in range(len(i)-1):
                var+=i[e]

            listaPuntaje.append(var)
            contador+=1
    archivo2.close()

    for i in range(len(listaPuntaje)-1):
        min=i
        for j in range(i+1,len(listaPuntaje)):
            if listaPuntaje[min] >= listaPuntaje[j]:
                min=j

        aux=listaPuntaje[min]
        listaPuntaje[min]=listaPuntaje[i]
        listaPuntaje[i]=aux
        auxDeNombres=listaNombres[min]
        listaNombres[min]=listaNombres[i]
        listaNombres[i]=auxDeNombres


    np1=listaNombres[len(listaNombres)-1]
    np2=listaNombres[len(listaNombres)-2]
    np3=listaNombres[len(listaNombres)-3]
    np4=listaNombres[len(listaNombres)-4]
    np5=listaNombres[len(listaNombres)-5]
    np6=listaPuntaje[len(listaPuntaje)-1]
    np7=listaPuntaje[len(listaPuntaje)-2]
    np8=listaPuntaje[len(listaPuntaje)-3]
    np9=listaPuntaje[len(listaPuntaje)-4]
    np10=listaPuntaje[len(listaPuntaje)-5]


    while True:
        mifuente2=pygame.font.SysFont("Arial",30)
        alias=mifuente2.render("Alias                          Puntaje",0,(255,255,255))
        n1=mifuente2.render(np1,0,(255,255,255))
        n2=mifuente2.render(np2,0,(255,255,255))
        n3=mifuente2.render(np3,0,(255,255,255))
        n4=mifuente2.render(np4,0,(255,255,255))
        n5=mifuente2.render(np5,0,(255,255,255))
        n6=mifuente2.render(np6,0,(255,255,255))
        n7=mifuente2.render(np7,0,(255,255,255))
        n8=mifuente2.render(np8,0,(255,255,255))
        n9=mifuente2.render(np9,0,(255,255,255))
        n10=mifuente2.render(np10,0,(255,255,255))

        screen.fill((0,0,0))
        screen.blit(alias,(50,100))
        screen.blit(n1,(50,150))
        screen.blit(n2,(50,200))
        screen.blit(n3,(50,250))
        screen.blit(n4,(50,300))
        screen.blit(n5,(50,350))
        screen.blit(n6,(330,150))
        screen.blit(n7,(330,200))
        screen.blit(n8,(330,250))
        screen.blit(n9,(330,300))
        screen.blit(n10,(330,350))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


def main():
    menu()
    juego()
    #puntaje()

if __name__ == '__main__':
    main()
