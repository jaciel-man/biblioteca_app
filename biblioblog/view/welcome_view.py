import customtkinter as ctk

class WelcomeView(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.configure(fg_color=("#f0f0f0", "#1a1a1a"))

        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(expand=True)

        title = ctk.CTkLabel(main_frame, text="📚 Bienvenido a BiblioBlog", font=("Arial", 32, "bold"))
        title.pack(pady=(0, 30))

        subtitle = ctk.CTkLabel(main_frame, text="Inicia sesión o crea una nueva cuenta", font=("Arial", 14), text_color=("gray60", "gray70"))
        subtitle.pack(pady=(0, 40))

        ctk.CTkButton(
            main_frame,
            text="Iniciar Sesión",
            command=self.iniciar_sesion,
            width=300,
            height=45,
            font=("Arial", 12, "bold"),
            fg_color=("#0078d4", "#0078d4")
        ).pack(pady=10)

        ctk.CTkButton(
            main_frame,
            text="Crear Nueva Cuenta",
            command=self.crear_cuenta,
            width=300,
            height=45,
            font=("Arial", 12, "bold"),
            fg_color=("#28a745", "#28a745")
        ).pack(pady=10)

    def iniciar_sesion(self):
        from view.login_view import LoginView
        self.destroy()
        LoginView(self.parent, self.controller).pack(fill="both", expand=True)

    def crear_cuenta(self):
        from view.registro_view import RegistroView
        self.destroy()
        RegistroView(self.parent, self.controller).pack(fill="both", expand=True)
