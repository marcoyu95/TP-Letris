from configuracion import *
from principal import *
from principal import *
import math
import random
import string


def recorroAQuitar (ocupadosX,ocupadosY,letrasEnPantalla,lista,fila):#recorre las listas y elimina la primer fila, luego hace bajar las letras que estan sobre esa fila
    aux=1
    while fila>=120: #techo+25
        if aux==1:   #quita la fila
            for elem in lista:
                    pos=busqueda(ocupadosX,ocupadosY,elem,fila)
                    if pos!=-1:
                        ocupadosX.pop(pos)
                        ocupadosY.pop(pos)
                        letrasEnPantalla.pop(pos)
            aux=0
        else:

            for elem in lista:  #hace descender las letras
                pos1=busqueda(ocupadosX,ocupadosY,elem,fila-25)
                if pos1!=-1: #arriba hay letras
                    ocupadosY[pos1]=ocupadosY[pos1]+25
            fila-=25

#para armar nueva palabra

def armarPalabra(ocupadosX,ocupadosY,posicionX,letrasenpantalla,posicionY,inicio):
    cadena=""
    band=1
    while band==1:
        pos=busqueda(ocupadosX,ocupadosY,inicio,posicionY)
        if pos!=-1:
            cadena+=letrasenpantalla[pos]
        else:
            band=0
        inicio+=30
    return cadena


def buscoinicio(ocupadosX,ocupadosY,posicionX,posicionY):#busca la posicion de la primer palabra ocupada
    inicio=posicionX
    while inicio>=0:
        pos=busqueda(ocupadosX,ocupadosY,inicio,posicionY)
        if pos==-1:
            return (inicio+30)
        inicio-=30
    return (inicio+30)

def busqueda(ocupadosX,ocupadosY,posicionX,posicionY): #Busco la posicionX, posicionY (por ejemplo posicionX=390, posicionY=500) en las listas
    for i in range(len(ocupadosX)):
        if(posicionX==ocupadosX[i] and posicionY==ocupadosY[i]):
            return i #retorna el indice
    return -1 #si no encontro el indice retorna -1


"""Compara al bajar si el lugar esta libre o no. Toma una posicion
y busca si no esta ocupada. Toma las listas de OcupadosX y ocupadosY y devuelve true
o false dependiendo de si la posicion esta libre o no
"""

def posicionLibre (ocupadosX,ocupadosY,posicionEnX,posicionEnY):
    for i in range(len(ocupadosX)):
        if(ocupadosX[i]==posicionEnX):
            aux=buscarMinimo(ocupadosX,ocupadosY,posicionEnX)
            if (posicionEnY>aux):#esta en una posicion ocupada
                return False
    return True


"""Recorre la lista de ocupadosX y se fija si ocupadosx[i] es igual
a la posicionEnX
En ese mismo i mira el indice de ocupadosY[i] y compara con el minimo.
Los valores en ocupadosY se listan en forma descendente segun se va ocupando el espacio
Retorna el valor minimo ocupado en Y.
"""

def buscarMinimo (ocupadosX,ocupadosY,posicionEnX):
    minimo=-1
    for i in range(len(ocupadosX)):
        if(ocupadosX[i]==posicionEnX):
            if(minimo==-1):
                minimo=ocupadosY[i]
            elif(ocupadosY[i]<minimo):
                minimo=ocupadosY[i]
    return minimo



# Cargar en listaPalabras las palabras del archivo.
def lectura(listaPalabras,archivo):
    for i in archivo:
        var=""
        for e in range(len(i)-1):
            var+=i[e]
        var=var.upper()
        listaPalabras.append(var)


# Puntua la palabra.
def puntuar(candidata):
    puntaje=0
    vocales="aeiouAEIOU"
    consonantesDificiles="jkqwxyzJKQWXYZ"
    for i in candidata:
        if i in vocales:
            puntaje=puntaje+1
        elif i in consonantesDificiles:
            puntaje=puntaje+5
        else:
            puntaje=puntaje+2
    return puntaje


"""Usa la funcion lugarLibre que toma como parametros la posicion en x +/- 30 pixeles
y la posicion en y + 20 pixeles para determinar si el lugar esta ocupado o no.
Verifica que la letra no pase los limites definidos en x y en y tanto para cada columna como para
los margenes de la pantalla del juego.
"""
# Mueve la letra hacia la izquierda, dererecha, hacia abajo.
def moverLetra(posicion, direccion,ocupadosX,ocupadosY):
    if direccion == "left" and posicion[0] > 0:
        if (posicion[0] - 30 < 0): #and posicionLibre(ocupadosX,ocupadosY,posicion[0]-30,posicion[1]+20)):
            posicion[0] = 0
        elif (posicionLibre(ocupadosX,ocupadosY,posicion[0] - 30, posicion[1] + 25)):
            posicion[0] -= 30
    elif direccion == "right" and posicion[0]<390:
        if(posicion[0] + 30 > 390):
            posicion[0] = 390
        elif(posicionLibre(ocupadosX,ocupadosY,posicion[0]+30,posicion[1]+25)):
            posicion[0] += 30
    elif direccion == "down":
        if posicion[1] < 490:
            if not posicion[0] in ocupadosX:
                posicion[1] += 40
            else:
                var=ocupadosX.count(posicion[0])
                var2 = 500 - (25*var)
                if posicion[1] + 40 < var2:
                    posicion[1] += 40
                else:
                    posicion[1] = var2

#Al presionar la tecla hacia arriba, hace caer la letra hasta la posicion libre que encuentre
    elif direccion == "up":
        var=ocupadosX.count(posicion[0])
        if var==0:
            posicion[1]=500
        else:
            posicion[1]= 500 - (25*var)


