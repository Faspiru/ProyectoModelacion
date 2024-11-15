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
        texto_javier.config(state="normal")
        texto_javier.delete(1.0, END)
        texto_javier.insert(END, f"Camino de Javier: {camino_javier}\n\nTiempo: {tiempo_javier} minutos")
        texto_javier.config(state="disabled")
        
        texto_andreina.config(state="normal")
        texto_andreina.delete(1.0, END)
        texto_andreina.insert(END, f"Camino de Andreina: {camino_andreina}\n\nTiempo: {tiempo_andreina} minutos")
        texto_andreina.config(state="disabled")

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


from tkinter import messagebox

def add_stablishment(stablishment_name, coords, stablishments, cuadricula):

    # Convertir las coordenadas a una tupla de enteros
    coords = (int(coords[0]), int(coords[1]))

    # Verificar si ya existe un establecimiento en las mismas coordenadas
    for stablishment in stablishments:
        if stablishment.coords == coords:
            messagebox.showwarning("Advertencia", f"Ya existe el establecimiento: {stablishment.name} en las coordenadas {coords}")
            return
    
    # Agregar el nuevo establecimiento si no hay conflicto de coordenadas
    new_stablishment = Stablishment(stablishment_name, coords)
    stablishments.append(new_stablishment)
    messagebox.showinfo("Resultados", f"Establecimiento '{stablishment_name}' agregado en {coords} con exito")


def remove_stablishment(stablishment_name, stablishments):
    establecimiento = None
    for stablishment in stablishments:
        if stablishment.name == stablishment_name:
            establecimiento = stablishment
    
    if establecimiento == None:
        print("No se ha encontrado el establecimiento a eliminar")
    else:
        stablishments.remove(establecimiento)

def find_establecimiento(stablishment_name, stablishments):
    for stablishment in stablishments:
        if stablishment.name == stablishment_name:
            return stablishment
    return None

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
    tam_punto = 7.5
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

            canvas.create_line(x1, y1, x2, y2, fill=color, width="3")
            canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(peso), fill="black", font=("Arial", 10))

    # Dibujar las etiquetas de las calles y carreras
    for carrera in range(cuadricula.limite_este, cuadricula.limite_oeste + 1):
        x = offset_x + (carrera - cuadricula.limite_este) * escala
        canvas.create_text(x, offset_y - 20, text=f"{carrera}", fill="black", font=("Arial", 12, "bold"))

    for calle in range(cuadricula.limite_sur, cuadricula.limite_norte + 1):
        y = offset_y + (cuadricula.limite_norte - calle) * escala
        canvas.create_text(offset_x - 40, y, text=f"{calle}", fill="black", font=("Arial", 12, "bold"))

    # Dibujar la cuadrícula de intersecciones y etiquetas especiales
    for calle in range(cuadricula.limite_sur, cuadricula.limite_norte + 1):
        for carrera in range(cuadricula.limite_este, cuadricula.limite_oeste + 1):
            x = offset_x + (carrera - cuadricula.limite_este) * escala
            y = offset_y + (cuadricula.limite_norte - calle) * escala

            # Dibujar el punto de intersección
            canvas.create_oval(x - tam_punto, y - tam_punto, x + tam_punto, y + tam_punto, fill="blue")

            # Etiquetas especiales
            if (calle, carrera) == javier.home_coords:
                canvas.create_text(x, y - 15, text="Javier", fill="red", font=("Arial", 10, "bold"))
            elif (calle, carrera) == andreina.home_coords:
                canvas.create_text(x, y - 15, text="Andreina", fill="yellow", font=("Arial", 10, "bold"))

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
    messagebox.showinfo("Resultados", "Carrera agregada con exito")

def add_calle_and_update(canvas_andreina, canvas_javier, cuadricula, javier, andreina, stablishments):
    add_calle(cuadricula)
    update_map([canvas_andreina, canvas_javier], cuadricula, javier, andreina, stablishments, [andreina, javier])
    messagebox.showinfo("Resultados", "Calle agregada con exito")

