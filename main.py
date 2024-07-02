import tetris
import gamelib
import os

ESPERA_DESCENDER = 15
ANCHO_VENTANA = 450
ALTO_VENTANA = 520

ALTO_GRILLA = 18
ANCHO_GRILLA = 9


#////////////////////////////////////funciones graficas////////////////////////////////////////////////////

def coordenadas_en_pixeles():
    '''
    Devuelve coordenadas en pixeles segun el lugar que ocuparia en la grilla cada pieza.
    '''
    longitud_casilla = 25
    grilla_draw = []
    y1 = 0
    y2 = 25
    for i in range(ALTO_GRILLA):
        grilla_draw.append([])
        x1 = 33
        y1 += longitud_casilla
        x2 = 58
        y2 += longitud_casilla
        for j in range(ANCHO_GRILLA):
            grilla_draw[i].append([])
            x1 += longitud_casilla
            x2 += longitud_casilla
            grilla_draw[i][j] = x1, y1, x2, y2
    return grilla_draw


def dibujar_grilla():
    logo_path = tetris.get_resource_path(os.path.join('img', 'tetrislogo.gif'))
    gamelib.draw_image(logo_path, 8, 200)
    gamelib.draw_rectangle(57, 24, 285, 477, outline='white', fill='black', width=2)
    gamelib.draw_text('G) guardar partida', 90, 500, fill='white')
    gamelib.draw_text('C) cargar partida', 240, 500, fill='white')
    
    longitud_casilla = 25
    y1 = 0
    y2 = longitud_casilla
    for _ in range(ALTO_GRILLA):
        x1 = 33
        y1 += longitud_casilla
        x2 = 58
        y2 += longitud_casilla
        for _ in range(ANCHO_GRILLA):
            x1 += longitud_casilla
            x2 += longitud_casilla
            gamelib.draw_rectangle(x1, y1, x2, y2, outline='#212325', fill='black')


def dibujar_siguientes_piezas(juego, siguiente_pieza):
    gamelib.draw_rectangle(300, 25, 435, 340, outline='black', fill='black')
    gamelib.draw_rectangle(300, 25, 435, 45, outline='black', fill='#48586f')#sombreado siguientes
    gamelib.draw_text('siguientes', 355, 34, fill='white')
    
    if siguiente_pieza != []:
        if len(siguiente_pieza) == 4:
            
            cord = coordenadas_en_pixeles()
            celdas = []
            _, p, s, t = siguiente_pieza
            siguiente_pieza = p, s, t

            for i in range(len(siguiente_pieza)):
                celdas.append([])
                for x in siguiente_pieza[i]:                   
                    celda = (cord[x[1]][x[0]])
                    celdas[i].append(celda) 

            color = '#8bce90'
            for celda in celdas[0]:  
                gamelib.draw_rectangle(celda[0]+260, celda[1]+30, celda[2]+260, celda[3]+30, fill=color)

            for celda in celdas[1]:     
                gamelib.draw_rectangle(celda[0]+260, celda[1]+130, celda[2]+260, celda[3]+130, fill=color)

            for celda in celdas[2]:     
                gamelib.draw_rectangle(celda[0]+260, celda[1]+230, celda[2]+260, celda[3]+230, fill=color)


def dibujar_score(puntaje):
    puntos, lineas = puntaje
    gamelib.draw_rectangle(300, 370, 435, 425, outline='black', fill='black')#score
    gamelib.draw_rectangle(300, 430, 435, 480, outline='black', fill='black')#lineas
    gamelib.draw_rectangle(300, 370, 435, 390, outline='black', fill='#48586f')#sombreado socre
    gamelib.draw_rectangle(300, 430, 435, 450, outline='black', fill='#48586f')#sombreado lineas
    gamelib.draw_text('score', 355, 380, fill='white')
    gamelib.draw_text('lineas', 355, 440, fill='white')
    gamelib.draw_text(f'{puntos}', 355, 405, fill='white')# marcador score
    gamelib.draw_text(f'{lineas}', 355, 465, fill='white')# marcador lineas
    

def dibujar_piezas(juego):
    grilla, pieza_actual = juego

    cord = coordenadas_en_pixeles()
    celdas = []
    
    for x in pieza_actual:
        celda = (cord[x[1]][x[0]])
        celdas.append(celda) 

    for celda in celdas:     
        gamelib.draw_rectangle(celda[0], celda[1], celda[2], celda[3], fill='#8bce90') #pieza en juego

    for i in range(tetris.ALTO_JUEGO):
        for j in range(tetris.ANCHO_JUEGO):
            if grilla[i][j] == 1:  
                gamelib.draw_rectangle(cord[i][j][0], cord[i][j][1], cord[i][j][2], cord[i][j][3], fill='#43844b') #pieza consolidada


def dibujar_tabla_puntuaciones(tabla):
    if tabla[0] != 0:
        gamelib.draw_rectangle(100, 50, 320, 440, outline='white', fill='black', width=2)
        gamelib.draw_text('Tabla de Puntuaciones', 210, 70, fill='white')
        gamelib.draw_text('pulsa Enter para volver a jugar', 210, 410, size=10, fill='white')
        medida_alto = 100
        puesto = 1
        
        for puntos in tabla:
            gamelib.draw_text(f'{puesto}) {puntos[1]} : {puntos[0]}', 210, medida_alto, fill='white')
            puesto += 1
            medida_alto += 30


