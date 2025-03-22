from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.router import router_health, router_rectangle
from app.database import create_tables, delete_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.APP_MODE == 'DEV':
        await delete_tables()
        print('База очищена')
    await create_tables()
    print('База готова к работе')
    yield
    print('Выключение')

app = FastAPI(lifespan=lifespan)
app.include_router(router_health)
app.include_router(router_rectangle)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)