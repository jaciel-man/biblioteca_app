import customtkinter as ctk
from controller.app_controller import AppController
from services.notification_service import NotificationService
from view.welcome_view import WelcomeView

class App(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("BiblioBlog - Sistema de Biblioteca")
        self.geometry("1000x600")
        
        # Configurar tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.controller = AppController()
        self.notification_service = NotificationService()

        self.frame = WelcomeView(self, self.controller)
        self.frame.pack(fill="both", expand=True)