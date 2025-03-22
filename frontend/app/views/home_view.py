import flet as ft

from app.views.base_view import BaseView
from app.routes import ViewRoutes
import httpx

class HomeView(BaseView):
    """
    Главная страница приложения.
    """

    ROUTE = ViewRoutes.HOME

    def __init__(self, page: ft.Page):
        """
        Инициализирует главную страницу.

        :param page: Экземпляр страницы Flet.
        """
        super().__init__(page)
        self.assemble_page()

    def assemble_page(self) -> None:
        """
        Собирает компоненты главной страницы.
        """
        try:
            with httpx.Client(http1=True, headers={"User-Agent": "Mozilla/5.0"}) as client:
                response = client.get("https://raw.githubusercontent.com/GrishaTS/GrishaTS/main/README.md")
                response.raise_for_status()
                readme_content = response.text
        except Exception as e:
            readme_content = f"Не удалось загрузить README.md: {e}"
        try:
            with httpx.Client(http1=True, headers={"User-Agent": "Mozilla/5.0"}) as client:
                response = client.get("https://raw.githubusercontent.com/GrishaTS/NVI-Solutions-LLC/main/README.md")
                response.raise_for_status()
                project_content = response.text
        except Exception as e:
            project_content = f"Не удалось загрузить README.md: {e}"
        self.controls = [
            ft.Container(
                content=ft.Column(
                    [
                        ft.TextButton(
                            "Перейти к пересечению прямоугольников",
                            on_click=lambda e: self.page.go(ViewRoutes.RECTANGLE_INTERSECTION)
                        ),
                        ft.Divider(),
                        ft.TextButton(
                            "Ссылка на проект",
                            url='https://github.com/GrishaTS/NVI-Solutions-LLC'
                        ),
                        ft.Markdown(project_content, selectable=True),
                        ft.Divider(),
                        ft.TextButton(
                            "Ссылка на гит (очень прошу ознакомиться с проектами указанными в конце этого README.md)",
                            url='https://github.com/GrishaTS'
                        ),
                        ft.Markdown(readme_content, selectable=True),
                    ],
                    scroll="auto",
                ),
                expand=True
            )
        ]