class Cliente:
    def __init__(self, nombre, telefono):
        self.nombre = nombre
        self.telefono = telefono

class Equipo:
    def __init__(self, tipo, marca, falla):
        self.tipo = tipo
        self.marca = marca
        self.falla = falla

class OrdenTrabajo:
    def __init__(self, id_orden, cliente, equipo):
        self.id_orden = id_orden
        self.cliente = cliente
        self.equipo = equipo
        self.estado = "Pendiente"
        self.repuestos = []

class GestorTaller:
    def __init__(self):
        self.ordenes = []
        self.contador_id = 1

    # Cubre: Registrar clientes/equipos y Crear órdenes
    def registrar_ingreso(self, nombre, telefono, tipo_eq, marca, falla):
        nuevo_cliente = Cliente(nombre, telefono)
        nuevo_equipo = Equipo(tipo_eq, marca, falla)
        nueva_orden = OrdenTrabajo(self.contador_id, nuevo_cliente, nuevo_equipo)
        
        self.ordenes.append(nueva_orden)
        self.contador_id += 1
        return nueva_orden

    # Cubre: Asignar estados
    def actualizar_estado(self, id_orden, nuevo_estado):
        for orden in self.ordenes:
            if orden.id_orden == id_orden:
                orden.estado = nuevo_estado
                return True
        return False

    # Cubre: Registrar repuestos
    def registrar_repuesto(self, id_orden, repuesto):
        for orden in self.ordenes:
            if orden.id_orden == id_orden:
                orden.repuestos.append(repuesto)
                return True
        return False

    def actualizar_datos(self, id_orden, nombre, telefono, tipo_eq, marca, falla):
        for orden in self.ordenes:
            if orden.id_orden == id_orden:
                orden.cliente.nombre = nombre
                orden.cliente.telefono = telefono
                orden.equipo.tipo = tipo_eq
                orden.equipo.marca = marca
                orden.equipo.falla = falla
                return True
        return False

    def eliminar_orden(self, id_orden):
        for indice, orden in enumerate(self.ordenes):
            if orden.id_orden == id_orden:
                del self.ordenes[indice]
                return True
        return False

    # Cubre: Consultar reparaciones pendientes
    def obtener_pendientes(self):
        return [orden for orden in self.ordenes if orden.estado == "Pendiente"]