def remove_carrera_and_update(canvas_andreina, canvas_javier, cuadricula, javier, andreina, stablishments):
    # Posiciones protegidas: casas de Javier y Andreina
    casas = {javier.home_coords[1], andreina.home_coords[1]}  # Solo carreras
    # Posiciones protegidas: establecimientos
    establecimientos = {s.coords[1] for s in stablishments}

    # Verificar si la carrera en el límite oeste coincide con alguna casa o establecimiento
    if cuadricula.limite_oeste in casas:
        messagebox.showwarning("Advertencia", "Para efectos del proyecto, esta carrera no se puede eliminar porque ahí vive uno de los dos actores principales del enunciado.")
        return
    elif cuadricula.limite_oeste in establecimientos:
        messagebox.showwarning("Advertencia", "No se puede eliminar la carrera porque hay un establecimiento. Primero elimínalo e intenta de nuevo.")
        return
    
    # Eliminar carrera y actualizar el mapa
    cuadricula.remove_carrera()
    update_map([canvas_andreina, canvas_javier], cuadricula, javier, andreina, stablishments, [andreina, javier])
    messagebox.showinfo("Resultados", "Carrera eliminada con exito")

def remove_calle_and_update(canvas_andreina, canvas_javier, cuadricula, javier, andreina, stablishments):
    # Posiciones protegidas: casas de Javier y Andreina
    casas = {javier.home_coords[0], andreina.home_coords[0]}  # Solo calles
    # Posiciones protegidas: establecimientos
    establecimientos = {s.coords[0] for s in stablishments}

    # Verificar si la calle en el límite norte coincide con alguna casa o establecimiento
    if cuadricula.limite_norte in casas:
        messagebox.showwarning("Advertencia", "Para efectos del proyecto, esta calle no se puede eliminar porque ahí vive uno de los dos actores principales del enunciado.")
        return
    elif cuadricula.limite_norte in establecimientos:
        messagebox.showwarning("Advertencia", "No se puede eliminar la calle porque hay un establecimiento. Primero elimínalo e intenta de nuevo.")
        return
    
    # Eliminar calle y actualizar el mapa
    cuadricula.remove_calle()
    update_map([canvas_andreina, canvas_javier], cuadricula, javier, andreina, stablishments, [andreina, javier])
    messagebox.showinfo("Resultados", "Calle eliminada con exito")

# Lista desplegable de establecimientos
def update_stablishment_combobox(combobox, stablishments):
    combobox['values'] = [stablishment.name for stablishment in stablishments]
    if stablishments:
        combobox.current(0)  # Seleccionar el primer establecimiento por defecto

def add_stablishment_and_update(canvas_andreina, canvas_javier, comboboxes, stablishment_name, coords, stablishments, cuadricula, javier, andreina):
    if not stablishment_name.strip():
        messagebox.showwarning("Advertencia", "El nombre del establecimiento no puede estar vacío")
        return

    if coords[0].isnumeric() == False or coords[1].isnumeric() == False:
        messagebox.showwarning("Advertencia", "Ambas cordenadas deben ser valores numéricos")
        return
    
    if int(coords[0]) < cuadricula.limite_sur or int(coords[0]) > cuadricula.limite_norte or int(coords[1]) < cuadricula.limite_este or int(coords[1]) > cuadricula.limite_oeste:
        messagebox.showwarning("Advertencia", f"Error: Las coordenadas {coords} están fuera de los límites de la cuadrícula. No se puede agregar el establecimiento")
        return

    add_stablishment(stablishment_name, coords, stablishments, cuadricula)
    for combobox in comboboxes:
        update_stablishment_combobox(combobox, stablishments)
    update_map([canvas_andreina, canvas_javier], cuadricula, javier, andreina, stablishments, [andreina, javier])

