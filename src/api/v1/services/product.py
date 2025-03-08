from fastapi import HTTPException, status
from faststream.rabbit import RabbitBroker
from src.models import ProductModel
from src.schemas.product import CreateProductRequest, UpdateProductRequest, CreateProductResponse, GetProductResponse, UpdateProductResponse
from src.utils.service import BaseService
from src.utils.unit_of_work import transaction_mode


class ProductService(BaseService):
    base_repository: str = 'product'

   

    @transaction_mode
    async def create_product(self, product_data: CreateProductRequest) -> CreateProductResponse:
        new_product: ProductModel = await self.uow.product.add_one_and_get_obj(**product_data.model_dump())

        if new_product:
            return new_product

    @transaction_mode
    async def delete_product(self, product_id: int) -> None:
        product: ProductModel = await self.uow.product.get_by_query_one_or_none(id=product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        await self.uow.product.delete_by_query(id=product.id)

    @transaction_mode
    async def update_product(self, product_id: int, product_data: UpdateProductRequest) -> UpdateProductResponse:
        product: ProductModel = await self.uow.product.get_by_query_one_or_none(id=product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
        updated_product: ProductModel = await self.uow.product.update_one_by_id(
            obj_id=product.id,
            **product_data.model_dump(exclude_none=True)
        )
        
        return updated_product

    @transaction_mode
    async def get_product(self, product_id: int) -> GetProductResponse:
        product: ProductModel = await self.uow.product.get_by_query_one_or_none(id=product_id)
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return product