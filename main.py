from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.api import health_router
from src.api.v1.routers import v1_product_router, v1_queue_router


"""@asynccontextmanager
async def lifespan(app: FastAPI):
    # Подключение брокера при старте
    await broker.connect()
    print("Брокер RabbitMQ подключён")
    
    yield  # Здесь приложение работает
    
    # Отключение брокера при завершении
    await broker.close()
    print("Брокер RabbitMQ отключён")


"""
app = FastAPI(
    title="Products API",
    version="1.0.0",
    openapi_tags=[
        {"name": "healthz", "description": "Проверка состояния сервиса"},
        {"name": "Продукты | v1", "description": "Эндпоинты для продуктов"}
    ],
)


app.include_router(health_router)
app.include_router(v1_product_router, prefix='/v1')
app.include_router(v1_queue_router)