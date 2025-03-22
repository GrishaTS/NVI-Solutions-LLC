import os
import flet as ft

from app.config import settings
from app.views import (
    HomeView
)


def main(page: ft.Page) -> None:
    """
    Инициализирует основное приложение Flet.

    :param page: Экземпляр страницы Flet.
    """
    page.title = "Умная галерея"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.padding = 20
    page.window.min_width = 400
    page.window.min_height = 500

    def route_change(route: ft.RouteChangeEvent) -> None:
        """
        Обрабатывает изменение маршрута.

        :param route: Событие изменения маршрута.
        """
        print(f'INFO:\t{page.client_ip} - "{route.data}"', end=" ")
        troute = ft.TemplateRoute(route.data)
        page.views.clear()
        page.on_resized = None

        if troute.match(HomeView.ROUTE):
            page.views.append(HomeView(page))
        elif troute.match():
            ...
        else:
            print(f'- REDIRECT TO "{HomeView.ROUTE}"', end=" ")
            page.views.append(HomeView(page))
        page.update()

        if page.views:
            print("200 OK")

    page.on_route_change = route_change
    page.go("/")


if __name__ == "__main__":
    ft.app(
        target=main,
        host=settings.FRONTEND_HOST,
        port=settings.FRONTEND_PORT,
        view=ft.AppView.WEB_BROWSER,
    )