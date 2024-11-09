import heapq

## A continuacion se definen variables constantes para todo el programa segun el enunciado del proyecto

# Define los tiempos que tardan Javier y Andreína por recorrer una cuadra
TIEMPO_JAVIER = {'normal': 4, 'mala_acera': 6, 'calle_comercial': 8}
TIEMPO_ANDREINA = {'normal': 6, 'mala_acera': 8, 'calle_comercial': 10}

# Coordenadas de cada punto relevante
CASA_JAVIER = (54, 14)
CASA_ANDREINA = (52, 13)
establecimientos = {
    "The Darkness": (50, 14),
    "La Pasion": (54, 11),
    "Mi Rolita": (50, 12)
}

# Limites de la cuadrícula
limite_norte = 55
limite_sur = 50
limite_este = 10
limite_oeste = 15

# Función para definir el tiempo de recorrido entre cuadras, considerando dirección del movimiento
def obtener_tiempo(origen, destino, persona):
    calle_origen, carrera_origen = origen
    calle_destino, carrera_destino = destino
    
    # Determinamos si el movimiento es en sentido vertical (carrera) o horizontal (calle)
    if calle_origen == calle_destino:
        # Movimiento en sentido de calle (Este-Oeste o Oeste-Este)
        if calle_origen == 51 or calle_destino == 51:
            # Si cualquiera de las dos calles es la comercial
            return TIEMPO_JAVIER['calle_comercial'] if persona == 'Javier' else TIEMPO_ANDREINA['calle_comercial']
        else:
            # Calle sin condición especial
            return TIEMPO_JAVIER['normal'] if persona == 'Javier' else TIEMPO_ANDREINA['normal']
        
    
    elif carrera_origen == carrera_destino:
        # Movimiento en sentido de carrera (Norte-Sur o Sur-Norte)
        if carrera_origen in {12, 13, 14} or carrera_destino in {12, 13, 14}:
            # Si cualquiera de las dos carreras es "mala acera"
            return TIEMPO_JAVIER['mala_acera'] if persona == 'Javier' else TIEMPO_ANDREINA['mala_acera']
        else:
            # Carrera sin condición especial
            return TIEMPO_JAVIER['normal'] if persona == 'Javier' else TIEMPO_ANDREINA['normal']

# Construcción del grafo como diccionario de adyacencia
def construir_grafo(persona):
    grafo = {}
    for calle in range(limite_sur, limite_norte + 1):
        for carrera in range(limite_este, limite_oeste + 1):
            nodo = (calle, carrera)
            grafo[nodo] = []
            vecinos = [
                (calle + 1, carrera), (calle - 1, carrera),  # arriba y abajo
                (calle, carrera + 1), (calle, carrera - 1)   # derecha e izquierda
            ]
            
            for vecino in vecinos:
                if (limite_sur <= vecino[0] <= limite_norte and limite_este <= vecino[1] <= limite_oeste):
                    tiempo = obtener_tiempo(nodo, vecino, persona)
                    grafo[nodo].append((vecino, tiempo))
    return grafo

def dijkstra(grafo, origen, destino):
    # Inicialización de la distancia y el predecesor
    distancia = {nodo: float('inf') for nodo in grafo}
    distancia[origen] = 0
    predecesor = {nodo: None for nodo in grafo}  # Almacena el nodo anterior en la ruta más corta
    cola_prioridad = [(0, origen)]
    
    while cola_prioridad:
        dist_actual, actual = heapq.heappop(cola_prioridad)
        
        # Si llegamos al destino, salimos del bucle
        if actual == destino:
            break
        
        # Recorremos los vecinos del nodo actual
        for vecino, peso in grafo[actual]:
            nueva_distancia = dist_actual + peso
            if nueva_distancia < distancia[vecino]:
                distancia[vecino] = nueva_distancia
                predecesor[vecino] = actual  # Guardamos el nodo anterior
                heapq.heappush(cola_prioridad, (nueva_distancia, vecino))
    
    # Reconstrucción del camino desde el destino hasta el origen
    camino = []
    paso = destino
    while paso is not None:
        camino.append(paso)  # Añadimos el nodo al camino
        paso = predecesor[paso]  # Nos movemos al nodo anterior en la ruta
    
    camino.reverse()  # Invertimos el camino para que esté desde el origen hasta el destino
    
    return distancia[destino], camino

# Encuentra las rutas óptimas y sincroniza las salidas
def calcular_ruta(establecimiento):
    destino = establecimientos[establecimiento]
    
    grafo_javier = construir_grafo('Javier')
    grafo_andreina = construir_grafo('Andreina')
    
    tiempo_javier, camino_javier = dijkstra(grafo_javier, CASA_JAVIER, destino)
    tiempo_andreina, camino_andreina = dijkstra(grafo_andreina, CASA_ANDREINA, destino)
    
    if tiempo_javier == tiempo_andreina:
        print(f"Ambos pueden salir al mismo tiempo y llegarán juntos en {tiempo_javier} minutos.")
    elif tiempo_javier < tiempo_andreina:
        diferencia = tiempo_andreina - tiempo_javier
        print(f"Andreina debe salir {diferencia} minutos antes que Javier para que lleguen a {establecimiento} al mismo tiempo")
        # print(f"Javier debe salir primero y esperar {diferencia} minutos para que Andreína llegue al mismo tiempo.")
        print(f"Tiempo total de Javier: {tiempo_javier} minutos, Tiempo total de Andreína: {tiempo_andreina} minutos.")
    else:
        diferencia = tiempo_javier - tiempo_andreina
        print(f"Javier debe salir {diferencia} minutos antes que Andreina para que lleguen a {establecimiento} al mismo tiempo")
        # print(f"Andreína debe salir primero y esperar {diferencia} minutos para que Javier llegue al mismo tiempo.")
        print(f"Tiempo total de Javier: {tiempo_javier} minutos, Tiempo total de Andreína: {tiempo_andreina} minutos.")

    print(camino_javier)
    print(camino_andreina)

def add_stablishment(stablishment_name, cords): 
    establecimientos[stablishment_name] = cords
    print("Establecimiento agregado correctamente")

def remove_stablishment(stablishment_name): 
    if stablishment_name in establecimientos:
        establecimientos.pop(stablishment_name)
        print("Establecimiento eliminado correctamente")
    else:
        print("El establecimiento no se encunetra reghistrado")

# def add_calle(limite_norte):
#     return limite_norte += 1

# def add_carrera():
#     return limite_oeste += 1

# Ejemplo de uso

calcular_ruta("Mi Rolita")
print("Hola")
# grafo = construir_grafo("Javier")
# print(grafo)