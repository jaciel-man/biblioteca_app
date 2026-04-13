import customtkinter as ctk
from tkinter import messagebox, simpledialog
from view.registro_view import RegistroView

class LoginView(ctk.CTkFrame):

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
            text="📚 BiblioBlog",
            font=("Arial", 40, "bold")
        )
        title.pack(pady=(0, 10))

        subtitle = ctk.CTkLabel(
            main_frame,
            text="Sistema de Gestión de Biblioteca",
            font=("Arial", 14),
            text_color=("gray60", "gray70")
        )
        subtitle.pack(pady=(0, 30))

        # Frame para inputs
        input_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        input_frame.pack(pady=20)

        # Usuario
        ctk.CTkLabel(input_frame, text="Usuario:", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(0, 5))
        self.user = ctk.CTkEntry(input_frame, placeholder_text="Ingrese su usuario", width=250, height=35)
        self.user.pack(padx=20, pady=(0, 15))
        self.user.bind("<Return>", lambda e: self.login())

        # Contraseña
        ctk.CTkLabel(input_frame, text="Contraseña:", font=("Arial", 12)).pack(anchor="w", padx=20, pady=(0, 5))
        self.password = ctk.CTkEntry(input_frame, placeholder_text="Ingrese su contraseña", show="*", width=250, height=35)
        self.password.pack(padx=20, pady=(0, 20))
        self.password.bind("<Return>", lambda e: self.login())

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
        ctk.CTkRadioButton(
            rol_frame,
            text="Propietario",
            variable=self.rol,
            value="propietario",
            font=("Arial", 11)
        ).pack(anchor="w", pady=5)

        # Botones
        button_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        button_frame.pack(pady=20)

        ctk.CTkButton(
            button_frame,
            text="Entrar",
            command=self.login,
            width=250,
            height=40,
            font=("Arial", 12, "bold"),
            fg_color=("#0078d4", "#0078d4")
        ).pack(pady=10)

        ctk.CTkButton(
            button_frame,
            text="Crear nueva cuenta",
            command=self.registro,
            width=250,
            height=40,
            font=("Arial", 12),
            fg_color=("gray70", "gray30"),
            text_color=("black", "white")
        ).pack(pady=5)

        ctk.CTkButton(
            button_frame,
            text="Recuperar Contraseña",
            command=self.recuperar_contraseña,
            width=250,
            height=40,
            font=("Arial", 12),
            fg_color=("#ffc107", "#ffc107"),
            text_color=("black", "white")
        ).pack(pady=5)
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

    def volver_a_inicio(self):
        from view.welcome_view import WelcomeView
        self.destroy()
        WelcomeView(self.parent, self.controller).pack(fill="both", expand=True)
    def login(self):
        user = self.user.get().strip()
        password = self.password.get()
        rol = self.rol.get()

        if not user or not password:
            messagebox.showwarning("Validación", "Por favor complete todos los campos")
            return

        valido = self.controller.login(user, password, rol)

        if valido == True:
            self.controller.usuario_actual = user
            self.controller.rol_actual = rol
            self.destroy()
            from view.dashboard_view import DashboardView
            DashboardView(self.parent, self.controller).pack(fill="both", expand=True)
            return

        if valido == "not_verified":
            from tkinter import simpledialog
            messagebox.showinfo("Cuenta sin verificar", "Tu cuenta está pendiente de verificación. Revisa tu correo para el código.")
            code = simpledialog.askstring("Verificación", "Ingresa el código de verificación que recibiste por correo:")
            if code and self.controller.verificar_codigo(user, rol, code.strip()):
                messagebox.showinfo("Verificación", "Código correcto. Sesión iniciada.")
                self.controller.usuario_actual = user
                self.controller.rol_actual = rol
                self.destroy()
                from view.dashboard_view import DashboardView
                DashboardView(self.parent, self.controller).pack(fill="both", expand=True)
                return

            # Reintentar con re-envío opcional
            if messagebox.askyesno("Reenviar código", "¿Deseas reenviar un nuevo código de verificación? Si eliges No, puedes intentar el código manual otra vez."):
                if self.controller.reenviar_codigo(user, rol):
                    messagebox.showinfo("Código reenviado", "Se envió un nuevo código a tu correo.")
                else:
                    messagebox.showwarning("Error", "No se pudo reenviar el código. Revisa la configuración SMTP.")
            self.password.delete(0, "end")
            return

        messagebox.showerror("Error de autenticación", "Usuario o contraseña incorrectos")
        self.password.delete(0, "end")

    def recuperar_contraseña(self):
        user = self.user.get().strip()
        rol = self.rol.get()

        if not user:
            messagebox.showwarning("Validación", "Ingresa tu usuario para recuperar contraseña")
            return

        enviado = self.controller.solicitar_codigo_recuperacion(user, rol)
        if not enviado:
            messagebox.showerror("Error", "No se pudo enviar el código de recuperación. Verifica tu usuario y configuración de correo")
            return

        messagebox.showinfo("Recuperar contraseña", "Se envió un código a tu correo registrado")

        codigo = simpledialog.askstring("Código de recuperación", "Ingresa el código recibido en tu correo:")
        if not codigo:
            return

        if not self.controller.verificar_codigo_recuperacion(user, rol, codigo.strip()):
            messagebox.showerror("Error", "Código incorrecto")
            return

        nueva = simpledialog.askstring("Nueva contraseña", "Ingresa la nueva contraseña:", show="*")
        if not nueva or len(nueva) < 4:
            messagebox.showwarning("Validación", "La contraseña debe tener al menos 4 caracteres")
            return

        confirmacion = simpledialog.askstring("Confirmar contraseña", "Repite la nueva contraseña:", show="*")
        if confirmacion != nueva:
            messagebox.showwarning("Validación", "Las contraseñas no coinciden")
            return

        rest = self.controller.restablecer_contraseña_por_codigo(user, rol, codigo.strip(), nueva)
        if rest:
            messagebox.showinfo("Éxito", "Contraseña actualizada correctamente. Ahora inicia sesión.")
        else:
            messagebox.showerror("Error", "No se pudo actualizar la contraseña")

    def registro(self):
        self.destroy()
        RegistroView(self.parent, self.controller).pack(fill="both", expand=True)