#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def preparar_piezas(siguiente_pieza):
    '''
    devuelve una lista con las siguientes 3 piezas a usar, si se usa una, se vuelve a llenar la lista par que sean 3 nuevamente.
    '''
    if siguiente_pieza == []:
        siguiente_pieza.append(0)
    
    if siguiente_pieza[0] != 3:
        while siguiente_pieza[0] < 3:     
            siguiente_pieza.append(tetris.generar_pieza())
            siguiente_pieza[0] += 1  
        return siguiente_pieza
    return siguiente_pieza


def juego_actualizar(juego, tecla_pres, teclas, piezas, puntaje):
    '''
    Analiza la tecla presionada y si corresponde a alguna anteriormente archivada devuelve un nuevo estado del juego.
    si la tecla no es de movimento, por ejemplo de guardar, guarda el juego actual y lo devuelve sin cambiar el estado.
    '''
    if not tecla_pres in teclas:
        return juego
        
    if teclas[tecla_pres] == 'IZQUIERDA':         
        return tetris.mover(juego, tetris.IZQUIERDA)

    if teclas[tecla_pres] == 'DERECHA':      
        return tetris.mover(juego, tetris.DERECHA)

    if teclas[tecla_pres] == 'DESCENDER': 
        juego_nuevo, opcion = tetris.avanzar(juego, piezas[1])
        if opcion[0]:
            # sound_path = tetris.get_resource_path(os.path.join('sound', 'colision.wav'))
            # gamelib.play_sound(sound_path)
            puntos_totales = tetris.puntuaciones(opcion[1], puntaje[0])
            puntaje[0] = puntos_totales
            puntaje[1] += opcion[1]
            piezas.pop(1)
            piezas[0] -= 1
        return juego_nuevo  
      
    if teclas[tecla_pres] == 'ROTAR':
        return tetris.rotar(juego)
    
    if teclas[tecla_pres] == 'GUARDAR':
        tetris.guardar_partida(juego, puntaje, 'partida_guardada.txt')
        return juego

    if teclas[tecla_pres] == 'CARGAR':
        juego_guardado, puntaje_guardado = tetris.cargar_archivos('partida_guardada.txt')   
        puntaje[0], puntaje[1] = puntaje_guardado[0], puntaje_guardado[1]      
        return juego_guardado

 
def main():
    gamelib.resize(ANCHO_VENTANA, ALTO_VENTANA)
    gamelib.title('Tetris')
    icon_path = tetris.get_resource_path(os.path.join('img', 'icon.gif'))
    gamelib.icon(icon_path)
    resetear = 0
    juego = tetris.crear_juego(tetris.generar_pieza())
    siguiente_pieza = []
    # Inicializar el estado del juego
    puntaje = [0, 0]
    teclas = tetris.cargar_archivos('teclas.txt')
    tabla_puntajes = [0]
    volver_a_jugar = [False] 
    tecla_seleccion = [0] 
    
    timer_bajar = ESPERA_DESCENDER
    while gamelib.loop(fps=30):
        gamelib.draw_begin()
        dibujar_grilla()
        dibujar_siguientes_piezas(juego, preparar_piezas(siguiente_pieza))
        dibujar_score(puntaje)
        dibujar_piezas(juego)
        dibujar_tabla_puntuaciones(tabla_puntajes)
        gamelib.draw_end()
        
        for event in gamelib.get_events():
            if not event:
                break
            if event.type == gamelib.EventType.KeyPress:
                tecla_pres = event.key
                juego = juego_actualizar(juego, tecla_pres, teclas, siguiente_pieza, puntaje)  
                tecla_seleccion[0] = tecla_pres
                # Actualizar el juego, según la tecla presionada
        if tetris.terminado(juego):
            puntuaciones, verificar = tetris.verificar_puntaje(puntaje[0])

            if verificar:
                nombre = gamelib.input('Nuevo puntaje alto, ingrese sus apodo (4 letras)')
                if nombre:
                    datos = nombre[:4], puntaje[0]
                else:
                    datos = 'desconocido', puntaje[0]
                tabla_puntajes = tetris.modificar_puntuaciones(puntuaciones[0], puntuaciones[1], datos)
                puntaje[0], puntaje[1] = resetear, resetear 
            else:
                tabla_puntajes = puntuaciones
            
            volver_a_jugar[0] = True

            if tecla_seleccion[0] == 'Return':
                puntaje[0], puntaje[1] = resetear, resetear 
                tabla_puntajes = [0]
                volver_a_jugar[0] = False
                juego = tetris.crear_juego(tetris.generar_pieza())
               
        elif not volver_a_jugar[0]:              
            timer_bajar -= 1
            if timer_bajar == 0:  
                juego = juego_actualizar(juego, 'Down', teclas, siguiente_pieza, puntaje)
                timer_bajar = ESPERA_DESCENDER 
        
gamelib.init(main)

