from tkinter import messagebox

class Cuadricula:
    def __init__(self, limite_norte, limite_sur, limite_este, limite_oeste):
        self.limite_norte = limite_norte
        self.limite_sur = limite_sur
        self.limite_este = limite_este
        self.limite_oeste = limite_oeste

    def construir_grafo(self, persona):
        grafo = {}
        for calle in range(self.limite_sur, self.limite_norte + 1):
            for carrera in range(self.limite_este, self.limite_oeste + 1):
                nodo = (calle, carrera)
                grafo[nodo] = []
                vecinos = [
                    (calle + 1, carrera), (calle - 1, carrera),
                    (calle, carrera + 1), (calle, carrera - 1)
                ]
                
                for vecino in vecinos:
                    if (self.limite_sur <= vecino[0] <= self.limite_norte and 
                        self.limite_este <= vecino[1] <= self.limite_oeste):
                        tiempo = persona.obtener_tiempo(nodo, vecino)
                        grafo[nodo].append((vecino, tiempo))
        return grafo
    
        # Método para agregar una calle al límite norte
    def add_calle(self):
        self.limite_norte += 1
        print(f"Límite norte aumentado a {self.limite_norte}")

    # Método para quitar una calle del límite norte
    def remove_calle(self):
        if self.limite_norte > self.limite_sur:
            self.limite_norte -= 1
            print(f"Límite norte reducido a {self.limite_norte}")
        else:
            messagebox.showwarning("Advertencia", "No se puede reducir más el límite norte")
            print("No se puede reducir más el límite norte")

    # Método para agregar una carrera al límite oeste
    def add_carrera(self):
        self.limite_oeste += 1
        print(f"Límite oeste aumentado a {self.limite_oeste}")

    # Método para quitar una carrera del límite oeste
    def remove_carrera(self):
        if self.limite_oeste > self.limite_este:
            self.limite_oeste -= 1
            print(f"Límite oeste reducido a {self.limite_oeste}")
        else:
            messagebox.showwarning("Advertencia", "No se puede reducir más el límite oeste")
            print("No se puede reducir más el límite oeste")
