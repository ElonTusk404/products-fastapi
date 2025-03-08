from src.models import ProductModel
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode
from src.schemas.queue import QueueOrderInfo
from typing import Tuple


class ReserveService(BaseService):
    base_repository: str = 'product'

    @transaction_mode
    async def reserve_order_products(self, order_info: QueueOrderInfo) -> Tuple[bool, QueueOrderInfo]:
        try:
            async with self.uow:
                total = 0  
                
                for item in order_info.items:
                    product: ProductModel = await self.uow.product.get_by_query_one_or_none(id=item.product_id)
                    
                    if not product:
                        raise ValueError(f"Product with id {item.product_id} not found")
                    
                    if product.quantity < item.quantity:
                        raise ValueError(
                            f"Not enough quantity for product {item.product_id}. "
                            f"Required: {item.quantity}, Available: {product.quantity}, Order ID: {order_info.id}"
                        )
                    
                    item_total = product.price * item.quantity
                    total += item_total
                    
                    updated_product = await self.uow.product.update_one_by_id(
                        obj_id=item.product_id,
                        quantity=product.quantity - item.quantity
                    )
                    
                    await self.uow.reserve.add_one(
                        order_id=order_info.id,
                        product_id=item.product_id,
                        quantity=item.quantity
                    )
                
                await self.uow.commit()
                
                order_info.total = total
                
                return True, order_info
                
        except Exception as e:
            await self.uow.rollback()
            return False, order_info