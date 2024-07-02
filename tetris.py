import sys
import os
import random
ANCHO_JUEGO, ALTO_JUEGO = 9, 18
IZQUIERDA, DERECHA = -1, 1
CUBO = 0
Z = 1
S = 2
I = 3
L = 4
L_INV = 5
T = 6

def get_resource_path(relative_path):
    """ Devuelve la ruta absoluta al recurso especificado """
    try:
        base_path = sys._MEIPASS  # Cuando se ejecuta con PyInstaller
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def verificar_puntaje(puntaje):
    '''
    Procesa el archivo de puntuaciones para convertirlo en una lista ordenada de mayor a menor.
    verifica si el puntaje obtenido supera a alguno de la lista.
    Si lo supera devuelve True y la posicion que deberia ocupar en la lista y la misma lista con todas las puntuaciones para poder agregar el nuevo, 
    y quitar el superado.
    De lo contrario devuelve False y la lista con las puntuaciones.

    '''
    puntuaciones = []
    puntuaciones_guardadas = get_resource_path('puntuaciones.txt')
    with open(puntuaciones_guardadas) as file:
        for linea in file:
            nombre, puntuacion = linea.strip('\n').split(';')
            puntuaciones.append((int(puntuacion), nombre))

        puntuaciones = (sorted(puntuaciones))[::-1]
        for i in range(len(puntuaciones)):
            if puntaje > puntuaciones[i][0]:
                return (i, puntuaciones), True
    return puntuaciones, False                    



def modificar_puntuaciones(posicion, puntuaciones, datos):
    '''
    agrega en el archivo de puntuaciones el puntaje y nombre nuevo y remueve el ultimo de la lista.
    '''
    puntaje, nombre = datos
    puntuaciones.insert(posicion, (nombre, puntaje))
    puntuaciones.remove(puntuaciones[-1])
    puntuaciones_guardadas = get_resource_path('puntuaciones.txt')
    with open(puntuaciones_guardadas, 'w') as file:    
        for x in puntuaciones:
            file.write(f'{x[1]};{x[0]}\n')

    return puntuaciones



def cargar_archivos(ruta):
    '''
    De acuerdo a la ruta ingresada carga y procesa el archivo de texto para que el contenido sea utilizable en las funciones.
    '''
    if ruta == 'teclas.txt':
        teclas = get_resource_path('teclas.txt')
        with open(teclas) as file:
            teclas = {}
            for linea in file: 
                if linea != ('\n'):
                    tecla, accion = linea.strip('\n').split(' = ')   
                    if not tecla in teclas:
                        teclas[tecla] = accion
        return teclas

    if ruta == 'partida_guardada.txt':
        partida_guardada = get_resource_path(ruta)
        with open(partida_guardada) as file:
        
            grilla = [[]for _ in range(18)]
            pieza_actual = [[]for _ in range(4)]
            puntaje = []

            for linea in file:
                grilla_txt, pieza_actual_txt, puntaje_txt = linea.split(';')

            cont = 0
            for x in grilla_txt:
                if x.isdigit():
                    grilla[cont].append(int(x))
                    if len(grilla[cont]) == 9:
                        cont += 1
            cont = 0
            for i in range(len(pieza_actual_txt)):
                c = pieza_actual_txt[i]
                if c.isdigit():
                    if pieza_actual_txt[i+1].isdigit():
                        c += pieza_actual_txt[i+1]
                        continue
                    pieza_actual[cont].append(int(c))
                    if len(pieza_actual[cont]) >= 2:
                        cont += 1
            puntaje_txt = puntaje_txt.split(',')
            puntaje.append(int(puntaje_txt[0][1:]))
            puntaje.append(int(puntaje_txt[1][:-1]))

            pieza_actual = (tuple(pieza_actual[0]), tuple(pieza_actual[1]) ,tuple(pieza_actual[2]) ,tuple(pieza_actual[3]))

            return (grilla, pieza_actual), puntaje



def guardar_partida(juego, puntaje, ruta):
    '''
    guarda el estado de juego ingresado.
    '''
    partida_a_guardar = get_resource_path(ruta)
    with open(partida_a_guardar, 'w') as file:
        file.write(f'{juego[0]};{juego[1]};{puntaje}')
    


def procesar_piezas():
    '''
    procesa el archivo txt de piezas y lo hace utilizable en las funciones
    '''
    piezas_file = get_resource_path('piezas.txt')
    with open(piezas_file) as file:
        cant_piezas = 7
        piezas_procesadas = [[]for _ in range(cant_piezas)] 
        contador = 0
        for linea in file:
            linea = linea.split()
            pieza_sin_procesar = linea[:-2] 
               
            for i in range(len(pieza_sin_procesar)):     
                p = pieza_sin_procesar[i].split(';')
                rotaciones = []

                for j in range(len(p)):
                    z = p[j].split(',')
                    cord = (int(z[0]), int(z[1]))
                    rotaciones.append(cord)
                piezas_procesadas[contador].append(rotaciones)
            contador += 1

        return piezas_procesadas   

