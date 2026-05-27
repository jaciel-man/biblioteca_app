import flet as ft
from biblioblog.utils.theme import PRIMARY_COLOR, SECONDARY_COLOR

class WelcomeView:
    def __init__(self, app):
        self.app = app

    def build(self):
        return ft.Container(
            expand=True,
            bgcolor='#1e1b4b',
            alignment=ft.Alignment(0, 0),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=40,
                controls=[
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                        controls=[
                            ft.Text("📚", size=90),
                            ft.Text("BiblioBlog", size=40, weight=ft.FontWeight.BOLD, color="#e0e7ff"),
                            ft.Text("Sistema de Gestión de Biblioteca", size=18, color="#a5b4fc"),
                            ft.Text("Accede y explora nuestra colección", size=14, color="#818cf8"),
                        ]
                    ),
                    ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=20,
                        controls=[
                            ft.ElevatedButton(
                                content=ft.Container(
                                    content=ft.Text("✓ Iniciar Sesión", size=16, weight=ft.FontWeight.BOLD),
                                    alignment=ft.Alignment(0, 0),
                                    height=52,
                                    width=300
                                ),
                                style=ft.ButtonStyle(
                                    bgcolor='#4f46e5',
                                    color=ft.Colors.WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                ),
                                on_click=lambda _: self.app.show_view("login")
                            ),
                            ft.ElevatedButton(
                                content=ft.Container(
                                    content=ft.Text("+ Crear Nueva Cuenta", size=16, weight=ft.FontWeight.BOLD),
                                    alignment=ft.Alignment(0, 0),
                                    height=52,
                                    width=300
                                ),
                                style=ft.ButtonStyle(
                                    bgcolor='#0891b2',
                                    color=ft.Colors.WHITE,
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                ),
                                on_click=lambda _: self.app.show_view("registro")
                            )
                        ]
                    )
                ]
            )
        )
