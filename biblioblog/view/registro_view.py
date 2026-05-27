import flet as ft
from biblioblog.utils.theme import PRIMARY_COLOR, SECONDARY_COLOR

class RegistroView:
    def __init__(self, app):
        self.app = app
        
        self.user_input = ft.TextField(label="Usuario (Ej: juan123)", width=400)
        self.nombres_input = ft.TextField(label="Nombres (Ej: Juan)", width=400)
        self.apellidos_input = ft.TextField(label="Apellidos (Ej: Pérez)", width=400)
        self.email_input = ft.TextField(label="Correo (ejemplo@email.com)", width=400)
        self.pass_input = ft.TextField(label="Contraseña (Mínimo 4 caracteres)", password=True, can_reveal_password=True, width=400)
        self.phone_input = ft.TextField(label="Teléfono (+1234567)", width=400)
        self.fecha_nac_input = ft.TextField(label="Fecha de Nac. (DD/MM/AAAA)", width=400)
        
        self.rol_input = ft.Dropdown(
            label="Tipo de usuario",
            width=400,
            options=[
                ft.dropdown.Option("Cliente"),
                ft.dropdown.Option("Propietario"),
            ],
            value="Cliente"
        )
        self.reg_btn = ft.ElevatedButton("✓ Registrar", on_click=self.do_register, style=ft.ButtonStyle(bgcolor=PRIMARY_COLOR, color=ft.Colors.WHITE), width=400, height=45)

    def build(self):
        return ft.Container(
            expand=True,
            alignment=ft.Alignment(0, 0),
            padding=20,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Text("📝 Crear Cuenta", size=24, weight=ft.FontWeight.BOLD, color=PRIMARY_COLOR),
                    self.user_input,
                    self.nombres_input,
                    self.apellidos_input,
                    self.email_input,
                    self.pass_input,
                    self.phone_input,
                    self.fecha_nac_input,
                    self.rol_input,
                    ft.Container(height=10),
                    self.reg_btn,
                    ft.ElevatedButton("← Volver al Inicio", on_click=lambda _: self.app.show_view("welcome"), style=ft.ButtonStyle(bgcolor="#64748b", color=ft.Colors.WHITE), width=400, height=40)
                ],
                scroll=ft.ScrollMode.AUTO
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

    def do_register(self, e):
        user = self.user_input.value.strip() if self.user_input.value else ""
        nombres = self.nombres_input.value.strip() if self.nombres_input.value else ""
        apellidos = self.apellidos_input.value.strip() if self.apellidos_input.value else ""
        pwd = self.pass_input.value if self.pass_input.value else ""
        email = self.email_input.value.strip() if self.email_input.value else ""
        phone = self.phone_input.value.strip() if self.phone_input.value else ""
        fecha_nac = self.fecha_nac_input.value.strip() if self.fecha_nac_input.value else ""
        rol = self.rol_input.value.lower() if self.rol_input.value else "cliente"
        if "propietario" in rol:
            rol = "administrador"
        
        if not all([user, nombres, apellidos, pwd, email, phone, fecha_nac]):
            self.show_alert('Error', 'Complete todos los campos')
            return
            
        self.reg_btn.text = '⏳ Registrando...'
        self.reg_btn.disabled = True
        self.app.page.update()
        
        import threading
        threading.Thread(target=self._reg_thread, args=(user, pwd, email, phone, rol, nombres, apellidos, fecha_nac), daemon=True).start()

    def _reg_thread(self, user, pwd, email, phone, rol, nombres, apellidos, fecha_nac):
        try:
            res = self.app.controller.registrar_usuario(user, pwd, email, phone, rol, nombres, apellidos, fecha_nac)
            if res:
                if rol == 'cliente':
                    self._verify_cliente(user, email, res, rol)
                else:
                    self.app.controller.usuario_actual = user
                    self.app.controller.rol_actual = rol
                    self.show_alert('Éxito', 'Cuenta de propietario creada y verificada')
                    self.app.show_view("dashboard")
            else:
                self.show_alert('Error', 'El usuario ya existe o error al registrar')
        except Exception as ex:
            self.show_alert('Error', str(ex))
        finally:
            self.reg_btn.text = '✓ Registrar'
            self.reg_btn.disabled = False
            self.app.page.update()

    def _verify_cliente(self, user, email, code, rol):
        code_input = ft.TextField(label="Código")
        
        def on_verify(e):
            input_code = code_input.value.strip()
            if self.app.controller.verificar_codigo(user, rol, input_code):
                self._close_dlg(dlg)
                self.app.controller.usuario_actual = user
                self.app.controller.rol_actual = rol
                self.show_alert('Éxito', 'Cuenta verificada')
                self.app.show_view("dashboard")
            else:
                self.show_alert('Error', 'Código incorrecto')
        
        dlg = ft.AlertDialog(
            title=ft.Text('Verificar Correo'),
            content=ft.Column([
                ft.Text(f'Enviando código a {email}...'),
                code_input
            ], tight=True),
            actions=[
                ft.TextButton("Verificar", on_click=on_verify),
                ft.TextButton("Cancelar", on_click=lambda _: self._close_dlg(dlg))
            ]
        )
        self._open_dlg(dlg)
        
        import threading
        def _send():
            self.app.controller.enviar_confirmacion_registro(user, email, code)
        threading.Thread(target=_send, daemon=True).start()
