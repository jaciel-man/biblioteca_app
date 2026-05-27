import flet as ft
import webbrowser
from collections import defaultdict
from biblioblog.utils.theme import PRIMARY_COLOR, SECONDARY_COLOR, TAB_COLORS, GENRE_COLORS

class DashboardView:
    def __init__(self, app):
        self.app = app
        self.content_area = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True, spacing=15)
        
    def build(self):
        usuario = self.app.controller.usuario_actual or "BiblioBlog"
        rol = self.app.controller.rol_actual or "cliente"
        
        # Header
        header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(f"📚 {usuario}", weight=ft.FontWeight.BOLD, size=16, color=ft.Colors.WHITE, expand=True),
                    ft.ElevatedButton("Salir", on_click=self.do_logout, style=ft.ButtonStyle(bgcolor="#dc2626", color=ft.Colors.WHITE))
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            bgcolor=PRIMARY_COLOR,
            padding=10
        )

        # Tabs
        if rol == 'cliente':
            tab_labels = ["📚 Libros", "📋 Mis Préstamos", "🔍 Búsqueda", "👤 Mi Perfil"]
        else:
            tab_labels = ["➕ Agregar", "📚 Mis Libros", "📋 Préstamos", "👥 Clientes", "📊 Stats", "👤 Perfil"]

        self.tabs_control = ft.Tabs(
            length=len(tab_labels),
            selected_index=0,
            on_change=self.on_tab_change,
            expand=True,
            content=ft.Column(
                controls=[
                    header,
                    ft.TabBar(
                        tabs=[ft.Tab(label=lbl) for lbl in tab_labels]
                    ),
                    ft.Container(content=self.content_area, expand=True, padding=10)
                ],
                expand=True,
                spacing=0
            )
        )
        
        # Load initial tab
        self.load_tab(0)
        
        return self.tabs_control

    def do_logout(self, e):
        self.app.controller.usuario_actual = None
        self.app.controller.rol_actual = None
        self.app.show_view("welcome")

    def _open_dlg(self, dlg):
        self.app.page.show_dialog(dlg)

    def _close_dlg(self, dlg):
        self.app.page.pop_dialog()

    def _safe_update(self, control):
        try:
            control.update()
        except Exception:
            pass

    def show_alert(self, title, msg):
        dlg = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(msg),
            actions=[ft.TextButton("OK", on_click=lambda _: self._close_dlg(dlg))]
        )
        self._open_dlg(dlg)

    def on_tab_change(self, e):
        self.load_tab(self.tabs_control.selected_index)

    def load_tab(self, index):
        self.content_area.controls = []
        rol = self.app.controller.rol_actual
        
        if rol == 'cliente':
            if index == 0: self.tab_libros()
            elif index == 1: self.tab_mis_prestamos()
            elif index == 2: self.tab_busqueda()
            elif index == 3: self.tab_perfil()
        else:
            if index == 0: self.tab_agregar()
            elif index == 1: self.tab_mis_libros()
            elif index == 2: self.tab_todos_prestamos()
            elif index == 3: self.tab_clientes()
            elif index == 4: self.tab_stats()
            elif index == 5: self.tab_perfil()
        self.app.page.update()
        self._safe_update(self.content_area)

    def _abrir_pdf(self, pdf_url):
        if not pdf_url or not pdf_url.strip():
            self.show_alert('Sin PDF', 'Este libro no tiene un PDF asociado.')
            return
        try:
            webbrowser.open(pdf_url.strip())
        except Exception:
            self.show_alert('Error', 'No se pudo abrir el PDF.')

    def _rentar(self, titulo, btn_ref=None):
        if btn_ref:
            btn_ref.text = "⏳"
            btn_ref.disabled = True
            self.app.page.update()
            self._safe_update(btn_ref)
            
        import threading
        def _task():
            self.app.controller.rentar_libro(titulo)
            self.show_alert('Éxito', f"Libro '{titulo}' rentado por 7 días")
            if self.app.controller.rol_actual == 'cliente':
                self.tabs_control.selected_index = 1
                self.load_tab(1)
            self.app.page.update()
            self._safe_update(self.content_area)
            
        threading.Thread(target=_task, daemon=True).start()

    # --- CLIENTE TABS ---
    def tab_libros(self):
        self.content_area.controls.append(ft.Text("📚 Libros Disponibles", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR))
        libros = self.app.controller.obtener_libros()
        if not libros:
            self.content_area.controls.append(ft.Text("No hay libros disponibles"))
            return
            
        por_genero = defaultdict(list)
        for lib in libros:
            por_genero[lib.get('genero', 'Sin Género')].append(lib)
            
        for gen, libs in por_genero.items():
            g_color = GENRE_COLORS.get(gen, '#6b7280')
            
            gen_col = ft.Column(spacing=10)
            gen_col.controls.append(ft.Text(f"📌 {gen} ({len(libs)})", color=g_color, weight=ft.FontWeight.BOLD, size=16))
            
            for l in libs:
                pdf_url = l.get('pdf_url', '') or ''
                has_pdf = bool(pdf_url.strip())
                
                btns = [
                    ft.ElevatedButton("Rentar", on_click=lambda e, t=l['titulo']: self._rentar(t, e.control), style=ft.ButtonStyle(bgcolor=SECONDARY_COLOR, color=ft.Colors.WHITE))
                ]
                if has_pdf:
                    btns.append(ft.ElevatedButton("Leer PDF", on_click=lambda e, u=pdf_url: self._abrir_pdf(u), style=ft.ButtonStyle(bgcolor="#7c3aed", color=ft.Colors.WHITE)))
                
                card = ft.Card(
                    content=ft.Container(
                        padding=10,
                        content=ft.Row(
                            controls=[
                                ft.Column([
                                    ft.Text(l['titulo'], weight=ft.FontWeight.BOLD, size=16),
                                    ft.Text(f"{l['autor']} • {l['anio']}", color=ft.Colors.GREY_600, size=12)
                                ], expand=True),
                                ft.Column(btns, spacing=5)
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    )
                )
                gen_col.controls.append(card)
            
            self.content_area.controls.append(ft.Container(
                content=gen_col,
                bgcolor=ft.Colors.with_opacity(0.1, g_color),
                padding=10,
                border_radius=8
            ))

    def tab_mis_prestamos(self):
        self.content_area.controls.append(ft.Text("📋 Mis Préstamos", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR))
        prestamos = self.app.controller.obtener_mis_prestamos()
        if not prestamos:
            self.content_area.controls.append(ft.Text("No tienes préstamos activos"))
            return
            
        libros_dict = {l['titulo']: l for l in self.app.controller.obtener_libros()}
        for p in prestamos:
            estado = "Devuelto" if p["devuelto"] else "Activo"
            libro_data = libros_dict.get(p['libro'], {})
            pdf_url = libro_data.get('pdf_url', '') or ''
            has_pdf = bool(pdf_url.strip())
            
            col_content = [
                ft.Text(f"📖 {p['libro']}", weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR, size=16),
                ft.Text(f"Desde: {p['fecha_renta']} | Hasta: {p['fecha_vencimiento']}\nEstado: {estado}", color=ft.Colors.GREY_600, size=12)
            ]
            if has_pdf:
                col_content.append(ft.ElevatedButton("Leer / Descargar PDF", on_click=lambda e, u=pdf_url: self._abrir_pdf(u), style=ft.ButtonStyle(bgcolor="#7c3aed", color=ft.Colors.WHITE)))
                
            self.content_area.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=10,
                        content=ft.Column(col_content, spacing=5)
                    )
                )
            )

    def tab_busqueda(self):
        self.content_area.controls.append(ft.Text("🔍 Buscar Libros", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR))
        
        results_col = ft.Column(spacing=10)
        
        def on_search(e=None):
            termino = search_inp.value.lower().strip()
            results_col.controls = []
            libros = self.app.controller.obtener_libros()
            if termino:
                res = [l for l in libros if termino in l['titulo'].lower() or termino in l['autor'].lower() or termino in str(l.get('genero','')).lower()]
            else:
                res = libros # Si está vacío mostrar todos o nada. Mostremos todos.
                
            if not res:
                results_col.controls.append(ft.Text("No se encontraron libros"))
            else:
                for l in res:
                    pdf_url = l.get('pdf_url', '') or ''
                    has_pdf = bool(pdf_url.strip())
                    
                    btns = [
                        ft.ElevatedButton("Rentar", on_click=lambda e, t=l['titulo']: self._rentar(t, e.control), style=ft.ButtonStyle(bgcolor=SECONDARY_COLOR, color=ft.Colors.WHITE))
                    ]
                    if has_pdf:
                        btns.append(ft.ElevatedButton("PDF", on_click=lambda e, u=pdf_url: self._abrir_pdf(u), style=ft.ButtonStyle(bgcolor="#7c3aed", color=ft.Colors.WHITE)))
                    
                    results_col.controls.append(
                        ft.Card(
                            content=ft.Container(
                                padding=10,
                                content=ft.Row(
                                    controls=[
                                        ft.Text(f"{l['titulo']}\n{l['autor']}", expand=True),
                                        ft.Row(btns, spacing=5)
                                    ]
                                )
                            )
                        )
                    )
            self.app.page.update()
            self._safe_update(self.content_area)

        search_inp = ft.TextField(hint_text="Título, autor, género...", expand=True, on_change=on_search)
        
        search_row = ft.Row([
            search_inp,
            ft.ElevatedButton("Buscar", on_click=on_search, style=ft.ButtonStyle(bgcolor=PRIMARY_COLOR, color=ft.Colors.WHITE))
        ])
        
        self.content_area.controls.append(search_row)
        self.content_area.controls.append(results_col)
        
        # Load initial results (all books)
        on_search()

    def tab_perfil(self):
        self.content_area.controls.append(ft.Text("👤 Mi Perfil", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR))
        info = self.app.controller.obtener_info_usuario(self.app.controller.usuario_actual, self.app.controller.rol_actual)
        
        self.content_area.controls.append(
            ft.Text(f"Usuario: {self.app.controller.usuario_actual}\nRol: {self.app.controller.rol_actual.title()}\nCorreo: {info.get('correo','')}\nTeléfono: {info.get('telefono','')}")
        )
        
        email_edit = ft.TextField(label="Nuevo Correo", value=info.get('correo',''))
        phone_edit = ft.TextField(label="Nuevo Teléfono", value=info.get('telefono',''))
        
        def on_save(e):
            c = email_edit.value.strip()
            t = phone_edit.value.strip()
            self.app.controller.actualizar_perfil(self.app.controller.usuario_actual, self.app.controller.rol_actual, c, t)
            self.show_alert('Éxito', 'Perfil actualizado')
            
        self.content_area.controls.append(email_edit)
        self.content_area.controls.append(phone_edit)
        self.content_area.controls.append(
            ft.ElevatedButton("Guardar Cambios", on_click=on_save, style=ft.ButtonStyle(bgcolor=PRIMARY_COLOR, color=ft.Colors.WHITE))
        )

    # --- PROPIETARIO TABS ---
    def tab_agregar(self):
        self.content_area.controls.append(ft.Text("➕ Agregar Libro", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR))
        
        t_inp = ft.TextField(label="Título")
        a_inp = ft.TextField(label="Autor")
        y_inp = ft.TextField(label="Año")
        p_inp = ft.TextField(label="Precio Renta", value="0")
        s_inp = ft.TextField(label="Stock", value="0")
        g_inp = ft.Dropdown(
            label="Género",
            options=[ft.dropdown.Option(g) for g in ["Novela", "Ciencia Ficción", "Fantasía", "Terror", "Romance", "Historia", "Realismo Mágico", "Misterio", "Ensayo / Historia", "Sin Género"]],
            value="Novela"
        )
        
        def on_add(e):
            t = t_inp.value.strip()
            a = a_inp.value.strip()
            y = y_inp.value.strip()
            g = g_inp.value
            precio = p_inp.value.strip() or '0'
            stock = s_inp.value.strip() or '0'
            
            if not t or not a or not y:
                self.show_alert('Error', 'Complete los campos obligatorios (Título, Autor, Año)')
                return
            try:
                self.app.controller.agregar_libro(t, a, y, g, float(precio), int(stock))
                self.show_alert('Éxito', f'Libro "{t}" agregado correctamente')
                t_inp.value = ""; a_inp.value = ""; y_inp.value = ""; p_inp.value = "0"; s_inp.value = "0"
                self.app.page.update()
                self._safe_update(self.content_area)
            except ValueError:
                self.show_alert('Error', 'Precio y Stock deben ser números')
                
        for inp in [t_inp, a_inp, y_inp, p_inp, s_inp, g_inp]:
            self.content_area.controls.append(inp)
            
        self.content_area.controls.append(
            ft.ElevatedButton("✓ Agregar Libro", on_click=on_add, style=ft.ButtonStyle(bgcolor=PRIMARY_COLOR, color=ft.Colors.WHITE))
        )

    def tab_mis_libros(self):
        self.content_area.controls.append(ft.Text("📚 Mis Libros", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR))
        libros = self.app.controller.obtener_libros()
        if not libros:
            self.content_area.controls.append(ft.Text("No hay libros registrados"))
            return
            
        for l in libros:
            def on_del(e, titulo=l['titulo']):
                self.app.controller.eliminar_libro(titulo)
                self.show_alert('Éxito', 'Libro eliminado')
                self.load_tab(1)
                
            self.content_area.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=10,
                        content=ft.Row(
                            controls=[
                                ft.Column([
                                    ft.Text(l['titulo'], weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR, size=16),
                                    ft.Text(f"{l['autor']} • {l.get('genero','?')} • Stock: {l.get('stock',0)}", color=ft.Colors.GREY_600, size=12)
                                ], expand=True),
                                ft.ElevatedButton("X", on_click=on_del, style=ft.ButtonStyle(bgcolor="#dc2626", color=ft.Colors.WHITE))
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    )
                )
            )

    def tab_todos_prestamos(self):
        self.content_area.controls.append(ft.Text("📋 Todos los Préstamos", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR))
        prestamos = self.app.controller.obtener_todos_prestamos()
        if not prestamos:
            self.content_area.controls.append(ft.Text("No hay préstamos registrados"))
            return
            
        for p in prestamos:
            devuelto = p["devuelto"]
            estado = "Devuelto" if devuelto else "Activo"
            bg = "#d1fae5" if devuelto else "#dbeafe"
            estado_color = "#059669" if devuelto else "#2563eb"
            
            self.content_area.controls.append(
                ft.Container(
                    bgcolor=bg,
                    padding=10,
                    border_radius=8,
                    content=ft.Column([
                        ft.Text(f"📖 {p['libro']}", weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR, size=14),
                        ft.Row([
                            ft.Text(f"👤 {p['usuario']}  |  Estado: ", color=ft.Colors.GREY_800, size=12),
                            ft.Text(f"[{estado}]", weight=ft.FontWeight.BOLD, color=estado_color, size=12)
                        ])
                    ], spacing=5)
                )
            )

    def tab_clientes(self):
        self.content_area.controls.append(ft.Text("👥 Clientes", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR))
        clientes = self.app.controller.obtener_clientes()
        for c in clientes:
            self.content_area.controls.append(
                ft.Card(
                    content=ft.Container(
                        padding=10,
                        content=ft.Text(f"User: {c['usuario']}\nEmail: {c['correo']}\nTel: {c['telefono']}")
                    )
                )
            )

    def tab_stats(self):
        self.content_area.controls.append(ft.Text("📊 Estadísticas", size=20, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR))
        libros = self.app.controller.obtener_libros()
        prestamos = self.app.controller.obtener_todos_prestamos()
        clientes = self.app.controller.obtener_clientes()
        p_activos = len([p for p in prestamos if not p["devuelto"]])
        p_devueltos = len([p for p in prestamos if p["devuelto"]])
        
        summary_items = [
            ("📚 Libros", str(len(libros)), '#3b82f6'),
            ("👥 Clientes", str(len(clientes)), '#10b981'),
            ("🟢 Activos", str(p_activos), '#f59e0b'),
            ("✅ Devueltos", str(p_devueltos), '#8b5cf6'),
        ]
        
        row_summary = ft.Row(spacing=10, wrap=True)
        for label_t, val_t, col in summary_items:
            row_summary.controls.append(
                ft.Container(
                    bgcolor=ft.Colors.with_opacity(0.15, col),
                    padding=10,
                    border_radius=8,
                    width=100,
                    content=ft.Column([
                        ft.Text(val_t, weight=ft.FontWeight.BOLD, size=24, color=col),
                        ft.Text(label_t, size=12, color=ft.Colors.GREY_700)
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                )
            )
            
        self.content_area.controls.append(row_summary)
        
        # Simple Bar Chart representation using Containers
        data = {
            "Total Libros": len(libros),
            "Clientes": len(clientes),
            "Préstamos Activos": p_activos,
            "Total Préstamos": len(prestamos)
        }
        max_val = max(data.values()) if data.values() else 1
        if max_val == 0: max_val = 1
        colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6']
        
        chart_col = ft.Column(spacing=10)
        for i, (label_t, value) in enumerate(data.items()):
            col_hex = colors[i % len(colors)]
            ratio = value / max_val
            
            chart_col.controls.append(
                ft.Row([
                    ft.Text(label_t, width=120, text_align=ft.TextAlign.RIGHT),
                    ft.Container(
                        bgcolor=col_hex,
                        height=20,
                        width=300 * ratio,
                        border_radius=5
                    ),
                    ft.Text(str(value), weight=ft.FontWeight.BOLD)
                ])
            )
            
        self.content_area.controls.append(ft.Container(content=chart_col, padding=20))
