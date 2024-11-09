from main import *
import tkinter as tk

# Función para dibujar el mapa en la cuadrícula, incluyendo las calles, carreras y pesos
def dibujar_mapa(canvas):
    # Ajustes del mapa
    tam_punto = 5  # Tamaño del punto en la cuadrícula
    escala = 50  # Escala para el tamaño de la cuadrícula en píxeles
    offset_x, offset_y = 50, 50  # Desplazamiento para centrar la cuadrícula en el canvas

    # Dibujar la cuadrícula de intersecciones y líneas de calles/carreras
    for calle in range(LIMITE_SUR, LIMITE_NORTE + 1):
        for carrera in range(LIMITE_ESTE, LIMITE_OESTE + 1):
            x = offset_x + (carrera - LIMITE_ESTE) * escala
            y = offset_y + (LIMITE_NORTE - calle) * escala

            # Dibujar el punto de intersección
            canvas.create_oval(x - tam_punto, y - tam_punto, x + tam_punto, y + tam_punto, fill="blue")

            # Etiquetas especiales
            if (calle, carrera) == CASA_JAVIER:
                canvas.create_text(x, y - 15, text="J", fill="red", font=("Arial", 10, "bold"))
            elif (calle, carrera) == CASA_ANDREINA:
                canvas.create_text(x, y - 15, text="A", fill="red", font=("Arial", 10, "bold"))

            # Etiquetar establecimientos
            for nombre, ubicacion in establecimientos.items():
                if ubicacion == (calle, carrera):
                    canvas.create_text(x, y + 15, text=nombre, fill="green", font=("Arial", 10, "bold"))

            grafo = construir_grafo("Andreina")
            # Dibujar las conexiones con pesos entre intersecciones (calles y carreras)
            if (calle, carrera + 1) in grafo[(calle, carrera)]:  # Conexión hacia la derecha
                x_dest = offset_x + (carrera + 1 - LIMITE_ESTE) * escala
                y_dest = y
                peso = grafo[(calle, carrera)][(calle, carrera + 1)]
                canvas.create_line(x, y, x_dest, y_dest, fill="gray")
                canvas.create_text((x + x_dest) / 2, y - 10, text=str(peso), fill="black", font=("Arial", 8))

            if (calle + 1, carrera) in grafo[(calle, carrera)]:  # Conexión hacia abajo
                x_dest = x
                y_dest = offset_y + (LIMITE_NORTE - (calle + 1)) * escala
                peso = grafo[(calle, carrera)][(calle + 1, carrera)]
                canvas.create_line(x, y, x_dest, y_dest, fill="gray")
                canvas.create_text(x - 10, (y + y_dest) / 2, text=str(peso), fill="black", font=("Arial", 8))

# Configuración de la ventana de Tkinter
ventana = tk.Tk()
ventana.title("Mapa de la Ciudad")

# Crear canvas para el mapa
canvas = tk.Canvas(ventana, width=600, height=600)
canvas.pack()

# Dibujar el mapa al iniciar
dibujar_mapa(canvas)

# Ejecutar la aplicación
ventana.mainloop()