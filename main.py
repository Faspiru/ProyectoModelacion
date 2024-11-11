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
def calcular_ruta(stablishment_name, stablishments, cuadricula, javier, andreina, canvas_javier, canvas_andreina, texto_javier, texto_andreina):
    destino = None
    establecimiento = None
    for stablishment in stablishments:
        if stablishment.name == stablishment_name:
            destino = stablishment.coords
            establecimiento = stablishment
    
    if destino is None:
        messagebox.showwarning("Advertencia", "El establecimiento no está registrado en la ciudad de Bogotá")
    else:
        grafo_javier = cuadricula.construir_grafo(javier)
        grafo_andreina = cuadricula.construir_grafo(andreina)
        
        tiempo_javier, camino_javier = dijkstra(grafo_javier, javier.home_coords, destino)
        tiempo_andreina, camino_andreina = dijkstra(grafo_andreina, andreina.home_coords, destino)
        
        # Actualizar los cuadros de texto con la ruta óptima
        texto_javier.delete(1.0, END)
        texto_javier.insert(END, f"Camino de Javier: {camino_javier}\nTiempo: {tiempo_javier} minutos")
        
        texto_andreina.delete(1.0, END)
        texto_andreina.insert(END, f"Camino de Andreina: {camino_andreina}\nTiempo: {tiempo_andreina} minutos")

        # Dibujar la ruta en los canvas
        update_map([canvas_andreina, canvas_javier], cuadricula, javier, andreina, stablishments, [andreina, javier], camino_andreina, camino_javier)

        # Mostrar mensaje en función de los tiempos
        if tiempo_javier == tiempo_andreina:
            messagebox.showinfo("Resultados", f"Ambos pueden salir al mismo tiempo y llegarán juntos en {tiempo_javier} minutos.")
        elif tiempo_javier < tiempo_andreina:
            diferencia = tiempo_andreina - tiempo_javier
            messagebox.showinfo("Resultados", f"Andreina debe salir {diferencia} minutos antes para llegar juntos.")
        else:
            diferencia = tiempo_javier - tiempo_andreina
            messagebox.showinfo("Resultados", f"Javier debe salir {diferencia} minutos antes para llegar juntos.")


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

def dibujar_mapa(canvas, cuadricula, javier, andreina, stablishments, referencia, ruta_optima=None):
    tam_punto = 5
    escala = 50
    offset_x, offset_y = 50, 50

    grafo = cuadricula.construir_grafo(referencia)

    # Dibujar los arcos o conexiones
    for nodo, vecinos in grafo.items():
        x1 = offset_x + (nodo[1] - cuadricula.limite_este) * escala
        y1 = offset_y + (cuadricula.limite_norte - nodo[0]) * escala
        for vecino, peso in vecinos:
            x2 = offset_x + (vecino[1] - cuadricula.limite_este) * escala
            y2 = offset_y + (cuadricula.limite_norte - vecino[0]) * escala
            color = "gray"
            if ruta_optima and ((nodo, vecino) in zip(ruta_optima, ruta_optima[1:]) or (vecino, nodo) in zip(ruta_optima, ruta_optima[1:])):
                color = "red" if referencia == javier else "yellow"  # Color para la ruta óptima

            canvas.create_line(x1, y1, x2, y2, fill=color)
            canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(peso), fill="black", font=("Arial", 8))

    # Dibujar las etiquetas de las calles y carreras
    for carrera in range(cuadricula.limite_este, cuadricula.limite_oeste + 1):
        x = offset_x + (carrera - cuadricula.limite_este) * escala
        canvas.create_text(x, offset_y - 20, text=f"{carrera}", fill="black", font=("Arial", 8, "bold"))

    for calle in range(cuadricula.limite_sur, cuadricula.limite_norte + 1):
        y = offset_y + (cuadricula.limite_norte - calle) * escala
        canvas.create_text(offset_x - 40, y, text=f"{calle}", fill="black", font=("Arial", 8, "bold"))

    # Dibujar la cuadrícula de intersecciones y etiquetas especiales
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

#Actualizar Mapa
def update_map(canvases, cuadricula, javier, andreina, stablishments, personas, ruta_andreina=None, ruta_javier=None):
    for i, persona in enumerate(personas):
        canvases[i].delete("all")
        ruta_optima = ruta_andreina if persona == andreina else ruta_javier
        dibujar_mapa(canvases[i], cuadricula, javier, andreina, stablishments, persona, ruta_optima)

        

def add_carrera_and_update(canvas_andreina, canvas_javier, cuadricula, javier, andreina, stablishments):
    add_carrera(cuadricula)
    update_map([canvas_andreina, canvas_javier], cuadricula, javier, andreina, stablishments, [andreina, javier])