def remove_stablishment_and_update(canvas_andreina, canvas_javier, cuadricula, javier, andreina, comboboxes, stablishment_name, stablishments):
    remove_stablishment(stablishment_name, stablishments)
    for combobox in comboboxes:
        update_stablishment_combobox(combobox, stablishments)
    messagebox.showinfo("Resultados", "Establecimiento agregado con exito")
    update_map([canvas_andreina, canvas_javier], cuadricula, javier, andreina, stablishments, [andreina, javier])

def edit_stablishment(stablishment, new_stablishment_name, new_location):

    if new_location[0].isnumeric() == False or new_location[1].isnumeric() == False:
        messagebox.showwarning("Advertencia", "Las coordenadas deben ser valores numéricos")
        return
    stablishment.name = new_stablishment_name
    stablishment.coords = (int(new_location[0]), int(new_location[1]))

def edit_stablishment_and_update(canvas_andreina, canvas_javier, cuadricula, javier, andreina, comboboxes, stablishment, new_stablishment_name, new_location: tuple, stablishments):
    edit_stablishment(stablishment, new_stablishment_name, new_location)
    for combobox in comboboxes:
        update_stablishment_combobox(combobox, stablishments)
    messagebox.showinfo("Resultados", "Establecimiento editado con exito")
    update_map([canvas_andreina, canvas_javier], cuadricula, javier, andreina, stablishments, [andreina, javier])

