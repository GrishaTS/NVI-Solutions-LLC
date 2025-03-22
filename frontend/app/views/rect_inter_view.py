import flet as ft
import flet.canvas as ft_cv
from flet import Paint, PaintingStyle
from app.views.base_view import BaseView
from app.routes import ViewRoutes

from app.api import intersection_area

class RectangleIntersectionView(BaseView):
    """
    Главная страница приложения для рисования прямоугольников.
    """

    ROUTE = ViewRoutes.RECTANGLE_INTERSECTION

    def __init__(self, page: ft.Page):
        """
        Инициализирует главную страницу.

        :param page: Экземпляр страницы Flet.
        """
        super().__init__(page)
        
        # Начальная и конечная точки для текущего рисуемого прямоугольника
        self.start_x = 0
        self.start_y = 0
        self.current_rect = None
        self.rectangles = []

        # Кисть для отрисовки
        self.paint = Paint(
            color="blue",
            style=PaintingStyle.STROKE,
            stroke_width=2
        )

        # Холст
        self.canvas = ft_cv.Canvas(controls=[])

        # Обертка для жестов мыши
        self.detector = ft.GestureDetector(
            content=self.canvas,
            on_pan_start=self.on_pan_start,
            on_pan_update=self.on_pan_update,
            on_pan_end=self.on_pan_end
        )

        self.assemble_page()

    def assemble_page(self) -> None:
        """
        Собирает компоненты главной страницы.
        """
        self.controls = [
            ft.Text("Нарисуйте прямоугольник, удерживая мышь:"),
            self.detector
        ]

    def on_pan_start(self, e: ft.DragStartEvent):
        self.start_x = e.local_x
        self.start_y = e.local_y
        self.current_rect = ft_cv.Rect(
            left=self.start_x,
            top=self.start_y,
            right=self.start_x,
            bottom=self.start_y,
            paint=self.paint
        )
        self.canvas.controls.append(self.current_rect)
        self.canvas.update()

    def on_pan_update(self, e: ft.DragUpdateEvent):
        if self.current_rect:
            self.current_rect.right = e.local_x
            self.current_rect.bottom = e.local_y
            self.canvas.update()

    def on_pan_end(self, e: ft.DragEndEvent):
        if self.current_rect:
            self.rectangles.append(self.current_rect)
            self.current_rect = None
import flet as ft
import flet.canvas as ft_cv
from flet import Paint, PaintingStyle
from app.views.base_view import BaseView
from app.routes import ViewRoutes


class RectangleIntersectionView(BaseView):
    """
    Главная страница приложения для рисования прямоугольников.
    """

    ROUTE = ViewRoutes.RECTANGLE_INTERSECTION
    CANVAS_WIDTH = 400
    CANVAS_HEIGHT = 400

    def __init__(self, page: ft.Page):
        """
        Инициализирует главную страницу.

        :param page: Экземпляр страницы Flet.
        """
        super().__init__(page)
        
        # Начальная и конечная точки для текущего рисуемого прямоугольника
        self.start_x = 0
        self.start_y = 0
        self.current_rect = None
        self.rectangles: list[ft_cv.Rect] = []

        # Кисть для отрисовки
        self.paint = Paint(
            color="blue",
            style=PaintingStyle.STROKE,
            stroke_width=2
        )
        # Холст
        self.canvas = ft_cv.Canvas(width=self.CANVAS_WIDTH, height=self.CANVAS_HEIGHT)

        # Обертка для жестов мыши
        self.detector = ft.GestureDetector(
            content=self.canvas,
            on_pan_start=self.on_pan_start,
            on_pan_update=self.on_pan_update,
            on_pan_end=self.on_pan_end
        )


        self.assemble_page()

    def assemble_page(self) -> None:
        """
        Собирает компоненты главной страницы.
        """
        self.rect_info = ft.Text()
        self.area = ft.Text(value='Площадь пересечения: ')
        self.controls = [
            ft.Text("Нарисуйте прямоугольник, удерживая мышь:"),
            ft.Container(self.detector, border=ft.border.all(3, 'white')),
            self.rect_info,
            self.area
        ]

    def on_pan_start(self, e: ft.DragStartEvent):
        if len(self.rectangles) == 2:
            self.canvas.shapes.clear()
            self.rectangles.clear()
            self.rect_info.value = ""
            self.area.value = "Площадь пересечения: "
        self.start_x = max(e.local_x, 0)
        self.start_y = max(e.local_y, 0)
        self.current_rect = ft_cv.Rect(
            x=self.start_x,
            y=self.start_y,
            width=0,
            height=0,
            paint=self.paint
        )
        self.canvas.shapes.append(self.current_rect)
        self.canvas.update()

    def on_pan_update(self, e: ft.DragUpdateEvent):
        if self.current_rect:
            new_width = min(e.local_x - self.start_x, self.CANVAS_WIDTH - self.start_x)
            new_height = min(e.local_y - self.start_y, self.CANVAS_HEIGHT - self.start_y)
            self.current_rect.width = abs(new_width)
            self.current_rect.height = abs(new_height)
            self.current_rect.x = self.start_x if new_width >= 0 else e.local_x
            self.current_rect.y = self.start_y if new_height >= 0 else e.local_y
            self.canvas.update()

    def on_pan_end(self, e: ft.DragEndEvent):
        if self.current_rect:
            self.rectangles.append(self.current_rect)
            self.current_rect = None
        if len(self.rectangles) == 2:
            rect1 = self.rectangles[0]
            rect2 = self.rectangles[1]

            rect1_info = f"Rect1: x={rect1.x}, y={rect1.y}, w={rect1.width}, h={rect1.height}"
            rect2_info = f"Rect2: x={rect2.x}, y={rect2.y}, w={rect2.width}, h={rect2.height}"
            self.rect_info.value = f"{rect1_info}\n{rect2_info}"

            area = intersection_area(
                rect1.x, rect1.y, rect1.width, rect1.height,
                rect2.x, rect2.y, rect2.width, rect2.height
            )

            self.area.value = f"Площадь пересечения: {area}"

        self.page.update()
        