def add_calle_and_update(canvas_andreina, canvas_javier, cuadricula, javier, andreina, stablishments):
    add_calle(cuadricula)
    update_map([canvas_andreina, canvas_javier], cuadricula, javier, andreina, stablishments, [andreina, javier])

def remove_carrera_and_update(canvas_andreina, canvas_javier, cuadricula, javier, andreina, stablishments):
    remove_carrera(cuadricula)
    uupdate_map([canvas_andreina, canvas_javier], cuadricula, javier, andreina, stablishments, [andreina, javier])

def remove_calle_and_update(canvas_andreina, canvas_javier, cuadricula, javier, andreina, stablishments):
    remove_calle(cuadricula)
    update_map([canvas_andreina, canvas_javier], cuadricula, javier, andreina, stablishments, [andreina, javier])

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
    ventana.geometry("1000x600")

    # Crear Notebook para las pestañas
    notebook = ttk.Notebook(ventana)
    notebook.grid(sticky="nsew")

    ventana.grid_rowconfigure(0, weight=1)
    ventana.grid_columnconfigure(0, weight=1)

    # Primera pestaña - Botones
    frame_botones = Frame(notebook)
    notebook.add(frame_botones, text="Opciones")

    # Segunda pestaña - Grafo de Andreina
    frame_grafo_andreina = Frame(notebook)
    notebook.add(frame_grafo_andreina, text="Grafo de Andreina")

    # Tercera pestaña - Grafo de Javier
    frame_grafo_javier = Frame(notebook)
    notebook.add(frame_grafo_javier, text="Grafo de Javier")

    # Combobox para establecimientos en la pestaña de opciones
    combobox = ttk.Combobox(frame_botones, width=25)
    combobox.pack(pady=5)
    update_stablishment_combobox(combobox, stablishments)

    # Configurar las columnas del frame de botones
    frame_botones.grid_columnconfigure((0, 1, 2, 3), weight=1)
    combobox.grid(row=0, column=1, columnspan=4, pady=5)
    Button(frame_botones, text="Calcular trayectoria", command=lambda: calcular_ruta(combobox.get(), stablishments, cuadricula, javier, andreina, canvas_javier, canvas_andreina, texto_javier, texto_andreina)).grid(row=0, column=0, sticky="ew", padx=100, pady=25)
    Button(frame_botones, text="Agregar calle", command=lambda: add_calle_and_update(canvas_andreina, canvas_javier, cuadricula, javier, andreina, stablishments)).grid(row=1, column=0, sticky="ew", padx=100, pady=25)
    Button(frame_botones, text="Agregar carrera", command=lambda: add_carrera_and_update(canvas_andreina, canvas_javier, cuadricula, javier, andreina, stablishments)).grid(row=2, column=0, sticky="ew", padx=100, pady=25)
    Button(frame_botones, text="Eliminar calle", command=lambda: remove_calle_and_update(canvas_andreina, canvas_javier, cuadricula, javier, andreina, stablishments)).grid(row=3, column=0, sticky="ew", padx=100, pady=25)

    #Cuadricula de Andreina
    canvas_andreina = Canvas(frame_grafo_andreina, width=600, height=600)
    canvas_andreina.pack(side=RIGHT, padx=80, pady=60)
    texto_andreina = Text(frame_grafo_andreina, width=50, height=5)
    leyendaAndreina = Label(frame_grafo_andreina, text="Leyenda: \nCalle Comercial: 10 minutos\nMala Acera: 8 minutos\nNormal: 6 minutos\n Ruta Óptima: Amarillo")
    leyendaAndreina.pack(side = BOTTOM,  pady=10)
    texto_andreina.pack(side=LEFT, anchor=CENTER, fill=X ,padx=20, pady=10)
    dibujar_mapa(canvas_andreina, cuadricula, javier, andreina, stablishments, andreina)

    #Cuadricula de Javier
    canvas_javier = Canvas(frame_grafo_javier, width=600, height=600)
    canvas_javier.pack(side=RIGHT, padx=80, pady=60)
    leyendaJavier = Label(frame_grafo_javier, text="Leyenda: \nCalle Comercial: 8 minutos\nMala Acera: 6 minutos\nNormal: 4 minutos\n Ruta Óptima: Rojo")
    leyendaJavier.pack(side = BOTTOM,  pady=10, padx = 20)
    texto_javier = Text(frame_grafo_javier, width=50, height=5)
    texto_javier.pack(side=LEFT, padx=10, pady=10)
    dibujar_mapa(canvas_javier, cuadricula, javier, andreina, stablishments, javier)

    ventana.mainloop()

# Función principal
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

    init_app(cuadricula, javier, andreina, stablishments)

main()