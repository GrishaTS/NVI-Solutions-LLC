# 🔷 Rectangle Intersector

Веб-приложение для рисования двух прямоугольников на холсте и вычисления площади их пересечения.

---

## 🐳 Быстрый старт (Docker)

Запуск проекта с переменными окружения
```bash
docker compose --env-file .env.dev up --build
```
---

## 📦 Описание

Приложение состоит из двух частей:

- 🧠 **Backend (FastAPI)**  
  Обрабатывает координаты прямоугольников, сохраняет их в PostgreSQL и рассчитывает площадь пересечения.
  
- 🖼️ **Frontend (Flet)**  
  Веб-интерфейс, в котором можно нарисовать два прямоугольника на холсте и получить площадь их пересечения.

---

## 🚀 Основной функционал

✅ Интерактивное рисование прямоугольников  
✅ Отправка координат на сервер  
✅ Расчёт площади пересечения  
✅ Очистка холста при добавлении новых фигур  
✅ Swagger UI для ручного тестирования API

---

## 🗃 Как работает база данных

Используются две таблицы:

### 📌 `rectangles`
| Поле | Тип | Описание |
|------|-----|----------|
| `id` | int | Уникальный идентификатор |
| `x1`, `y1`, `x2`, `y2` | float | Координаты противоположных углов прямоугольника |

### 📌 `rectangle_intersections`
| Поле | Тип | Описание |
|------|-----|----------|
| `id` | int | Уникальный идентификатор |
| `rectangle1_id`, `rectangle2_id` | int | Ссылки на пересекающиеся прямоугольники |
| `intersection_area` | float | Площадь пересечения |

🔁 Если пара прямоугольников уже встречалась, результат берётся из кэша, а не рассчитывается заново — это повышает производительность.

---

## 🧱 Стек технологий

- 🐍 **Python 3.11+**
- ⚡ **FastAPI** — легковесный backend-фреймворк
- 🖥️ **Flet** — Python-фреймворк для создания UI
- 🐘 **PostgreSQL** — надёжная СУБД
- 🔁 **SQLAlchemy (async)** — асинхронная работа с базой
- 🐳 **Docker + Compose** — контейнеризация и оркестрация

---

После запуска, backend и frontend будут доступы по адресам: 

📄 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

📄 [http://localhost:3000](http://localhost:3000)

---
