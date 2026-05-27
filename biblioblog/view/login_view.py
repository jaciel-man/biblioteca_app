import flet as ft
from biblioblog.utils.theme import PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR

class LoginView:
    def __init__(self, app):
        self.app = app
        self.user_input = ft.TextField(label="Usuario", hint_text="Ingrese su usuario", width=400)
        self.pass_input = ft.TextField(label="Contraseña", hint_text="Ingrese su contraseña", password=True, can_reveal_password=True, width=400)
        self.rol_input = ft.Dropdown(
            label="Tipo de usuario",
            width=400,
            options=[
                ft.dropdown.Option("Cliente"),
                ft.dropdown.Option("Propietario"),
            ],
            value="Cliente"
        )
        self.login_btn = ft.ElevatedButton("✓ Entrar", on_click=self.do_login, style=ft.ButtonStyle(bgcolor=PRIMARY_COLOR, color=ft.Colors.WHITE), width=400, height=45)

    def build(self):
        return ft.Container(
            expand=True,
            alignment=ft.Alignment(0, 0),
            padding=20,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15,
                controls=[
                    ft.Text("📚 Iniciar Sesión", size=24, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
                    self.user_input,
                    self.pass_input,
                    self.rol_input,
                    ft.Container(height=20),
                    self.login_btn,
                    ft.ElevatedButton("+ Crear nueva cuenta", on_click=lambda _: self.app.show_view("registro"), style=ft.ButtonStyle(bgcolor=SECONDARY_COLOR, color=ft.Colors.WHITE), width=400, height=40),
                    ft.ElevatedButton("🔑 Recuperar Contraseña", on_click=self.do_recover, style=ft.ButtonStyle(bgcolor=ACCENT_COLOR, color=ft.Colors.WHITE), width=400, height=40),
                    ft.ElevatedButton("← Volver al Inicio", on_click=lambda _: self.app.show_view("welcome"), style=ft.ButtonStyle(bgcolor="#64748b", color=ft.Colors.WHITE), width=400, height=40)
                ]
            )
        )

    def _open_dlg(self, dlg):
        self.app.page.show_dialog(dlg)

    def _close_dlg(self, dlg):
        self.app.page.pop_dialog()

    def show_alert(self, title, msg):
        dlg = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(msg),
            actions=[ft.TextButton("OK", on_click=lambda _: self._close_dlg(dlg))]
        )
        self._open_dlg(dlg)

    def do_login(self, e):
        user = self.user_input.value.strip() if self.user_input.value else ""
        pwd = self.pass_input.value if self.pass_input.value else ""
        rol = self.rol_input.value.lower() if self.rol_input.value else "cliente"
        if "propietario" in rol:
            rol = "administrador"
        
        if not user or not pwd:
            self.show_alert('Error', 'Complete todos los campos')
            return
            
        self.login_btn.text = '⏳ Entrando...'
        self.login_btn.disabled = True
        self.app.page.update()
        
        import threading
        threading.Thread(target=self._login_thread, args=(user, pwd, rol), daemon=True).start()

    def _login_thread(self, user, pwd, rol):
        try:
            res = self.app.controller.login(user, pwd, rol)
            if res is True:
                self.app.controller.usuario_actual = user
                self.app.controller.rol_actual = rol
                self.app.show_view("dashboard")
            elif res == 'not_verified':
                self.ask_verification(user, rol)
            else:
                self.show_alert('Error', 'Usuario o contraseña incorrectos')
        except Exception as ex:
            self.show_alert('Error', str(ex))
        finally:
            self.login_btn.text = '✓ Entrar'
            self.login_btn.disabled = False
            self.app.page.update()

    def ask_verification(self, user, rol):
        code_input = ft.TextField(label="Código de 6 dígitos")
        
        def on_verify(e):
            code = code_input.value.strip()
            if self.app.controller.verificar_codigo(user, rol, code):
                self._close_dlg(dlg)
                self.app.controller.usuario_actual = user
                self.app.controller.rol_actual = rol
                self.show_alert('Éxito', 'Cuenta verificada correctamente')
                self.app.show_view("dashboard")
            else:
                self.show_alert('Error', 'Código incorrecto')

        dlg = ft.AlertDialog(
            title=ft.Text('Verificación'),
            content=ft.Column([
                ft.Text('Tu cuenta está pendiente de verificación.\nRevisa tu correo e ingresa el código:'),
                code_input
            ], tight=True),
            actions=[
                ft.TextButton("Verificar", on_click=on_verify),
                ft.TextButton("Cancelar", on_click=lambda _: self._close_dlg(dlg))
            ]
        )
        self._open_dlg(dlg)

    def do_recover(self, e):
        user = self.user_input.value.strip() if self.user_input.value else ""
        rol = self.rol_input.value.lower() if self.rol_input.value else "cliente"
        if "propietario" in rol:
            rol = "administrador"
        if not user:
            self.show_alert('Error', 'Ingrese su usuario primero en el campo correspondiente')
            return
            
        code_input = ft.TextField(label="Código recibido")
        new_pwd = ft.TextField(label="Nueva contraseña", password=True)
        status_text = ft.Text("Generando código y enviando correo...")
        
        def on_update(e):
            code = code_input.value.strip()
            pwd = new_pwd.value
            if len(pwd) < 4:
                self.show_alert('Error', 'Mínimo 4 caracteres')
                return
            if self.app.controller.restablecer_contraseña_por_codigo(user, rol, code, pwd):
                self._close_dlg(dlg)
                self.show_alert('Éxito', 'Contraseña actualizada')
            else:
                self.show_alert('Error', 'Código incorrecto o error al actualizar')
        
        dlg = ft.AlertDialog(
            title=ft.Text('Recuperar Contraseña'),
            content=ft.Column([status_text, code_input, new_pwd], tight=True),
            actions=[
                ft.TextButton("Actualizar", on_click=on_update),
                ft.TextButton("Cancelar", on_click=lambda _: self._close_dlg(dlg))
            ]
        )
        self._open_dlg(dlg)
        
        import threading
        def _send_recover():
            if self.app.controller.solicitar_codigo_recuperacion(user, rol):
                status_text.value = "Se envió un código a tu correo."
            else:
                status_text.value = "Error al enviar el correo. Verifique el usuario."
                status_text.color = ft.Colors.RED
            self.app.page.update()
            
        threading.Thread(target=_send_recover, daemon=True).start()
