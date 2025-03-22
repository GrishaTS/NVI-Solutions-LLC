import httpx

from app.config import settings


def add_rectangle(client: httpx.Client, x: float, y: float, width: float, height: float) -> int:
    response = client.post(
        f"{settings.BACKEND_URL}/rectangles/",
        json={
            "x1": x,
            "y1": y,
            "x2": x+width,
            "y2": y+height,
        }
    )
    response.raise_for_status()
    return response.json()["rectangle_id"]


def intersection_area(x1, y1, w1, h1, x2, y2, w2, h2) -> float:
    with httpx.Client(http1=True) as client:
        rect1_id = add_rectangle(client, x1, y1, w1, h1)
        rect2_id = add_rectangle(client, x2, y2, w2, h2)

        resp = client.post(
            f"{settings.BACKEND_URL}/rectangles/intersect",
            params={
                "rectangle1_id": rect1_id,
                "rectangle2_id": rect2_id,
            }
        )
        resp.raise_for_status()
        return resp.json()["intersection_area"]
