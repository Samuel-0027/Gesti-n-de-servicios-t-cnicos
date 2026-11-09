import tkinter as tk
from tkinter import ttk, messagebox
from Modelos import GestorTaller

class InterfazTaller:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Servicios Técnicos")
        ancho_ventana = 900
        alto_ventana = 500
        x = (root.winfo_screenwidth() - ancho_ventana) // 2
        y = (root.winfo_screenheight() - alto_ventana) // 2
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")
        
        self.gestor = GestorTaller()

        # Sistema de pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Creación de los marcos para cada pestaña
        self.tab_recepcion = ttk.Frame(self.notebook)
        self.tab_taller = ttk.Frame(self.notebook)
        self.tab_pendientes = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_recepcion, text="1. Recepción (Clientes y Equipos)")
        self.notebook.add(self.tab_taller, text="2. Taller (Estados y Repuestos)")
        self.notebook.add(self.tab_pendientes, text="3. Reparaciones Pendientes")

        self.armar_pestana_recepcion()
        self.armar_pestana_taller()
        self.armar_pestana_pendientes()

        # Evento para actualizar tablas al cambiar de pestaña
        self.notebook.bind("<<NotebookTabChanged>>", self.actualizar_tablas)

    def armar_pestana_recepcion(self):
        contenedor = ttk.Frame(self.tab_recepcion)
        contenedor.pack(fill="both", expand=True)
        contenedor.grid_rowconfigure(0, weight=1)
        contenedor.grid_columnconfigure(0, weight=1)

        marco = tk.LabelFrame(contenedor, text="Datos del Ingreso")
        marco.grid(row=0, column=0, padx=20, pady=20)
        validar_nombre = (self.root.register(self.permite_nombre), "%P")
        validar_telefono = (self.root.register(self.permite_telefono), "%P")

        # Entradas (Inputs)
        tk.Label(marco, text="Cliente:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_cliente = tk.Entry(marco, validate="key", validatecommand=validar_nombre)
        self.ent_cliente.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(marco, text="Teléfono:").grid(row=0, column=2, padx=5, pady=5)
        self.ent_telefono = tk.Entry(marco, validate="key", validatecommand=validar_telefono)
        self.ent_telefono.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(marco, text="Equipo (Tipo):").grid(row=1, column=0, padx=5, pady=5)
        self.ent_tipo = tk.Entry(marco)
        self.ent_tipo.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(marco, text="Marca/Modelo:").grid(row=1, column=2, padx=5, pady=5)
        self.ent_marca = tk.Entry(marco)
        self.ent_marca.grid(row=1, column=3, padx=5, pady=5)

        tk.Label(marco, text="Falla:").grid(row=2, column=0, padx=5, pady=5)
        self.ent_falla = tk.Entry(marco)
        self.ent_falla.grid(row=2, column=1, columnspan=3, sticky="we", padx=5, pady=5)

        btn_guardar = tk.Button(contenedor, text="Registrar y Generar Orden", command=self.guardar_ingreso)
        btn_guardar.grid(row=1, column=0, pady=(0, 20))

    def armar_pestana_taller(self):
        self.tree_taller = ttk.Treeview(self.tab_taller, columns=("ID", "Cliente", "Equipo", "Falla", "Estado", "Repuestos"), show="headings")
        for col in self.tree_taller["columns"]:
            self.tree_taller.heading(col, text=col)
            self.tree_taller.column(col, width=100 if col != "Repuestos" else 150)
        self.tree_taller.pack(fill="x", padx=10, pady=10)

        marco_acciones = tk.Frame(self.tab_taller)
        marco_acciones.pack(fill="x", padx=10)

        # Sección de Estados
        tk.Label(marco_acciones, text="Nuevo Estado:").grid(row=0, column=0, padx=5)
        self.combo_estado = ttk.Combobox(marco_acciones, values=["Pendiente", "En Proceso", "Reparado", "Entregado"], state="readonly")
        self.combo_estado.grid(row=0, column=1, padx=5)
        tk.Button(marco_acciones, text="Actualizar Estado", command=self.cambiar_estado).grid(row=0, column=2, padx=5)

        # Sección de Repuestos
        tk.Label(marco_acciones, text="Repuesto a registrar:").grid(row=1, column=0, padx=5, pady=15)
        self.ent_repuesto = tk.Entry(marco_acciones)
        self.ent_repuesto.grid(row=1, column=1, padx=5)
        tk.Button(marco_acciones, text="Añadir Repuesto", command=self.agregar_repuesto).grid(row=1, column=2, padx=5)

        tk.Button(marco_acciones, text="Editar datos", command=self.editar_orden).grid(row=2, column=0, padx=5, pady=10)
        tk.Button(marco_acciones, text="Eliminar orden", command=self.eliminar_orden).grid(row=2, column=1, padx=5, pady=10)

    def armar_pestana_pendientes(self):
        self.tree_pendientes = ttk.Treeview(self.tab_pendientes, columns=("ID", "Cliente", "Equipo", "Falla"), show="headings")
        for col in self.tree_pendientes["columns"]:
            self.tree_pendientes.heading(col, text=col)
            self.tree_pendientes.column(col, width=150)
        self.tree_pendientes.pack(fill="both", expand=True, padx=10, pady=10)

    # --- Lógica de los botones ---
    @staticmethod
    def permite_nombre(valor):
        return all(caracter.isalpha() or caracter in " '-" for caracter in valor)

    @staticmethod
    def permite_telefono(valor):
        return all("0" <= caracter <= "9" for caracter in valor)

    @staticmethod
    def nombre_valido(valor):
        return bool(valor.strip()) and any(caracter.isalpha() for caracter in valor) and InterfazTaller.permite_nombre(valor)

    def guardar_ingreso(self):
        nombre = self.ent_cliente.get().strip()
        telefono = self.ent_telefono.get()
        if not self.nombre_valido(nombre) or not self.ent_tipo.get().strip():
            messagebox.showwarning("Error", "Faltan datos obligatorios.")
            return
        if telefono and not self.permite_telefono(telefono):
            messagebox.showwarning("Error", "El teléfono solo puede contener números.")
            return

        self.gestor.registrar_ingreso(
            nombre, telefono,
            self.ent_tipo.get(), self.ent_marca.get(), self.ent_falla.get()
        )
        messagebox.showinfo("Éxito", "Orden creada en memoria.")
        self.actualizar_tablas()
        
        # Limpiar campos
        for widget in [self.ent_cliente, self.ent_telefono, self.ent_tipo, self.ent_marca, self.ent_falla]:
            widget.delete(0, tk.END)

    def obtener_id_seleccionado(self, treeview):
        seleccion = treeview.selection()
        if not seleccion:
            messagebox.showwarning("Error", "Seleccione una orden de la lista primero.")
            return None
        return int(treeview.item(seleccion[0], "values")[0])

    def cambiar_estado(self):
        id_orden = self.obtener_id_seleccionado(self.tree_taller)
        nuevo_estado = self.combo_estado.get()
        if id_orden and nuevo_estado:
            self.gestor.actualizar_estado(id_orden, nuevo_estado)
            messagebox.showinfo("Éxito", f"Estado actualizado a {nuevo_estado}")
            self.actualizar_tablas()

    def agregar_repuesto(self):
        id_orden = self.obtener_id_seleccionado(self.tree_taller)
        repuesto = self.ent_repuesto.get()
        if id_orden and repuesto:
            self.gestor.registrar_repuesto(id_orden, repuesto)
            messagebox.showinfo("Éxito", f"Repuesto '{repuesto}' añadido a la orden {id_orden}")
            self.ent_repuesto.delete(0, tk.END)
            self.actualizar_tablas()

    def editar_orden(self):
        id_orden = self.obtener_id_seleccionado(self.tree_taller)
        if id_orden is None:
            return
        orden = next((orden for orden in self.gestor.ordenes if orden.id_orden == id_orden), None)
        if orden is None:
            messagebox.showerror("Error", "No se encontró la orden seleccionada.")
            return

        ventana = tk.Toplevel(self.root)
        ventana.withdraw()
        ventana.title(f"Editar orden {id_orden}")
        ventana.transient(self.root)

        marco = ttk.Frame(ventana, padding=15)
        marco.pack(fill="both", expand=True)
        validar_nombre = (self.root.register(self.permite_nombre), "%P")
        validar_telefono = (self.root.register(self.permite_telefono), "%P")
        campos = (
            ("Cliente:", orden.cliente.nombre, "nombre"),
            ("Teléfono:", orden.cliente.telefono, "telefono"),
            ("Equipo (Tipo):", orden.equipo.tipo, "tipo"),
            ("Marca/Modelo:", orden.equipo.marca, "marca"),
            ("Falla:", orden.equipo.falla, "falla"),
        )
        entradas = {}
        for fila, (etiqueta, valor, campo) in enumerate(campos):
            tk.Label(marco, text=etiqueta).grid(row=fila, column=0, sticky="e", padx=5, pady=5)
            opciones = {}
            if campo == "nombre":
                opciones = {"validate": "key", "validatecommand": validar_nombre}
            elif campo == "telefono":
                opciones = {"validate": "key", "validatecommand": validar_telefono}
            entrada = tk.Entry(marco, width=35, **opciones)
            entrada.insert(0, valor)
            entrada.grid(row=fila, column=1, padx=5, pady=5)
            entradas[campo] = entrada

        def guardar_cambios():
            nombre = entradas["nombre"].get().strip()
            telefono = entradas["telefono"].get()
            tipo_equipo = entradas["tipo"].get().strip()
            if not self.nombre_valido(nombre) or not tipo_equipo:
                messagebox.showwarning("Error", "El cliente y el tipo de equipo son obligatorios.", parent=ventana)
                return
            if telefono and not self.permite_telefono(telefono):
                messagebox.showwarning("Error", "El teléfono solo puede contener números.", parent=ventana)
                return

            actualizada = self.gestor.actualizar_datos(
                id_orden,
                nombre,
                telefono,
                tipo_equipo,
                entradas["marca"].get().strip(),
                entradas["falla"].get().strip(),
            )
            if not actualizada:
                messagebox.showerror("Error", "No se pudo encontrar la orden para actualizarla.", parent=ventana)
                return
            self.actualizar_tablas()
            ventana.destroy()

        tk.Button(marco, text="Guardar cambios", command=guardar_cambios).grid(
            row=len(campos), column=0, columnspan=2, pady=10
        )
        ventana.update_idletasks() 
        ancho = ventana.winfo_reqwidth()
        alto = ventana.winfo_reqheight()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - ancho) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - alto) // 2
        ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
        ventana.deiconify()
        ventana.lift()
        ventana.grab_set()
        ventana.focus_set()

    def eliminar_orden(self):
        id_orden = self.obtener_id_seleccionado(self.tree_taller)
        if id_orden is None:
            return
        confirmar = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Desea eliminar la orden {id_orden}?",
            parent=self.root,
        )
        if not confirmar:
            return
        if not self.gestor.eliminar_orden(id_orden):
            messagebox.showerror("Error", "No se encontró la orden para eliminarla.")
            return
        self.actualizar_tablas()

    def actualizar_tablas(self, event=None):
        # Limpiar ambas tablas
        for row in self.tree_taller.get_children(): self.tree_taller.delete(row)
        for row in self.tree_pendientes.get_children(): self.tree_pendientes.delete(row)

        # Llenar Taller (Todas las órdenes)
        for orden in self.gestor.ordenes:
            self.tree_taller.insert("", tk.END, values=(
                orden.id_orden, orden.cliente.nombre, 
                f"{orden.equipo.tipo} {orden.equipo.marca}", 
                orden.equipo.falla, orden.estado, ", ".join(orden.repuestos)
            ))

        # Llenar Pendientes (Solo pendientes)
        for orden in self.gestor.obtener_pendientes():
            self.tree_pendientes.insert("", tk.END, values=(
                orden.id_orden, orden.cliente.nombre, 
                f"{orden.equipo.tipo} {orden.equipo.marca}", 
                orden.equipo.falla
            ))

if __name__ == "__main__":
    ventana = tk.Tk()
    app = InterfazTaller(ventana)
    ventana.mainloop()