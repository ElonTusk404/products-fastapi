__all__ = [
    'v1_product_router',
    'v1_queue_router'
]

from src.api.v1.routers.product import router as v1_product_router
from src.api.v1.routers.queue import router as v1_queue_router