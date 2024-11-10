import heapq
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
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
        messagebox.showwarning("Advertencia", "El establecimiento no está registrado en la ciudad de Bogotá")
    else:
        grafo_javier = cuadricula.construir_grafo(javier)
        grafo_andreina = cuadricula.construir_grafo(andreina)

        # print(grafo_javier)
        
        tiempo_javier, camino_javier = dijkstra(grafo_javier, javier.home_coords, destino)
        tiempo_andreina, camino_andreina = dijkstra(grafo_andreina, andreina.home_coords, destino)
        
        if tiempo_javier == tiempo_andreina:
            messagebox.showinfo("Resultados", f"Ambos pueden salir al mismo tiempo y llegarán juntos en {tiempo_javier} minutos.\n\nCamino que debe recorrer Javier: {camino_javier}\nCamino que debe recorrer Andreína: {camino_andreina}")
        elif tiempo_javier < tiempo_andreina:
            diferencia = tiempo_andreina - tiempo_javier
            messagebox.showinfo("Resultados", f"Andreina debe salir {diferencia} minutos antes que Javier para que lleguen a {establecimiento.name} al mismo tiempo\n\nTiempo total de Javier: {tiempo_javier} minutos\nTiempo total de Andreína: {tiempo_andreina} minutos.\n\nCamino que debe recorrer Javier: {camino_javier}\nCamino que debe recorrer Andreína: {camino_andreina}")
            # print(f"Javier debe salir primero y esperar {diferencia} minutos para que Andreína llegue al mismo tiempo.")
            # messagebox.showinfo("Resultados", f"Tiempo total de Javier: {tiempo_javier} minutos\nTiempo total de Andreína: {tiempo_andreina} minutos.")
        else:
            diferencia = tiempo_javier - tiempo_andreina
            messagebox.showinfo("Resultados", f"Javier debe salir {diferencia} minutos antes que Andreina para que lleguen a {establecimiento.name} al mismo tiempo\n\nTiempo total de Javier: {tiempo_javier} minutos\nTiempo total de Andreína: {tiempo_andreina} minutos.\n\nCamino que debe recorrer Javier: {camino_javier}\nCamino que debe recorrer Andreína: {camino_andreina}")
            # print(f"Javier debe salir {diferencia} minutos antes que Andreina para que lleguen a {establecimiento.name} al mismo tiempo\nTiempo total de Javier: {tiempo_javier} minutos\nTiempo total de Andreína: {tiempo_andreina} minutos.")
            # print(f"Andreína debe salir primero y esperar {diferencia} minutos para que Javier llegue al mismo tiempo.")
            # messagebox.showinfo("Resultados", f"Tiempo total de Javier: {tiempo_javier} minutos\nTiempo total de Andreína: {tiempo_andreina} minutos.")
            # print(f"Tiempo total de Javier: {tiempo_javier} minutos, Tiempo total de Andreína: {tiempo_andreina} minutos.")

        #print(camino_javier)
        #print(camino_andreina)

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

# Funciones para añadir y eliminar calles/carreras
def add_carrera(cuadricula):
    cuadricula.add_carrera()

def add_calle(cuadricula):
    cuadricula.add_calle()

def remove_carrera(cuadricula):
    cuadricula.remove_carrera()

def remove_calle(cuadricula):
    cuadricula.remove_calle()

# Función para dibujar el mapa en la cuadrícula, incluyendo las calles, carreras y pesos
def dibujar_mapa(canvas, cuadricula, javier, andreina, stablishments):
    # Ajustes del mapa
    tam_punto = 5  # Tamaño del punto en la cuadrícula
    escala = 50  # Escala para el tamaño de la cuadrícula en píxeles
    offset_x, offset_y = 50, 50  # Desplazamiento para centrar la cuadrícula en el canvas

    # Dibujar la cuadrícula de intersecciones y líneas de calles/carreras
    for calle in range(cuadricula.limite_sur, cuadricula.limite_norte + 1):
        for carrera in range(cuadricula.limite_este, cuadricula.limite_oeste + 1):
            x = offset_x + (carrera - cuadricula.limite_este) * escala
            y = offset_y + (cuadricula.limite_norte - calle) * escala

            # Dibujar el punto de intersección
            canvas.create_oval(x - tam_punto, y - tam_punto, x + tam_punto, y + tam_punto, fill="blue")

            # Etiquetas especiales
            if (calle, carrera) == javier.home_coords:
                canvas.create_text(x, y - 15, text="J", fill="red", font=("Arial", 10, "bold"))
            elif (calle, carrera) == andreina.home_coords:
                canvas.create_text(x, y - 15, text="A", fill="red", font=("Arial", 10, "bold"))

            # Etiquetar establecimientos
            for stablishment in stablishments:
                if stablishment.coords == (calle, carrera):
                    canvas.create_text(x, y + 15, text=stablishment.name, fill="green", font=("Arial", 10, "bold"))

            grafo = cuadricula.construir_grafo(andreina)
            # Dibujar las conexiones con pesos entre intersecciones (calles y carreras)
            if (calle, carrera + 1) in grafo[(calle, carrera)]:  # Conexión hacia la derecha
                x_dest = offset_x + (carrera + 1 - cuadricula.limite_este) * escala
                y_dest = y
                peso = grafo[(calle, carrera)][(calle, carrera + 1)]
                canvas.create_line(x, y, x_dest, y_dest, fill="gray")
                canvas.create_text((x + x_dest) / 2, y - 10, text=str(peso), fill="black", font=("Arial", 8))

            if (calle + 1, carrera) in grafo[(calle, carrera)]:  # Conexión hacia abajo
                x_dest = x
                y_dest = offset_y + (cuadricula.limite_norte - (calle + 1)) * escala
                peso = grafo[(calle, carrera)][(calle + 1, carrera)]
                canvas.create_line(x, y, x_dest, y_dest, fill="gray")
                canvas.create_text(x - 10, (y + y_dest) / 2, text=str(peso), fill="black", font=("Arial", 8))

