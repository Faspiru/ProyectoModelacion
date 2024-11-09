# Clase para representar a una persona y sus tiempos de recorrido
class Person:
    def __init__(self, nombre, tiempo_normal, tiempo_mala_acera, tiempo_calle_comercial, home_coords):
        self.nombre = nombre
        self.tiempo_normal = tiempo_normal
        self.tiempo_mala_acera = tiempo_mala_acera
        self.tiempo_calle_comercial = tiempo_calle_comercial
        self.home_coords = home_coords

    def obtener_tiempo(self, origen, destino):
        calle_origen, carrera_origen = origen
        calle_destino, carrera_destino = destino
        
        if calle_origen == calle_destino:  # Movimiento en sentido de calle
            if calle_origen == 51 or calle_destino == 51:
                return self.tiempo_calle_comercial
            else:
                return self.tiempo_normal
        elif carrera_origen == carrera_destino:  # Movimiento en sentido de carrera
            if carrera_origen in {12, 13, 14} or carrera_destino in {12, 13, 14}:
                return self.tiempo_mala_acera
            else:
                return self.tiempo_normal
        return float('inf')  # En caso de un movimiento no permitido