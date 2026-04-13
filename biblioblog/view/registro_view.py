import customtkinter as ctk
from tkinter import messagebox, simpledialog

class RegistroView(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.configure(fg_color=("#f0f0f0", "#1a1a1a"))

        # Frame principal centrado
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True)

        # Título
        title = ctk.CTkLabel(
            main_frame,
            text="📝 Crear Cuenta",
            font=("Arial", 40, "bold")
        )
        title.pack(pady=(0, 10))

        subtitle = ctk.CTkLabel(
            main_frame,
            text="Complete todos los campos para registrarse",
            font=("Arial", 14),
            text_color=("gray60", "gray70")
        )
        subtitle.pack(pady=(0, 30))

        # Frame para inputs
        input_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        input_frame.pack(pady=20)

        # Usuario
        ctk.CTkLabel(input_frame, text="Usuario:", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(0, 5))
        self.user = ctk.CTkEntry(input_frame, placeholder_text="Ingrese un nombre de usuario", width=250, height=35)
        self.user.pack(padx=20, pady=(0, 15))

        # Contraseña
        ctk.CTkLabel(input_frame, text="Contraseña:", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(0, 5))
        password_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        password_frame.pack(padx=20, pady=(0, 15), fill="x")

        self.password = ctk.CTkEntry(password_frame, placeholder_text="Ingrese una contraseña", show="*", width=200, height=35)
        self.password.pack(side="left", fill="x", expand=True)

        # Botón pequeño para ver contraseña mientras se mantiene presionado
        self.btn_toggle_password = ctk.CTkButton(
            password_frame,
            text="👁",
            width=40,
            height=35,
            fg_color=("#6c757d", "#6c757d")
        )
        self.btn_toggle_password.pack(side="left", padx=(10, 0))
        self.btn_toggle_password.bind("<ButtonPress-1>", self._start_reveal_password)
        self.btn_toggle_password.bind("<ButtonRelease-1>", self._stop_reveal_password)
        self.btn_toggle_password.bind("<Leave>", self._stop_reveal_password)

        # Correo
        ctk.CTkLabel(input_frame, text="Correo:", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(0, 5))
        self.correo = ctk.CTkEntry(input_frame, placeholder_text="ejemplo@email.com", width=250, height=35)
        self.correo.pack(padx=20, pady=(0, 15))

        # Teléfono
        ctk.CTkLabel(input_frame, text="Teléfono:", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(0, 5))
        self.telefono = ctk.CTkEntry(input_frame, placeholder_text="+1 XXX XXX XXXX", width=250, height=35)
        self.telefono.pack(padx=20, pady=(0, 20))

        # Rol
        ctk.CTkLabel(input_frame, text="Tipo de usuario:", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(0, 10))
        rol_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        rol_frame.pack(padx=20, pady=(0, 20))

        self.rol = ctk.StringVar(value="cliente")
        ctk.CTkRadioButton(
            rol_frame,
            text="Cliente",
            variable=self.rol,
            value="cliente",
            font=("Arial", 11)
        ).pack(anchor="w", pady=5)

        # Botones
        button_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        button_frame.pack(pady=20)

        ctk.CTkButton(
            button_frame,
            text="Registrar",
            command=self.registrar,
            width=250,
            height=40,
            font=("Arial", 12, "bold"),
            fg_color=("#0078d4", "#0078d4")
        ).pack(pady=10)

        ctk.CTkButton(
            button_frame,
            text="Volver al Inicio",
            command=self.volver_a_inicio,
            width=250,
            height=40,
            font=("Arial", 12),
            fg_color=("gray70", "gray30"),
            text_color=("black", "white")
        ).pack(pady=5)

    def _start_reveal_password(self, event=None):
        """Mostrar contraseña mientras se presiona el botón"""
        self.password.configure(show="")

    def _stop_reveal_password(self, event=None):
        """Ocultar contraseña al soltar el botón"""
        self.password.configure(show="*")

    def registrar(self):
        user = self.user.get().strip()
        password = self.password.get()
        correo = self.correo.get().strip()
        telefono = self.telefono.get().strip()
        rol = self.rol.get()

        # Validaciones
        if not user or not password or not correo or not telefono:
            messagebox.showwarning("Validación", "Por favor complete todos los campos")
            return

        if len(user) < 3:
            messagebox.showwarning("Validación", "El usuario debe tener al menos 3 caracteres")
            return

        if len(password) < 4:
            messagebox.showwarning("Validación", "La contraseña debe tener al menos 4 caracteres")
            return

        if "@" not in correo or "." not in correo:
            messagebox.showwarning("Validación", "Ingrese un correo válido")
            return

        if not telefono.isdigit():
            messagebox.showwarning("Validación", "El teléfono debe contener solo números")
            return

        resultado = self.controller.registrar_usuario(user, password, correo, telefono, rol)

        if resultado:
            if rol == "cliente":
                codigo = resultado
                enviado = self.controller.enviar_confirmacion_registro(user, correo, codigo)
                if enviado:
                    messagebox.showinfo(
                        "Éxito",
                        "¡Cuenta registrada exitosamente! Se envió un correo con el código de verificación."
                    )
                else:
                    messagebox.showwarning(
                        "Advertencia",
                        "Cuenta registrada, pero no se pudo enviar el correo de confirmación. Copia el código que aparece a continuación."
                    )
                    messagebox.showinfo("Código de verificación", f"Tu código es: {codigo}")

                # Pedir código para activar la cuenta
                intentos = 3
                while intentos > 0:
                    ingresado = simpledialog.askstring("Verificación de correo", "Ingresa el código de verificación enviado al correo:")

                    if ingresado is None:
                        messagebox.showinfo("Cancelado", "Registro cancelado. El usuario no se guardará.")
                        self.controller.eliminar_usuario(user, rol)
                        self.destroy()
                        from view.welcome_view import WelcomeView
                        WelcomeView(self.parent, self.controller).pack(fill="both", expand=True)
                        return

                    if not ingresado.strip():
                        messagebox.showwarning("Validación", "Por favor ingresa el código de verificación")
                        continue

                    if self.controller.verificar_codigo(user, rol, ingresado.strip()):
                        messagebox.showinfo("Verificado", "Cuenta verificada correctamente. Accediendo al menú principal...")
                        self.controller.usuario_actual = user
                        self.controller.rol_actual = rol
                        self.destroy()
                        from view.dashboard_view import DashboardView
                        DashboardView(self.parent, self.controller).pack(fill="both", expand=True)
                        return

                    intentos -= 1
                    if intentos > 0:
                        messagebox.showwarning("Código incorrecto", f"Código incorrecto. Te quedan {intentos} intentos.")

                # Si llega aquí, se agotaron intentos
                messagebox.showerror("Verificación fallida", "No se verificó la cuenta. El usuario no será guardado.")
                self.controller.eliminar_usuario(user, rol)
                self.destroy()
                from view.welcome_view import WelcomeView
                WelcomeView(self.parent, self.controller).pack(fill="both", expand=True)
                return

            # Propietario: ya verificado, entra directo al dashboard
            self.controller.usuario_actual = user
            self.controller.rol_actual = rol
            messagebox.showinfo("Éxito", "Cuenta de propietario creada y verificada. Accediendo al menú principal...")
            self.destroy()
            from view.dashboard_view import DashboardView
            DashboardView(self.parent, self.controller).pack(fill="both", expand=True)
            return

        messagebox.showerror("Error", "Este usuario ya existe. Intente con otro")

    def volver_a_inicio(self):
        from view.welcome_view import WelcomeView
        self.destroy()
        WelcomeView(self.parent, self.controller).pack(fill="both", expand=True)