# Devuelve una letra del abecedario al azar.
def nuevaLetra():  #completa
    #abecedario = "OMARC"
    abecedario = "ARC"
    #abecedario = "mar"
    letraAleatoria = random.choice(abecedario)
    if letraAleatoria=="I":
        letraAleatoria=" I"
    return letraAleatoria


# Inventa una posicion. Por ejemplo: (x, y) x al azar e y bien arriba de
# la pantalla.
#La posicion fija siempre va a ser 35px sobre y para que no se superponga con el texto
def nuevaPosicion(posicion):  #completa
    posicionAleatoriaX = random.randrange(0,391,30)
    posicionFijaY = 35
    posicion[0] = posicionAleatoriaX
    posicion[1] = posicionFijaY


# Arma la palabra que esta en la fila de la ultima letra que cayo. En
# esta funcion pueden usar las tres funciones opcionales.
"""Busca la altura en y de la letra que cayo.
Luego busca todas las x que se encuentran en esa misma altura, ya que tienen
el mismo indice en las listas ocupadosX y ocupadosY.
Se obtienen las listas desordenadas. Para ordenarlas se utilizo un algoritmo de seleccion.
Compara las x de menor a mayor y las ordena de esa forma manteniendo el indice en y.
Luego el string obtenido se suma en la cadena nuevaPalabra, que es lo que devuelve la funcion.
"""
##def armarPalabra(letrasEnPantalla, ocupadosX, ocupadosY):
##    #evalua con esta variable la linea de la ultima letra
##    alturaultimaLetra=ocupadosY[len(ocupadosY)-1]
##    #aca se arma la nueva palabra a retornar
##    nuevaPalabra=""
##    listaDeIndicesEnY=[]
##    listaDeIndicesEnX=[]
##    listaDeNumerosEnX=[]
##    contador=0
##    for elemento in ocupadosY:
##        if elemento==alturaultimaLetra:
##            listaDeIndicesEnY.append(contador)
##        contador+=1
##
##    for indice in listaDeIndicesEnY:
##        numero=ocupadosX[indice]
##        listaDeNumerosEnX.append(numero)
##
##    for i in range(len(listaDeNumerosEnX)-1):
##        min=i
##        for j in range(i+1,len(listaDeNumerosEnX)):
##            if listaDeNumerosEnX[min] > listaDeNumerosEnX[j]:
##                min=j
##        auxDeY=listaDeIndicesEnY[min]
##        aux=listaDeNumerosEnX[min]
##        listaDeIndicesEnY[min]=listaDeIndicesEnY[i]
##        listaDeNumerosEnX[min]=listaDeNumerosEnX[i]
##        listaDeNumerosEnX[i]=aux
##        listaDeIndicesEnY[i]=auxDeY
##
##
##    for indice in listaDeIndicesEnY:
##        nuevaPalabra+=letrasEnPantalla[indice]
##    return nuevaPalabra


# Hace descender la letra, siempre que haya lugar hacia abajo. Devuelve
# True si la letra pudo bajar, y False en caso contrario. Si la letra no
# puede seguir bajando la guarda en letrasEnPantalla, y guarda su
# posicion en ocupados.
#Actualiza hasta que encuentra un limite inferior (esto es, la linea o alguna fila formada)
def actualizar(letra, posicion, letrasEnPantalla, ocupadosX, ocupadosY):
    if posicion[1] < 500:
        if not posicion[0] in ocupadosX:
            posicion[1] += 5
        else:
            var=ocupadosX.count(posicion[0])
            var2 = 500 - (25 * var)
            if posicion[1]<var2:
                posicion[1]+= 5
            else:
                #Cuando encuentra un limite, asigna las posiciones x e y que ocupa la letra a las listas ocupadosX y ocupadosY
                #y ademas asigna la letra a la lista letrasEnPantalla.
                #Guarda en el mismo subindice las tres listas
                ocupadosX.append(posicion[0])
                ocupadosY.append(posicion[1])
                if(letra==" I"):
                    letrasEnPantalla.append("I")
                else:
                    letrasEnPantalla.append(letra)
                #Estas son las listas que imprime cuando la letra se ubica sobre una posicion libre
                #distinta del limite inferior (503px, donde se ubica la linea)
                #print(ocupadosX)# Control de lista X
                #print(ocupadosY) #Control de lista Y
                #print(letrasEnPantalla)
                return True

#Cuando la condicion del if anterior no se cumple, asigna el lugar que ocupa la letra a la primera posicion
#de la lista en ocupadosY y en ocupadosX. Este es el limite inferior, ubicado inmediatamente sobre la linea
#del final de la pantalla
    else:
        posicion[1]=500
        #Cuando encuentra un limite, asigna las posiciones x e y que ocupa la letra a las listas ocupadosX y ocupadosY
        #y ademas asigna la letra a la lista letrasEnPantalla.
        #Guarda en el mismo subindice las tres listas
        ocupadosX.append(posicion[0])
        ocupadosY.append(posicion[1])
        if(letra==" I"):
            letrasEnPantalla.append("I")
        else:
            letrasEnPantalla.append(letra)
        #Estas son las listas que imprime cuando la letra toca el limite definido sobre la linea
        #print(ocupadosX) #Control de lista X
        #print(ocupadosY) #Control de lista Y
        #print(letrasEnPantalla)
        return True

#Define el limite superior de la pantalla
def techo(letra, posicion, letrasEnPantalla, ocupadosX, ocupadosY, bandera2):
    if posicion[1]<490:
        if not posicion[0] in ocupadosX:
            pass
        else:
            var=ocupadosX.count(posicion[0])
            var2=500-(25*var)
            if posicion[1]<=var2:
                pass
            else:
                if ocupadosY[len(ocupadosY)-1] <= 100: #limite de filas (techo)
                    resultado=1
                    return resultado
    return 0