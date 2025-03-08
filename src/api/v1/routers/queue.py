from typing import Annotated
from fastapi import Depends, FastAPI
from pydantic import BaseModel
from src.config import settings
from faststream.rabbit.fastapi import RabbitRouter, Logger
from src.schemas.queue import QueueOrderInfo
from src.api.v1.services import ReserveService
router = RabbitRouter(settings.RABBITMQ)

class CartMessage(BaseModel):
    product_id: int
    quantity: int

def call():
    return True

def broker():
    return router.broker


@router.subscriber("order_created", )
async def order_created(order_info: QueueOrderInfo, d=Depends(call),  service: ReserveService = Depends(ReserveService)):
    status, result = await service.reserve_order_products(order_info)
    if status:
        await router.broker.publish(
            queue='order_items_reserved',
            message=result
        )
    else:
        await router.broker.publish(
            queue='order_items_unavailable',
            message=result
        )