PIEZAS = procesar_piezas()



def generar_pieza(pieza=None):
    """
    Genera una nueva pieza de entre PIEZAS al azar. Si se especifica el parámetro pieza
    se generará una pieza del tipo indicado. Los tipos de pieza posibles
    están dados por las constantes CUBO, Z, S, I, L, L_INV, T.

    El valor retornado es una tupla donde cada elemento es una posición
    ocupada por la pieza, ubicada en (0, 0). Por ejemplo, para la pieza
    I se devolverá: ( (0, 0), (0, 1), (0, 2), (0, 3) ), indicando que 
    ocupa las posiciones (x = 0, y = 0), (x = 0, y = 1), ..., etc.
    """
    piezas_sin_rotar = []
    for i in range(len(PIEZAS)):
        piezas_sin_rotar.append(PIEZAS[i][0])
    
    if pieza is None:
        return random.choice(piezas_sin_rotar)
    return piezas_sin_rotar[pieza]



def trasladar_pieza(pieza, dx, dy):
    """
    Traslada la pieza de su posición actual a (posicion + (dx, dy)).

    La pieza está representada como una tupla de posiciones ocupadas,
    donde cada posición ocupada es una tupla (x, y). 
    Por ejemplo para la pieza ( (0, 0), (0, 1), (0, 2), (0, 3) ) y
    el desplazamiento dx=2, dy=3 se devolverá la pieza 
    ( (2, 3), (2, 4), (2, 5), (2, 6) ).
    """
    pieza_trasladada = []
    for x, y in pieza:     
        x += dx
        y += dy      
        pieza_trasladada.append((x, y))  
    return tuple(pieza_trasladada) 



