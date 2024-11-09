import heapq
from Person import Person
from Stablishment import Stablishment
from Cuadricula import Cuadricula

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
def calcular_ruta(stablishment_name, stablishments, cuadricula, javier, andreina):
    destino = None
    establecimiento = None
    for stablishment in stablishments:
        if stablishment.name == stablishment_name:
            destino = stablishment.coords
            establecimiento = stablishment
    
    if destino == None:
        print("El establecimiento no esta registrado en la ciudad de Bogota")
    else:
        grafo_javier = cuadricula.construir_grafo(javier)
        grafo_andreina = cuadricula.construir_grafo(andreina)

        print(grafo_javier)
        
        tiempo_javier, camino_javier = dijkstra(grafo_javier, javier.home_coords, destino)
        tiempo_andreina, camino_andreina = dijkstra(grafo_andreina, andreina.home_coords, destino)
        
        if tiempo_javier == tiempo_andreina:
            print(f"Ambos pueden salir al mismo tiempo y llegarán juntos en {tiempo_javier} minutos.")
        elif tiempo_javier < tiempo_andreina:
            diferencia = tiempo_andreina - tiempo_javier
            print(f"Andreina debe salir {diferencia} minutos antes que Javier para que lleguen a {establecimiento.name} al mismo tiempo")
            # print(f"Javier debe salir primero y esperar {diferencia} minutos para que Andreína llegue al mismo tiempo.")
            print(f"Tiempo total de Javier: {tiempo_javier} minutos, Tiempo total de Andreína: {tiempo_andreina} minutos.")
        else:
            diferencia = tiempo_javier - tiempo_andreina
            print(f"Javier debe salir {diferencia} minutos antes que Andreina para que lleguen a {establecimiento.name} al mismo tiempo")
            # print(f"Andreína debe salir primero y esperar {diferencia} minutos para que Javier llegue al mismo tiempo.")
            print(f"Tiempo total de Javier: {tiempo_javier} minutos, Tiempo total de Andreína: {tiempo_andreina} minutos.")

        print(camino_javier)
        print(camino_andreina)

def add_stablishment(stablishment_name, coords, stablishments, cuadricula):
    x, y = coords
    # Verificar si las coordenadas están dentro de los límites de la cuadrícula
    if (cuadricula.limite_sur <= x <= cuadricula.limite_norte and
        cuadricula.limite_este <= y <= cuadricula.limite_oeste):
        
        new_stablishment = Stablishment(stablishment_name, coords)
        stablishments.append(new_stablishment)
        print(f"Establecimiento '{stablishment_name}' agregado en {coords}")
    else:
        print(f"Error: Las coordenadas {coords} están fuera de los límites de la cuadrícula. No se puede agregar el establecimiento")

def remove_stablishment(stablishment_name, stablishments):
    establecimiento = None
    for stablishment in stablishments:
        if stablishment.name == stablishment_name:
            establecimiento = stablishment
    
    if establecimiento == None:
        print("No se ha encontrado el establecimiento a eliminar")
    else:
        stablishments.remove(establecimiento)
        
def add_carrera(cuadricula):
    cuadricula.add_carrera()

def add_calle(cuadricula):
    cuadricula.add_calle()

def remove_carrera(cuadricula):
    cuadricula.remove_carrera()

def remove_calle(cuadricula):
    cuadricula.remove_calle()

def main():
    persons = []
    stablishments = []
    ## Creamos a Javier y Andreina
    javier = Person("Javier", 4, 6, 8, (54, 14))
    andreina = Person("Andreina", 6, 8, 10, (52, 13))
    persons.append(javier)
    persons.append(andreina)

    ## Creamos los establecimientos iniciales
    the_darkness = Stablishment("The Darkness", (50, 14))
    la_pasion = Stablishment("La Pasion", (54, 11))
    mi_rolita = Stablishment("Mi Rolita", (50, 12))
    stablishments.append(the_darkness)
    stablishments.append(la_pasion)
    stablishments.append(mi_rolita)

    ## Creamos la cuadricula
    cuadricula = Cuadricula(55, 50, 10, 15)

    ## Pruebas
    add_calle(cuadricula)
    add_calle(cuadricula)
    add_carrera(cuadricula)
    remove_calle(cuadricula)

    calcular_ruta("The Darkness", stablishments, cuadricula, javier, andreina)
    add_stablishment("Mi Gafita", (57, 12), stablishments, cuadricula)
    print("Hola")

    return 

main()