# Funciones para actulizar el mapa
def update_map(canvas, cuadricula, javier, andreina, stablishments):
    # Limpiar el canvas antes de redibujar
    canvas.delete("all")
    dibujar_mapa(canvas, cuadricula, javier, andreina, stablishments)

def add_carrera_and_update(canvas, cuadricula, javier, andreina, stablishments):
    add_carrera(cuadricula)
    update_map(canvas, cuadricula, javier, andreina, stablishments)

def add_calle_and_update(canvas, cuadricula, javier, andreina, stablishments):
    add_calle(cuadricula)
    update_map(canvas, cuadricula, javier, andreina, stablishments)

def remove_carrera_and_update(canvas, cuadricula, javier, andreina, stablishments):
    remove_carrera(cuadricula)
    update_map(canvas, cuadricula, javier, andreina, stablishments)

def remove_calle_and_update(canvas, cuadricula, javier, andreina, stablishments):
    remove_calle(cuadricula)
    update_map(canvas, cuadricula, javier, andreina, stablishments)

# Lista desplegable de establecimientos
def update_stablishment_combobox(combobox, stablishments):
    combobox['values'] = [stablishment.name for stablishment in stablishments]
    if stablishments:
        combobox.current(0)  # Seleccionar el primer establecimiento por defecto

def add_stablishment_and_update(combobox, stablishment_name, coords, stablishments, cuadricula):
    add_stablishment(stablishment_name, coords, stablishments, cuadricula)
    update_stablishment_combobox(combobox, stablishments)

def remove_stablishment_and_update(combobox, stablishment_name, stablishments):
    remove_stablishment(stablishment_name, stablishments)
    update_stablishment_combobox(combobox, stablishments)

def init_app(cuadricula, javier, andreina, stablishments):
    # Configuración de la ventana de Tkinter
    ventana = Tk()
    ventana.title("Mapa de la Ciudad")
    ventana.geometry("950x500")

    # Crear un frame para los botones
    marco = Frame(ventana)
    marco.pack(side=LEFT, padx=80, pady=10)

    # Crear un combobox para los establecimientos
    combobox = ttk.Combobox(marco, width=25)
    combobox.pack(pady=5)

    # Actualizar el Combobox con los establecimientos existentes
    update_stablishment_combobox(combobox, stablishments)

    # Botones
    btn_calcular_ruta = Button(marco, text="Calcular trayectoria", command=lambda: calcular_ruta(combobox.get(), stablishments, cuadricula, javier, andreina))
    btn_calcular_ruta.pack(fill=X, pady=5)

    btn_agregar_calle = Button(marco, text="Agregar calle", command=lambda: add_calle_and_update(canvas, cuadricula, javier, andreina, stablishments))
    btn_agregar_calle.pack(fill=X, pady=5)

    btn_agregar_carrera = Button(marco, text="Agregar carrera", command=lambda: add_carrera_and_update(canvas, cuadricula, javier, andreina, stablishments))
    btn_agregar_carrera.pack(fill=X, pady=5)

    btn_eliminar_calle = Button(marco, text="Eliminar calle", command=lambda: remove_calle_and_update(canvas, cuadricula, javier, andreina, stablishments))
    btn_eliminar_calle.pack(fill=X, pady=5)

    btn_eliminar_carrera = Button(marco, text="Eliminar carrera", command=lambda: remove_carrera_and_update(canvas, cuadricula, javier, andreina, stablishments))
    btn_eliminar_carrera.pack(fill=X, pady=5)

    # Crear canvas para el mapa
    canvas = Canvas(ventana, width=600, height=600)
    canvas.pack(side=RIGHT, padx=80, pady=60)

    # Dibujar el mapa al iniciar
    dibujar_mapa(canvas, cuadricula, javier, andreina, stablishments)

    # Con este comando arranca la interfaz
    ventana.mainloop()

def main():
    persons = []
    stablishments = []

    # Creamos a Javier y Andreina
    javier = Person("Javier", 4, 6, 8, (54, 14))
    andreina = Person("Andreina", 6, 8, 10, (52, 13))
    persons.append(javier)
    persons.append(andreina)

    # Creamos los establecimientos iniciales
    the_darkness = Stablishment("The Darkness", (50, 14))
    la_pasion = Stablishment("La Pasion", (54, 11))
    mi_rolita = Stablishment("Mi Rolita", (50, 12))
    stablishments.append(the_darkness)
    stablishments.append(la_pasion)
    stablishments.append(mi_rolita)

    # Creamos la cuadricula
    cuadricula = Cuadricula(55, 50, 10, 15)

    '''calcular_ruta("The Darkness", stablishments, cuadricula, javier, andreina)
    add_stablishment("Mi Gafita", (57, 12), stablishments, cuadricula)'''

    init_app(cuadricula, javier, andreina, stablishments)
    
    return 

main()