def crear_juego(pieza_inicial):
    """
    Crea un nuevo juego de Tetris.

    El parámetro pieza_inicial es una pieza obtenida mediante 
    pieza.generar_pieza. Ver documentación de esa función para más información.

    El juego creado debe cumplir con lo siguiente:
    - La grilla está vacía: hay_superficie da False para todas las ubicaciones
    - La pieza actual está arriba de todo, en el centro de la pantalla.
    - El juego no está terminado: terminado(juego) da False

    Que la pieza actual esté arriba de todo significa que la coordenada Y de 
    sus posiciones superiores es 0 (cero).
    """
    grilla = [[0 for _ in range(ANCHO_JUEGO)] for _ in range(ALTO_JUEGO)]
    pieza_centrada = trasladar_pieza(pieza_inicial, ANCHO_JUEGO//2-1, 0)
    return grilla, pieza_centrada



def dimensiones(juego):
    """
    Devuelve las dimensiones de la grilla del juego como una tupla (ancho, alto).
    """
    return (len(juego[0][0]), len(juego[0]))



def pieza_actual(juego):
    """
    Devuelve una tupla de tuplas (x, y) con todas las posiciones de la
    grilla ocupadas por la pieza actual.

    Se entiende por pieza actual a la pieza que está cayendo y todavía no
    fue consolidada con la superficie.

    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    return juego[1]
    


def hay_superficie(juego, x, y):
    """
    Devuelve True si la celda (x, y) está ocupada por la superficie consolidada.
    
    La coordenada (0, 0) se refiere a la posición que está en la esquina 
    superior izquierda de la grilla.
    """
    grilla, _ = juego   
    return grilla[y][x] != 0



def mover(juego, direccion):
    """
    Mueve la pieza actual hacia la derecha o izquierda, si es posible.
    Devuelve un nuevo estado de juego con la pieza movida o el mismo estado 
    recibido si el movimiento no se puede realizar.

    El parámetro direccion debe ser una de las constantes DERECHA o IZQUIERDA.
    """
    grilla, pieza_actual = juego
    
    movimiento = trasladar_pieza(pieza_actual, direccion, 0)
    if not validacion(grilla, movimiento):   
        return juego 
    return grilla, movimiento



def rotar(juego):
    '''
    Rota la pieza actual, de acuerdo a las rotaciones disponibles en el archivo "piezas.txt"
    si se alcanza la ultima rotacion, se vuelve a la del inicio.
    si la rotacion se puede hacer, devuelve un nuevo estado del juego, de lo contrario, devuelve el mismo estado que se ingreso.
    '''
    grilla, pieza_actual = juego
    pieza_ordenada = sorted(pieza_actual)
    pos_1 = pieza_ordenada[0]
    pieza_en_origen = []
    pieza_rotada = []
    
    for i in range(len(pieza_ordenada)):
        pieza_en_origen.append((pieza_ordenada[i][0] - pos_1[0], pieza_ordenada[i][1] - pos_1[1]))

    for i in range(len(PIEZAS)):
        for j in range(len(PIEZAS[i])):
            if PIEZAS[i][j] == pieza_en_origen:
                if PIEZAS[i][j] == PIEZAS[i][-1]:
                    for k in range(len(PIEZAS[i][j])):
                        pieza_rotada.append((PIEZAS[i][0][k][0] + pos_1[0], PIEZAS[i][0][k][1] + pos_1[1]))
                else:
                    for k in range(len(PIEZAS[i][j])):
                        pieza_rotada.append((PIEZAS[i][j+1][k][0] + pos_1[0], PIEZAS[i][j+1][k][1] + pos_1[1]))
    if not validacion(grilla, pieza_rotada):
        return grilla, pieza_actual
    return grilla, tuple(pieza_rotada)
            


def puntuaciones(lineas, puntos_anteriores=0):
    '''
    devuelve los puntos que se hicieron por jugada. Por cada pieza consolidada se suma 10 pts, por cada linea formada son 20 pts, 
    pero si se forman mas de una linea el resultado se multiplica por la cantidad de lineas formadas.
    por ejemplo si se formo una linea se suman 20 pts, pero si se formaron dos serian 40 pts por 2.

    '''
    linea_formada = 20
    pieza_consolidada = 10
    puntos_totales = puntos_anteriores + pieza_consolidada
    if lineas != 0:
        if lineas !=1:
            puntos_x_linea = linea_formada * lineas
            puntos_totales += puntos_x_linea * lineas
        else:
            puntos_totales += lineas * linea_formada
    return puntos_totales



def avanzar(juego, siguiente_pieza):
    """
    Avanza al siguiente estado de juego a partir del estado actual.
    
    Devuelve una tupla (juego_nuevo, cambiar_pieza) donde el primer valor
    es el nuevo estado del juego y el segundo valor es un booleano que indica
    si se debe cambiar la siguiente_pieza (es decir, se consolidó la pieza
    actual con la superficie).
    
    Avanzar el estado del juego significa:
     - Descender una posición la pieza actual.
     - Si al descender la pieza no colisiona con la superficie, simplemente
       devolver el nuevo juego con la pieza en la nueva ubicación.
     - En caso contrario, se debe
       - Consolidar la pieza actual con la superficie.
       - Eliminar las líneas que se hayan completado.
       - Cambiar la pieza actual por siguiente_pieza.

    Si se debe agregar una nueva pieza, se utilizará la pieza indicada en
    el parámetro siguiente_pieza. El valor del parámetro es una pieza obtenida 
    llamando a generar_pieza().

    **NOTA:** Hay una simplificación respecto del Tetris real a tener en
    consideración en esta función: la próxima pieza a agregar debe entrar 
    completamente en la grilla para poder seguir jugando, si al intentar 
    incorporar la nueva pieza arriba de todo en el medio de la grilla se
    pisara la superficie, se considerará que el juego está terminado.

    Si el juego está terminado (no se pueden agregar más piezas), la funcion no hace nada, 
    se debe devolver el mismo juego que se recibió.
    """
    grilla, pieza_actual = juego
    
    if terminado(juego):
        return juego, (False, 0)

    descenso = trasladar_pieza(pieza_actual, 0, 1)

    if validacion(grilla, descenso):
        juego_nuevo = grilla, descenso 
        return juego_nuevo, (False, 0) 
    
    consolidar(grilla, pieza_actual)

    pieza_centrada = trasladar_pieza(siguiente_pieza, ANCHO_JUEGO//2-1, 0) 

    verificar = forma_linea(grilla) #se forman lineas?

    if verificar[1] == 0: 
        juego_nuevo = grilla, pieza_centrada         
        return juego_nuevo, (True, 0)    
    juego_nuevo = verificar[0], pieza_centrada    
    return juego_nuevo, (True, verificar[1])


def terminado(juego):
    """
    Devuelve True si el juego terminó, es decir no se pueden agregar
    nuevas piezas, o False si se puede seguir jugando.
    """  
    grilla, pieza_actual = juego
    return not validacion(grilla, pieza_actual)



#/////////////////////////////////////////////////////funciones auxiliares////////////////////////////////////////////////////////////

def validacion(grilla, pieza):
    """
    Devuelve True si la posicion de la pieza esta disponible en la grilla,
    devuelve Fasle si esta ocupada por la superficie consolidadad o si esta fuera del margen.
    """
    for x, y in pieza:
        if x >= ANCHO_JUEGO or x < 0 or y >= ALTO_JUEGO or y < 0:
            return False
        elif grilla[y][x] != 0:
            return False
    return True


def forma_linea(grilla):
    """
    Analiza si se forma una o mas lineas horizontales, 
    si esto ocurre devuelve una nueva grilla con la linea borrada y el descenso de las piezas superiores si es que hay.
    y tambien devuelve la cantidad de lineas que se formaron.
    En caso contrario devuelve la misma grilla que se ingreso.
    """
    lineas = 0
    for linea in grilla:
        if all(valor == 1 for valor in linea):
            lineas += 1
            grilla.remove(linea)
            grilla.insert(0, [0 for _ in range(ANCHO_JUEGO)])
    return grilla, lineas


def consolidar(grilla, pieza):
    """
    consolida a la superficie de la grilla la pieza que ya no puede bajar.
    """
    for x, y in pieza:
        grilla[y][x] = 1 


