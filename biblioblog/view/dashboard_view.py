import customtkinter as ctk
from tkinter import messagebox, simpledialog, ttk
import tkinter as tk

class DashboardView(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.configure(fg_color=("#f0f0f0", "#1a1a1a"))

        # Crear menú superior
        self.crear_menu_superior()

        # Crear contenido principal con tabs
        self.crear_tabs()

        if controller.rol_actual == "propietario":
            self.crear_tabs_propietario()
        else:
            self.crear_tabs_cliente()

    def crear_menu_superior(self):
        """Crea la barra superior con título y botón de logout"""
        top_frame = ctk.CTkFrame(self, fg_color=("#e0e0e0", "#2a2a2a"), height=60)
        top_frame.pack(fill="x", padx=0, pady=0)
        top_frame.grid_propagate(False)

        # Título
        titulo = ctk.CTkLabel(
            top_frame,
            text=f" BiblioBlog - {self.controller.rol_actual.title()}",
            font=("Arial", 18, "bold")
        )
        titulo.pack(side="left", padx=20, pady=10)

        # Info del usuario
        info_label = ctk.CTkLabel(
            top_frame,
            text=f"Sesión: {self.controller.usuario_actual}",
            font=("Arial", 11),
            text_color=("gray60", "gray70")
        )
        info_label.pack(side="left", padx=10)

        # Botón Volver a Login (Cerrar Sesión)
        logout_btn = ctk.CTkButton(
            top_frame,
            text="Volver al Login",
            command=self.logout,
            width=130,
            height=35,
            font=("Arial", 10, "bold"),
            fg_color=("#dc3545", "#dc3545")
        )
        logout_btn.pack(side="right", padx=(10, 5), pady=10)

        # Botón Salir
        salir_btn = ctk.CTkButton(
            top_frame,
            text="Salir",
            command=self.parent.destroy,
            width=100,
            height=35,
            font=("Arial", 10, "bold"),
            fg_color=("#ff5722", "#ff5722")
        )
        salir_btn.pack(side="right", padx=(5, 20), pady=10)

    def crear_tabs(self):
        """Crea el sistema de tabs"""
        self.tab_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.tab_frame.pack(fill="both", expand=True, padx=0, pady=0)

    def crear_tabs_cliente(self):
        """Crea las tabs para clientes"""
        # Frame para los botones de tab
        tab_buttons_frame = ctk.CTkFrame(self.tab_frame, fg_color=("#e0e0e0", "#2a2a2a"), height=50)
        tab_buttons_frame.pack(fill="x", padx=0, pady=0)
        tab_buttons_frame.grid_propagate(False)

        self.tab_buttons = {}
        tabs = [
            ("Libros", self.mostrar_tab_libros),
            ("Mis Préstamos", self.mostrar_tab_mis_prestamos),
            ("Búsqueda", self.mostrar_tab_busqueda),
            ("Mi Perfil", self.mostrar_tab_perfil)
        ]

        for i, (nombre, comando) in enumerate(tabs):
            btn = ctk.CTkButton(
                tab_buttons_frame,
                text=nombre,
                command=comando,
                width=120,
                height=40,
                font=("Arial", 11, "bold"),
                fg_color=("#0078d4" if i == 0 else ("gray70", "gray60")),
                text_color=("white", "white") if i == 0 else ("black", "white")
            )
            btn.pack(side="left", padx=5, pady=5)
            self.tab_buttons[nombre] = btn

        # Frame para el contenido de tabs
        self.content_frame = ctk.CTkFrame(self.tab_frame, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Mostrar primera tab
        self.mostrar_tab_libros()

    def crear_tabs_propietario(self):
        """Crea las tabs para propietarios"""
        # Frame para los botones de tab
        tab_buttons_frame = ctk.CTkFrame(self.tab_frame, fg_color=("#e0e0e0", "#2a2a2a"), height=50)
        tab_buttons_frame.pack(fill="x", padx=0, pady=0)
        tab_buttons_frame.grid_propagate(False)

        self.tab_buttons = {}
        tabs = [
            ("Agregar Libro", self.mostrar_tab_agregar_libro),
            ("Mis Libros", self.mostrar_tab_mis_libros),
            ("Préstamos", self.mostrar_tab_todos_prestamos),
            ("Clientes", self.mostrar_tab_clientes),
            ("Estadísticas", self.mostrar_tab_estadisticas),
            ("Mi Perfil", self.mostrar_tab_perfil_propietario)
        ]

        for i, (nombre, comando) in enumerate(tabs):
            btn = ctk.CTkButton(
                tab_buttons_frame,
                text=nombre,
                command=comando,
                width=120,
                height=40,
                font=("Arial", 11, "bold"),
                fg_color=("#0078d4" if i == 0 else ("gray70", "gray60")),
                text_color=("white", "white") if i == 0 else ("black", "white")
            )
            btn.pack(side="left", padx=5, pady=5)
            self.tab_buttons[nombre] = btn

        # Frame para el contenido de tabs
        self.content_frame = ctk.CTkFrame(self.tab_frame, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Mostrar primera tab
        self.mostrar_tab_agregar_libro()

    def limpiar_content(self):
        """Limpia el frame de contenido"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def cambiar_color_tab(self, tab_nombre):
        """Cambia el color del tab activo"""
        for nombre, btn in self.tab_buttons.items():
            if nombre == tab_nombre:
                btn.configure(fg_color="#0078d4", text_color=("white", "white"))
            else:
                btn.configure(fg_color=("gray70", "gray60"), text_color=("black", "white"))

    # ==================== TABS CLIENTE ====================

    def mostrar_tab_libros(self):
        """Tab de libros disponibles"""
        self.cambiar_color_tab("Libros")
        self.limpiar_content()

        # Título
        ctk.CTkLabel(self.content_frame, text=" Libros Disponibles", font=("Arial", 14, "bold")).pack(pady=(0, 15))

        # Tabla de libros
        self.crear_tabla_libros_cliente(self.content_frame)

    def mostrar_tab_mis_prestamos(self):
        """Tab de mis préstamos"""
        self.cambiar_color_tab("Mis Préstamos")
        self.limpiar_content()

        # Título
        ctk.CTkLabel(self.content_frame, text=" Mis Préstamos", font=("Arial", 14, "bold")).pack(pady=(0, 15))

        # Tabla de préstamos
        self.crear_tabla_prestamos_cliente(self.content_frame)

    def mostrar_tab_busqueda(self):
        """Tab de búsqueda de libros"""
        self.cambiar_color_tab("Búsqueda")
        self.limpiar_content()

        # Título
        ctk.CTkLabel(self.content_frame, text=" Buscar Libros", font=("Arial", 14, "bold")).pack(pady=(0, 15))

        # Frame de búsqueda
        search_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        search_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(search_frame, text="Buscar por título, autor o año:", font=("Arial", 11)).pack(anchor="w", padx=10, pady=(0, 5))
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Ingrese título, autor o año", height=35, width=300)
        self.search_entry.pack(side="left", padx=10)

        ctk.CTkButton(search_frame, text="Buscar", command=self.buscar_libros, width=100, height=35).pack(side="left", padx=5)

        # Frame para resultados
        self.search_results_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        self.search_results_frame.pack(fill="both", expand=True, pady=20)

    def mostrar_tab_perfil(self):
        """Tab de perfil del cliente"""
        self.cambiar_color_tab("Mi Perfil")
        self.limpiar_content()

        ctk.CTkLabel(self.content_frame, text="👤 Mi Perfil", font=("Arial", 14, "bold")).pack(pady=(0, 20))

        # Datos visibles siempre
        ctk.CTkLabel(self.content_frame, text=f"Usuario: {self.controller.usuario_actual}", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(0, 5))
        ctk.CTkLabel(self.content_frame, text=f"Rol: {self.controller.rol_actual.title()}", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(0, 10))

        self.info_visible = False
        self.btn_toggle_info = ctk.CTkButton(
            self.content_frame,
            text="Mostrar mi información",
            command=self.toggle_info_usuario,
            width=220,
            height=40,
            font=("Arial", 11, "bold"),
            fg_color=("#0078d4", "#0078d4")
        )
        self.btn_toggle_info.pack(pady=(0, 20), padx=20, anchor="w")

        # Frame oculto para los datos de correo/teléfono y edición
        self.info_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")


        ctk.CTkButton(
            self.content_frame,
            text="Recuperar Contraseña",
            command=self.recuperar_contraseña,
            width=200,
            height=40,
            font=("Arial", 11, "bold"),
            fg_color=("#ffc107", "#ffc107")
        ).pack(pady=(0, 10), padx=20, anchor="w")

    def toggle_info_usuario(self):
        """Alterna la visibilidad de la información del perfil"""
        if self.info_visible:
            self.info_frame.pack_forget()
            self.btn_toggle_info.configure(text="Mostrar mi información")
            self.info_visible = False
        else:
            self.mostrar_info_detalle()
            self.info_frame.pack(fill="x", padx=20, pady=(0, 20))
            self.btn_toggle_info.configure(text="Ocultar mi información")
            self.info_visible = True

    def mostrar_info_detalle(self):
        """Muestra datos de correo, teléfono y permite editar"""
        for w in self.info_frame.winfo_children():
            w.destroy()

        usuario_info = self.controller.obtener_info_usuario(self.controller.usuario_actual, self.controller.rol_actual)
        correo_actual = usuario_info.get("correo") if usuario_info else ""
        telefono_actual = usuario_info.get("telefono") if usuario_info else ""

        ctk.CTkLabel(self.info_frame, text=f"Nombre de cuenta: {self.controller.usuario_actual}", font=("Arial", 12)).pack(anchor="w", pady=(0, 5))
        ctk.CTkLabel(self.info_frame, text=f"Correo: {correo_actual}", font=("Arial", 12)).pack(anchor="w", pady=(0, 5))
        ctk.CTkLabel(self.info_frame, text=f"Teléfono: {telefono_actual}", font=("Arial", 12)).pack(anchor="w", pady=(0, 10))

        ctk.CTkButton(
            self.info_frame,
            text="Editar mi información",
            command=self.mostrar_formulario_editar,
            width=200,
            height=35,
            font=("Arial", 11, "bold"),
            fg_color=("#17a2b8", "#17a2b8")
        ).pack(pady=(0, 10), anchor="w")

    def mostrar_formulario_editar(self):
        """Muestra campos de edición dentro del info_frame"""
        for w in self.info_frame.winfo_children():
            w.destroy()

        usuario_info = self.controller.obtener_info_usuario(self.controller.usuario_actual, self.controller.rol_actual)
        correo_actual = usuario_info.get("correo") if usuario_info else ""
        telefono_actual = usuario_info.get("telefono") if usuario_info else ""

        ctk.CTkLabel(self.info_frame, text="Correo:", font=("Arial", 12)).pack(anchor="w", pady=(0, 5))
        self.correo_entry = ctk.CTkEntry(self.info_frame, width=300, height=35)
        self.correo_entry.insert(0, correo_actual)
        self.correo_entry.pack(pady=(0, 10), anchor="w")

        ctk.CTkLabel(self.info_frame, text="Teléfono:", font=("Arial", 12)).pack(anchor="w", pady=(0, 5))
        self.telefono_entry = ctk.CTkEntry(self.info_frame, width=300, height=35)
        self.telefono_entry.insert(0, telefono_actual)
        self.telefono_entry.pack(pady=(0, 10), anchor="w")

        ctk.CTkButton(
            self.info_frame,
            text="Guardar cambios",
            command=self.actualizar_perfil,
            width=200,
            height=35,
            font=("Arial", 11, "bold"),
            fg_color=("#28a745", "#28a745")
        ).pack(pady=(0, 10), anchor="w")

    # ==================== TABS PROPIETARIO ====================

    def mostrar_tab_agregar_libro(self):
        """Tab para agregar nuevos libros"""
        self.cambiar_color_tab("Agregar Libro")
        self.limpiar_content()

        titulo = ctk.CTkLabel(self.content_frame, text=" Agregar Nuevo Libro", font=("Arial", 14, "bold"))
        titulo.pack(pady=(0, 20))

        # Frame con inputs
        input_frame = ctk.CTkFrame(self.content_frame, fg_color=("#e8f4f8", "#2a3a3a"), corner_radius=10)
        input_frame.pack(fill="x", padx=20, pady=20)

        # Título
        ctk.CTkLabel(input_frame, text="Título:", font=("Arial", 11)).pack(anchor="w", padx=15, pady=(15, 5))
        self.entrada_titulo = ctk.CTkEntry(input_frame, placeholder_text="Ej: El Quijote", height=30)
        self.entrada_titulo.pack(anchor="w", padx=15, pady=(0, 10), fill="x")

        # Autor
        ctk.CTkLabel(input_frame, text="Autor:", font=("Arial", 11)).pack(anchor="w", padx=15, pady=(5, 5))
        self.entrada_autor = ctk.CTkEntry(input_frame, placeholder_text="Ej: Miguel de Cervantes", height=30)
        self.entrada_autor.pack(anchor="w", padx=15, pady=(0, 10), fill="x")

        # Año
        ctk.CTkLabel(input_frame, text="Año:", font=("Arial", 11)).pack(anchor="w", padx=15, pady=(5, 5))
        self.entrada_anio = ctk.CTkEntry(input_frame, placeholder_text="Ej: 1605", height=30)
        self.entrada_anio.pack(anchor="w", padx=15, pady=(0, 15), fill="x")

        # Botón agregar
        ctk.CTkButton(
            input_frame,
            text="Agregar Libro",
            command=self.agregar_libro,
            width=150,
            height=35,
            font=("Arial", 11, "bold"),
            fg_color=("#28a745", "#28a745")
        ).pack(pady=10)

    def mostrar_tab_mis_libros(self):
        """Tab de libros agregados"""
        self.cambiar_color_tab("Mis Libros")
        self.limpiar_content()

        ctk.CTkLabel(self.content_frame, text=" Libros en la Biblioteca", font=("Arial", 14, "bold")).pack(pady=(0, 15))

        self.crear_tabla_libros_propietario(self.content_frame)

    def mostrar_tab_todos_prestamos(self):
        """Tab de todos los préstamos"""
        self.cambiar_color_tab("Préstamos")
        self.limpiar_content()

        ctk.CTkLabel(self.content_frame, text=" Todos los Préstamos", font=("Arial", 14, "bold")).pack(pady=(0, 15))

        self.crear_tabla_todos_prestamos(self.content_frame)

    def mostrar_tab_clientes(self):
        """Tab de gestión de clientes"""
        self.cambiar_color_tab("Clientes")
        self.limpiar_content()

        ctk.CTkLabel(self.content_frame, text="👥 Gestión de Clientes", font=("Arial", 14, "bold")).pack(pady=(0, 15))

        self.crear_tabla_clientes(self.content_frame)

    def mostrar_tab_estadisticas(self):
        """Tab de estadísticas"""
        self.cambiar_color_tab("Estadísticas")
        self.limpiar_content()

        ctk.CTkLabel(self.content_frame, text=" Estadísticas", font=("Arial", 14, "bold")).pack(pady=(0, 20))

        libros = self.controller.obtener_libros()
        prestamos = self.controller.obtener_todos_prestamos()
        prestamos_activos = [p for p in prestamos if not p["devuelto"]]
        prestamos_vencidos = self.controller.prestamo_model.obtener_prestamos_vencidos()
        clientes = self.controller.obtener_clientes()

        stats = f"""
 ESTADÍSTICAS DEL SISTEMA:

Libros Totales: {len(libros)}
Clientes Registrados: {len(clientes)}
Préstamos Activos: {len(prestamos_activos)}
Préstamos Finalizados: {len(prestamos) - len(prestamos_activos)}
Préstamos Vencidos: {len(prestamos_vencidos)}
        """

        ctk.CTkLabel(
            self.content_frame,
            text=stats,
            font=("Arial", 12),
            justify="left",
            text_color=("gray20", "gray80")
        ).pack(anchor="w", padx=30, pady=20)

    def mostrar_tab_perfil_propietario(self):
        """Tab de perfil del propietario"""
        self.cambiar_color_tab("Mi Perfil")
        self.limpiar_content()

        ctk.CTkLabel(self.content_frame, text="👤 Mi Perfil", font=("Arial", 14, "bold")).pack(pady=(0, 20))

        ctk.CTkLabel(self.content_frame, text=f"Usuario: {self.controller.usuario_actual}", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(0, 5))
        ctk.CTkLabel(self.content_frame, text=f"Rol: {self.controller.rol_actual.title()}", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(0, 10))

        self.info_visible = False
        self.btn_toggle_info = ctk.CTkButton(
            self.content_frame,
            text="Mostrar mi información",
            command=self.toggle_info_usuario,
            width=220,
            height=40,
            font=("Arial", 11, "bold"),
            fg_color=("#0078d4", "#0078d4")
        )
        self.btn_toggle_info.pack(pady=(0, 20), padx=20, anchor="w")

        self.info_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")

        ctk.CTkButton(
            self.content_frame,
            text="Cambiar Contraseña",
            command=self.cambiar_contraseña,
            width=200,
            height=40,
            font=("Arial", 11, "bold")
        ).pack(pady=(0, 10), padx=20, anchor="w")

        ctk.CTkButton(
            self.content_frame,
            text="Recuperar Contraseña",
            command=self.recuperar_contraseña,
            width=200,
            height=40,
            font=("Arial", 11, "bold"),
            fg_color=("#ffc107", "#ffc107")
        ).pack(pady=(0, 10), padx=20, anchor="w")

    # ==================== MÉTODOS AUXILIARES ====================

    def crear_tabla_libros_cliente(self, parent):
        """Crea tabla de libros para cliente"""
        # Frame para la tabla
        table_frame = ctk.CTkFrame(parent, fg_color="transparent")
        table_frame.pack(fill="both", expand=True)

        # Crear Treeview
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Treeview', font=("Arial", 10), rowheight=25)
        style.configure('Treeview.Heading', font=("Arial", 10, "bold"))

        columns = ("Título", "Autor", "Año", "Acción")

        tree = ttk.Treeview(table_frame, columns=columns, height=12, show="headings")
        tree.pack(fill="both", expand=True)

        tree.column("Título", width=150)
        tree.column("Autor", width=150)
        tree.column("Año", width=80)
        tree.column("Acción", width=100)

        tree.heading("Título", text="Título")
        tree.heading("Autor", text="Autor")
        tree.heading("Año", text="Año")
        tree.heading("Acción", text="Acción")

        libros = self.controller.obtener_libros()

        if not libros:
            tree.insert("", "end", values=("No hay libros disponibles", "", ""))
        else:
            for libro in libros:
                valores = (libro["titulo"], libro["autor"], libro["anio"], "Rentar")
                tree.insert("", "end", values=valores)

        def on_click(event):
            item = tree.selection()[0] if tree.selection() else None
            if item:
                titulo = tree.item(item)["values"][0]
                if titulo != "No hay libros disponibles":
                    self.rentar_libro(titulo)

        tree.bind("<Button-1>", on_click)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscroll=scrollbar.set)

    def crear_tabla_prestamos_cliente(self, parent):
        """Crea tabla de préstamos para cliente"""
        table_frame = ctk.CTkFrame(parent, fg_color="transparent")
        table_frame.pack(fill="both", expand=True)

        style = ttk.Style()
        columns = ("Libro", "Desde", "Hasta", "Estado", "Renovaciones", "Acción")

        tree = ttk.Treeview(table_frame, columns=columns, height=12, show="headings")
        tree.pack(fill="both", expand=True)

        tree.column("Libro", width=120)
        tree.column("Desde", width=100)
        tree.column("Hasta", width=100)
        tree.column("Estado", width=70)
        tree.column("Renovaciones", width=80)
        tree.column("Acción", width=100)

        for col in columns:
            tree.heading(col, text=col)

        prestamos = self.controller.obtener_mis_prestamos()

        if not prestamos:
            tree.insert("", "end", values=("No tienes préstamos", "", "", "", "", ""))
        else:
            for prestamo in prestamos:
                estado = "Devuelto" if prestamo["devuelto"] else "Activo"
                renovaciones = prestamo.get("renovaciones", 0)
                valores = (
                    prestamo["libro"],
                    prestamo["fecha_prestamo"],
                    prestamo["fecha_vencimiento"],
                    estado,
                    renovaciones,
                    "Renovar" if not prestamo["devuelto"] else ""
                )
                tree.insert("", "end", values=valores)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscroll=scrollbar.set)

    def crear_tabla_libros_propietario(self, parent):
        """Crea tabla de libros para propietario"""
        table_frame = ctk.CTkFrame(parent, fg_color="transparent")
        table_frame.pack(fill="both", expand=True)

        style = ttk.Style()
        columns = ("Título", "Autor", "Año")

        self.tree_libros_propietario = ttk.Treeview(table_frame, columns=columns, height=12, show="headings")
        self.tree_libros_propietario.pack(fill="both", expand=True)

        for col in columns:
            if col == "Título":
                self.tree_libros_propietario.column(col, width=200)
            else:
                self.tree_libros_propietario.column(col, width=150)
            self.tree_libros_propietario.heading(col, text=col)

        self.actualizar_tabla_libros_propietario()

        self.tree_libros_propietario.bind("<<TreeviewSelect>>", self._on_libro_seleccionado)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree_libros_propietario.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree_libros_propietario.configure(yscroll=scrollbar.set)

        # Botón de eliminar
        delete_frame = ctk.CTkFrame(parent, fg_color="transparent")
        delete_frame.pack(fill="x", padx=20, pady=(10, 0))

        self.btn_eliminar_libro = ctk.CTkButton(
            delete_frame,
            text="Eliminar libro seleccionado",
            command=self.eliminar_libro_seleccionado,
            width=220,
            height=35,
            font=("Arial", 11, "bold"),
            fg_color=("#dc3545", "#dc3545"),
            state="disabled"
        )
        self.btn_eliminar_libro.pack(side="left")

        self.libro_seleccionado = None

    def actualizar_tabla_libros_propietario(self):
        """Refresca el contenido de la tabla de libros """
        for item in self.tree_libros_propietario.get_children():
            self.tree_libros_propietario.delete(item)

        libros = self.controller.obtener_libros()

        if not libros:
            self.tree_libros_propietario.insert("", "end", values=("No hay libros", "", ""))
            self.btn_eliminar_libro.configure(state="disabled")
        else:
            for libro in libros:
                self.tree_libros_propietario.insert("", "end", values=(libro["titulo"], libro["autor"], libro["anio"]))

    def _on_libro_seleccionado(self, event):
        selected = self.tree_libros_propietario.selection()
        if not selected:
            self.libro_seleccionado = None
            self.btn_eliminar_libro.configure(state="disabled")
            return

        values = self.tree_libros_propietario.item(selected[0], "values")
        if not values or values[0] == "No hay libros":
            self.libro_seleccionado = None
            self.btn_eliminar_libro.configure(state="disabled")
        else:
            self.libro_seleccionado = values[0]
            self.btn_eliminar_libro.configure(state="normal")

    def eliminar_libro_seleccionado(self):
        if not self.libro_seleccionado:
            return

        confirm = messagebox.askyesno("Confirmar eliminación", f"¿Estás seguro de eliminar el libro '{self.libro_seleccionado}'?")
        if not confirm:
            return

        eliminado = self.controller.eliminar_libro(self.libro_seleccionado)
        if eliminado:
            messagebox.showinfo("Éxito", "Libro eliminado correctamente")
            self.actualizar_tabla_libros_propietario()
            self.libro_seleccionado = None
            self.btn_eliminar_libro.configure(state="disabled")
        else:
            messagebox.showerror("Error", "No se pudo eliminar el libro")

    def crear_tabla_todos_prestamos(self, parent):
        """Crea tabla de todos los préstamos"""
        table_frame = ctk.CTkFrame(parent, fg_color="transparent")
        table_frame.pack(fill="both", expand=True)

        style = ttk.Style()
        columns = ("Cliente", "Libro", "Desde", "Hasta", "Estado")

        tree = ttk.Treeview(table_frame, columns=columns, height=12, show="headings")
        tree.pack(fill="both", expand=True)

        tree.column("Cliente", width=120)
        tree.column("Libro", width=150)
        tree.column("Desde", width=100)
        tree.column("Hasta", width=100)
        tree.column("Estado", width=80)

        for col in columns:
            tree.heading(col, text=col)

        prestamos = self.controller.obtener_todos_prestamos()

        if not prestamos:
            tree.insert("", "end", values=("No hay préstamos", "", "", "", ""))
        else:
            for prestamo in prestamos:
                estado = "Devuelto" if prestamo["devuelto"] else "Activo"
                tree.insert("", "end", values=(
                    prestamo["usuario"],
                    prestamo["libro"],
                    prestamo["fecha_prestamo"],
                    prestamo["fecha_vencimiento"],
                    estado
                ))

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscroll=scrollbar.set)

    def crear_tabla_clientes(self, parent):
        """Crea tabla de clientes"""
        table_frame = ctk.CTkFrame(parent, fg_color="transparent")
        table_frame.pack(fill="both", expand=True)

        style = ttk.Style()
        columns = ("Usuario", "Correo", "Teléfono", "Estado")

        tree = ttk.Treeview(table_frame, columns=columns, height=12, show="headings")
        tree.pack(fill="both", expand=True)

        tree.column("Usuario", width=120)
        tree.column("Correo", width=150)
        tree.column("Teléfono", width=120)
        tree.column("Estado", width=80)

        for col in columns:
            tree.heading(col, text=col)

        clientes = self.controller.obtener_clientes()

        if not clientes:
            tree.insert("", "end", values=("No hay clientes", "", "", ""))
        else:
            for cliente in clientes:
                tree.insert("", "end", values=(
                    cliente["usuario"],
                    cliente["correo"],
                    cliente["telefono"],
                    cliente["estado"]
                ))

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscroll=scrollbar.set)

    def buscar_libros(self):
        """Busca libros por título, autor o año"""
        termino = self.search_entry.get().strip().lower()

        if not termino:
            messagebox.showwarning("Búsqueda", "Ingrese un término de búsqueda")
            return

        libros = self.controller.obtener_libros()
        resultados = [l for l in libros if termino in l["titulo"].lower() or termino in l["autor"].lower() or termino in str(l["anio"])]

        # Limpiar resultados anteriores
        for widget in self.search_results_frame.winfo_children():
            widget.destroy()

        if not resultados:
            ctk.CTkLabel(self.search_results_frame, text="No se encontraron libros", font=("Arial", 12)).pack(pady=20)
        else:
            ctk.CTkLabel(self.search_results_frame, text=f"Se encontraron {len(resultados)} resultado(s)", font=("Arial", 12, "bold")).pack(pady=10)

            for libro in resultados:
                libro_frame = ctk.CTkFrame(self.search_results_frame, fg_color=("#e8f4f8", "#2a3a3a"), corner_radius=8)
                libro_frame.pack(fill="x", pady=10)

                info_text = f" {libro['titulo']} - {libro['autor']} ({libro['anio']})"
                ctk.CTkLabel(libro_frame, text=info_text, font=("Arial", 11)).pack(anchor="w", padx=15, pady=10)

                ctk.CTkButton(
                    libro_frame,
                    text="Rentar",
                    command=lambda t=libro['titulo']: self.rentar_libro(t),
                    width=80,
                    height=30,
                    font=("Arial", 10)
                ).pack(anchor="e", padx=15, pady=10)

    def agregar_libro(self):
        """Valida y agrega un nuevo libro"""
        titulo = self.entrada_titulo.get().strip()
        autor = self.entrada_autor.get().strip()
        anio = self.entrada_anio.get().strip()

        if not titulo or not autor or not anio:
            messagebox.showwarning("Validación", "Complete todos los campos")
            return

        if not anio.isdigit() or len(anio) != 4:
            messagebox.showwarning("Validación", "El año debe ser un número de 4 dígitos")
            return

        self.controller.agregar_libro(titulo, autor, anio)
        messagebox.showinfo("Éxito", f"✓ '{titulo}' agregado a la biblioteca")

        self.entrada_titulo.delete(0, "end")
        self.entrada_autor.delete(0, "end")
        self.entrada_anio.delete(0, "end")

        self.mostrar_tab_mis_libros()

    def rentar_libro(self, titulo):
        """Renta un libro"""
        if titulo == "No hay libros disponibles":
            return

        self.controller.rentar_libro(titulo)
        messagebox.showinfo("Éxito", f"✓ Libro '{titulo}' rentado por 7 días")
        self.mostrar_tab_mis_prestamos()

    def actualizar_perfil(self):
        """Guarda los cambios de correo y teléfono del usuario"""
        correo = self.correo_entry.get().strip()
        telefono = self.telefono_entry.get().strip()

        if not correo or not telefono:
            messagebox.showwarning("Validación", "El correo y el teléfono son obligatorios")
            return

        if "@" not in correo or "." not in correo:
            messagebox.showwarning("Validación", "Ingrese un correo válido")
            return

        self.controller.actualizar_perfil(self.controller.usuario_actual, self.controller.rol_actual, correo, telefono)
        messagebox.showinfo("Actualización", "Datos de perfil actualizados correctamente")

    def cambiar_contraseña(self):
        """Abre diálogo para cambiar contraseña con contraseña actual"""
        actual = simpledialog.askstring("Cambiar contraseña", "Ingresa tu contraseña actual:", show="*")
        if not actual:
            return

        nueva = simpledialog.askstring("Cambiar contraseña", "Ingresa la nueva contraseña:", show="*")
        if not nueva or len(nueva) < 4:
            messagebox.showwarning("Validación", "La contraseña nueva debe tener al menos 4 caracteres")
            return

        confirmacion = simpledialog.askstring("Cambiar contraseña", "Confirma la nueva contraseña:", show="*")
        if confirmacion != nueva:
            messagebox.showwarning("Validación", "Las contraseñas no coinciden")
            return

        if self.controller.cambiar_contraseña(self.controller.usuario_actual, self.controller.rol_actual, actual, nueva):
            messagebox.showinfo("Contraseña", "Contraseña cambiada correctamente")
        else:
            messagebox.showerror("Contraseña", "Contraseña actual incorrecta")

    def recuperar_contraseña(self):
        """Solicita código de recuperación y actualiza la contraseña"""
        user = self.controller.usuario_actual
        rol = self.controller.rol_actual

        if not self.controller.solicitar_codigo_recuperacion(user, rol):
            messagebox.showerror("Recuperar contraseña", "No se pudo enviar el código. Verifica tu correo y configuración SMTP")
            return

        messagebox.showinfo("Recuperar contraseña", "Se envió un código al correo registrado")
        codigo = simpledialog.askstring("Recuperar contraseña", "Ingresa el código recibido en el correo:")
        if not codigo:
            return

        if not self.controller.verificar_codigo_recuperacion(user, rol, codigo.strip()):
            messagebox.showerror("Recuperar contraseña", "Código incorrecto")
            return

        nueva = simpledialog.askstring("Recuperar contraseña", "Ingresa la nueva contraseña:", show="*")
        if not nueva or len(nueva) < 4:
            messagebox.showwarning("Validación", "La contraseña nueva debe tener al menos 4 caracteres")
            return

        confirmacion = simpledialog.askstring("Recuperar contraseña", "Confirma la nueva contraseña:", show="*")
        if confirmacion != nueva:
            messagebox.showwarning("Validación", "Las contraseñas no coinciden")
            return

        if self.controller.restablecer_contraseña_por_codigo(user, rol, codigo.strip(), nueva):
            messagebox.showinfo("Recuperar contraseña", "Contraseña actualizada correctamente")
        else:
            messagebox.showerror("Recuperar contraseña", "No se pudo cambiar la contraseña. Intenta de nuevo")

    def logout(self):
        """Cierra la sesión y vuelve al login"""
        self.controller.usuario_actual = None
        self.controller.rol_actual = None
        self.destroy()
        from view.login_view import LoginView
        LoginView(self.parent, self.controller).pack(fill="both", expand=True)