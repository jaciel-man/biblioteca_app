import flet as ft
from biblioblog.controller.app_controller import AppController
from biblioblog.utils.theme import BG_PRIMARY

class App:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = "BiblioBlog - Sistema de Biblioteca"
        self.page.bgcolor = BG_PRIMARY
        self.page.theme_mode = ft.ThemeMode.LIGHT
        
        # Flet window config
        self.page.window.width = 1200
        self.page.window.height = 800
        self.page.padding = 0

        self.controller = AppController()

        self.current_view = None
        self.show_view("welcome")

    def show_view(self, view_name, **kwargs):
        from biblioblog.view.welcome_view import WelcomeView
        from biblioblog.view.login_view import LoginView
        from biblioblog.view.registro_view import RegistroView
        from biblioblog.view.dashboard_view import DashboardView

        views = {
            "welcome": WelcomeView,
            "login": LoginView,
            "registro": RegistroView,
            "dashboard": DashboardView,
        }

        if view_name not in views:
            return

        self.page.controls.clear()
        
        ViewClass = views[view_name]
        self.current_view = ViewClass(self, **kwargs)
        
        self.page.add(self.current_view.build())
        self.page.update()

def main(page: ft.Page):
    app = App(page)
