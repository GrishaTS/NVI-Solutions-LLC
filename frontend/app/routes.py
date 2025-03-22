from dataclasses import dataclass


@dataclass(frozen=True)
class ViewRoutes:
    """
    Класс для хранения маршрутов приложения.
    """

    HOME: str = "/"
    RECTANGLE_INTERSECTION: str = "/rectangle_intersection"