def edit_person(person, avenueTime, dangerTime, streetTime, home_coords, cuadricula, canvases, javier, andreina, stablishments):

    if avenueTime.isnumeric() == False or dangerTime.isnumeric() == False or streetTime.isnumeric() == False:
        messagebox.showwarning("Advertencia", "Los tiempos deben ser valores numéricos")
        return

    if home_coords[0].isnumeric() == False or home_coords[1].isnumeric() == False:
        messagebox.showwarning("Advertencia", "Las coordenadas de la casa deben ser valores numéricos")
        return

    if int(home_coords[0]) < cuadricula.limite_sur or int(home_coords[0]) > cuadricula.limite_norte or int(home_coords[1]) < cuadricula.limite_este or int(home_coords[1]) > cuadricula.limite_oeste:
        messagebox.showwarning("Advertencia", "Las coordenadas de la casa deben estar dentro de los límites de la cuadrícula")
        return

    if int(avenueTime) <= 0 or int(dangerTime) <= 0 or int(streetTime) <= 0:
        messagebox.showwarning("Advertencia", "Los tiempos deben ser mayores a cero")
        return
    
    # Validación de que la posición de la casa no esté ocupada por Javier o Andreina
    nueva_home_coords = (int(home_coords[0]), int(home_coords[1]))
    if person.nombre =="Andreina" and nueva_home_coords == javier.home_coords:
        messagebox.showwarning("Advertencia", "La posición ya está siendo ocupada por Javier")
        return
    
    if person.nombre =="Javier" and nueva_home_coords == andreina.home_coords:
        messagebox.showwarning("Advertencia", "La posición ya está siendo ocupada por Andreina")
        return
    
    
    person.tiempo_normal = int(streetTime)
    person.tiempo_mala_acera = int(dangerTime)
    person.tiempo_calle_comercial = int(avenueTime)
    person.home_coords = (int(home_coords[0]), int(home_coords[1]))

    messagebox.showinfo("Resultados", "Persona editada con exito")

    update_map(canvases, cuadricula, javier, andreina, stablishments, [andreina, javier])


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

    #Cuarta Pestaña - Editar Personas
    frame_editar_personas = Frame(notebook)
    notebook.add(frame_editar_personas, text="Editar Personas")

    #Quinta Pestaña - Añadir o Eliminar Establecimientos
    frame_editar_establecimientos = Frame(notebook)
    notebook.add(frame_editar_establecimientos, text="Establecimientos")

    # Combobox para establecimientos en la pestaña de opciones
    combobox1 = ttk.Combobox(frame_botones, width=25)
    combobox1.pack(pady=5)
    update_stablishment_combobox(combobox1, stablishments)



    # Configurar las columnas del frame de botones
    frame_botones.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
    combobox1.grid(row=1, column=1, columnspan=5, pady=5)
    Button(frame_botones, text="Calcular trayectoria", command=lambda: calcular_ruta(combobox1.get(), stablishments, cuadricula, javier, andreina, canvas_javier, canvas_andreina, texto_javier, texto_andreina)).grid(row=0, column=0, sticky="ew", padx=100, pady=25)
    Button(frame_botones, text="Agregar calle", command=lambda: add_calle_and_update(canvas_andreina, canvas_javier, cuadricula, javier, andreina, stablishments)).grid(row=1, column=0, sticky="ew", padx=100, pady=25)
    Button(frame_botones, text="Eliminar calle", command=lambda: remove_calle_and_update(canvas_andreina, canvas_javier, cuadricula, javier, andreina, stablishments)).grid(row=2, column=0, sticky="ew", padx=100, pady=25)
    Button(frame_botones, text="Agregar carrera", command=lambda: add_carrera_and_update(canvas_andreina, canvas_javier, cuadricula, javier, andreina, stablishments)).grid(row=3, column=0, sticky="ew", padx=100, pady=25)
    Button(frame_botones, text="Eliminar carrera", command=lambda: remove_carrera_and_update(canvas_andreina, canvas_javier, cuadricula, javier, andreina, stablishments)).grid(row=4, column=0, sticky="ew", padx=100, pady=25)

    #Cuadricula de Andreina
    canvas_andreina = Canvas(frame_grafo_andreina, width=600, height=600)
    canvas_andreina.pack(side=RIGHT, padx=10, pady=60)
    texto_andreina = Text(frame_grafo_andreina, width=100, height=10)
    leyendaAndreina = Label(frame_grafo_andreina, text="Leyenda: \nCalle Comercial: 10 minutos\nMala Acera: 8 minutos\nNormal: 6 minutos\n Ruta Óptima: Amarillo")
    leyendaAndreina.pack(side = BOTTOM,  pady=10)
    texto_andreina.pack(side=LEFT, anchor=CENTER, fill=X ,padx=20, pady=10)
    texto_andreina.config(state="disabled")
    dibujar_mapa(canvas_andreina, cuadricula, javier, andreina, stablishments, andreina)

    #Cuadricula de Javier
    canvas_javier = Canvas(frame_grafo_javier, width=600, height=600)
    canvas_javier.pack(side=RIGHT, padx=10, pady=60)
    leyendaJavier = Label(frame_grafo_javier, text="Leyenda: \nCalle Comercial: 8 minutos\nMala Acera: 6 minutos\nNormal: 4 minutos\n Ruta Óptima: Rojo")
    leyendaJavier.pack(side = BOTTOM,  pady=10)
    texto_javier = Text(frame_grafo_javier, width=100, height=10)
    texto_javier.pack(side=LEFT, anchor=CENTER, fill=X ,padx=20, pady=10)
    texto_javier.config(state="disabled")
    dibujar_mapa(canvas_javier, cuadricula, javier, andreina, stablishments, javier)

    #Editar Personas
    Label(frame_editar_personas, text="Editar Personas").grid(row=0, column=0, columnspan=5, pady=10)
    Label(frame_editar_personas, text="Javier").grid(row=1, column=0, pady=10, padx=120)
    Label(frame_editar_personas, text="Tiempo Calle Comercial").grid(row=2, column=0, pady=10)
    Label(frame_editar_personas, text="Tiempo Mala Acera").grid(row=3, column=0, pady=10)
    Label(frame_editar_personas, text="Tiempo Normal").grid(row=4, column=0, pady=10)
    Label(frame_editar_personas, text="Calle donde vive").grid(row=5, column=0, pady=10)
    Label(frame_editar_personas, text="Carrera donde vive").grid(row=6, column=0, pady=10)


    entry_javier_avenue = Entry(frame_editar_personas)
    entry_javier_avenue.grid(row=2, column=1)
    entry_javier_avenue.insert(0, javier.tiempo_calle_comercial)
    entry_javier_danger = Entry(frame_editar_personas)
    entry_javier_danger.grid(row=3, column=1)
    entry_javier_danger.insert(0, javier.tiempo_mala_acera)
    entry_javier_street = Entry(frame_editar_personas)
    entry_javier_street.grid(row=4, column=1)
    entry_javier_street.insert(0, javier.tiempo_normal)
    entry_javier_home_street = Entry(frame_editar_personas)
    entry_javier_home_street.grid(row=5, column=1)
    entry_javier_home_street.insert(0, javier.home_coords[0])
    entry_javier_home_avenue = Entry(frame_editar_personas)
    entry_javier_home_avenue.grid(row=6, column=1)
    entry_javier_home_avenue.insert(0, javier.home_coords[1])

    Label(frame_editar_personas, text="Andreina").grid(row=1, column=3, pady=10, padx=30)
    Label(frame_editar_personas, text="Tiempo Calle Comercial").grid(row=2, column=3, pady=10, padx=30)
    Label(frame_editar_personas, text="Tiempo Mala Acera").grid(row=3, column=3, pady=10, padx=30)
    Label(frame_editar_personas, text="Tiempo Normal").grid(row=4, column=3, pady=10, padx=30)
    Label(frame_editar_personas, text="Calle donde vive").grid(row=5, column=3, pady=10, padx=30)
    Label(frame_editar_personas, text="Carrera donde vive").grid(row=6, column=3, pady=10, padx=30)

    entry_andreina_avenue = Entry(frame_editar_personas)
    entry_andreina_avenue.grid(row=2, column=4)
    entry_andreina_avenue.insert(0, andreina.tiempo_calle_comercial)
    entry_andreina_danger = Entry(frame_editar_personas)
    entry_andreina_danger.grid(row=3, column=4)
    entry_andreina_danger.insert(0, andreina.tiempo_mala_acera)
    entry_andreina_street = Entry(frame_editar_personas)
    entry_andreina_street.grid(row=4, column=4)
    entry_andreina_street.insert(0, andreina.tiempo_normal)
    entry_andreina_home_street = Entry(frame_editar_personas)
    entry_andreina_home_street.grid(row=5, column=4)
    entry_andreina_home_street.insert(0, andreina.home_coords[0])
    entry_andreina_home_avenue = Entry(frame_editar_personas)
    entry_andreina_home_avenue.grid(row=6, column=4)
    entry_andreina_home_avenue.insert(0, andreina.home_coords[1])

    Button(frame_editar_personas, text="Editar información Javier", command=lambda: edit_person(javier, entry_javier_avenue.get(), entry_javier_danger.get(), entry_javier_street.get(), [entry_javier_home_street.get(), entry_javier_home_avenue.get()], cuadricula, [canvas_andreina, canvas_javier], javier, andreina, stablishments)).grid(row=7, column=0, columnspan=2, pady=10)

    Button(frame_editar_personas, text="Editar información Andreina", command=lambda: edit_person(andreina, entry_andreina_avenue.get(), entry_andreina_danger.get(), entry_andreina_street.get(), [entry_andreina_home_street.get(), entry_andreina_home_avenue.get()], cuadricula, [canvas_andreina, canvas_javier], javier, andreina, stablishments)).grid(row=7, column=3, columnspan=2, pady=10, padx=30)


    #Añadir, Editar o Eliminar Establecimientos
    #Añadir
    Label(frame_editar_establecimientos, text="Añadir Establecimiento").grid(row=0, column=0, padx= 10, pady=10)
    Label(frame_editar_establecimientos, text="Nombre del Establecimiento").grid(row=1, column=0, padx=10, pady=5)
    entry_new_stablishment = Entry(frame_editar_establecimientos)
    entry_new_stablishment.grid(row=2, column=0, padx=10, pady=5)
    Label(frame_editar_establecimientos, text="Calle").grid(row=3, column=0, padx=10, pady=5)
    entry_new_street = Entry(frame_editar_establecimientos)
    entry_new_street .grid(row=4, column=0, padx=10, pady=5)
    Label(frame_editar_establecimientos, text="Carrera").grid(row=5, column=0, padx=10, pady=5)
    entry_new_avenue = Entry(frame_editar_establecimientos)
    entry_new_avenue .grid(row=6, column=0, padx= 10, pady=5)
    Button(frame_editar_establecimientos, text = "Añadir Establecimiento", command=lambda: add_stablishment_and_update(canvas_andreina, canvas_javier, [combobox1, combobox2, combobox3], entry_new_stablishment.get(), (entry_new_street.get(), entry_new_avenue.get()), stablishments, cuadricula, javier, andreina)).grid(row=7, column=0, padx=10, pady=5)
    

    Label(frame_editar_establecimientos, text="Editar Establecimiento").grid(row=0, column=10, columnspan=5, pady=10)
    Label(frame_editar_establecimientos, text="Seleccionar Establecimiento").grid(row=1, column=10, padx=10, pady=5)
    combobox2 = ttk.Combobox(frame_editar_establecimientos, width=25)
    combobox2.grid(row=1, column=10, columnspan=5, pady=5)    
    update_stablishment_combobox(combobox2, stablishments)

    actual_stablishment = find_establecimiento(combobox2.get(), stablishments)

    def update_entries(*args):
        actual_stablishment = find_establecimiento(combobox2.get(), stablishments)
        entry_edit_stablishment_name.delete(0, END)
        entry_edit_stablishment_name.insert(0, actual_stablishment.name)
        entry_edit_street.delete(0, END)
        entry_edit_street.insert(0, actual_stablishment.coords[0])
        entry_edit_avenue.delete(0, END)
        entry_edit_avenue.insert(0, actual_stablishment.coords[1])

    combobox2.bind("<<ComboboxSelected>>", update_entries)

    Label(frame_editar_establecimientos, text="Nuevo Nombre del Establecimiento").grid(row=2, column=10, padx=10, pady=5)
    entry_edit_stablishment_name = Entry(frame_editar_establecimientos)
    entry_edit_stablishment_name.grid(row=3, column=10, padx=10, pady=5)
    entry_edit_stablishment_name.insert(0, actual_stablishment.name)
    Label(frame_editar_establecimientos, text="Nueva Calle").grid(row=4, column=10, padx=10, pady=5)
    entry_edit_street = Entry(frame_editar_establecimientos)
    entry_edit_street.grid(row=5, column=10, padx=10, pady=5)
    entry_edit_street.insert(0, actual_stablishment.coords[0])
    Label(frame_editar_establecimientos, text="Nueva Carrera").grid(row=6, column=10, padx=10, pady=5)
    entry_edit_avenue = Entry(frame_editar_establecimientos)
    entry_edit_avenue.grid(row=7, column=10, padx=10, pady=5)
    entry_edit_avenue.insert(0, actual_stablishment.coords[1])
    Button(frame_editar_establecimientos, text="Editar Establecimiento", command=lambda: edit_stablishment_and_update(canvas_andreina, canvas_javier, cuadricula, javier, andreina, [combobox1, combobox2, combobox3], actual_stablishment, entry_edit_stablishment_name.get(), (entry_edit_street.get(), entry_edit_avenue.get()), stablishments)).grid(row=8, column=10, padx=10, pady=5)

    Label(frame_editar_establecimientos, text="Eliminar Establecimiento").grid(row=0, column=20, columnspan=5, pady=10)
    Label(frame_editar_establecimientos, text="Seleccionar Establecimiento").grid(row=1, column=20, padx=10, pady=5)
    combobox3 = ttk.Combobox(frame_editar_establecimientos, width=25)
    combobox3.grid(row=1, column=20, columnspan=5, pady=5)
    update_stablishment_combobox(combobox3, stablishments)
    Button(frame_editar_establecimientos, text="Eliminar Establecimiento", command=lambda: remove_stablishment_and_update(canvas_andreina, canvas_javier, cuadricula, javier, andreina, [combobox1, combobox2, combobox3], combobox3.get(), stablishments)).grid(row=2, column=20, padx=10, pady=5)







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