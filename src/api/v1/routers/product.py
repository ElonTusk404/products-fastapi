from typing import Annotated
from fastapi import status, APIRouter, Depends
from src.schemas.token import DecodedToken
from src.api.v1.services import ProductService
from src.schemas.product import CreateProductRequest, CreateProductResponse, UpdateProductRequest
from faststream.rabbit import RabbitBroker, RabbitRouter
router = APIRouter(prefix='/products', tags=['Продукты | v1'])
from src.utils.jwt import get_current_user

@router.post(
    '',
    status_code=status.HTTP_201_CREATED
)
async def create_product(
    product_data: CreateProductRequest,
    current_user: DecodedToken = Depends(get_current_user("write:products")),
    
    service: ProductService = Depends(ProductService),
    
):
    return await service.create_product(product_data)


@router.delete(
    '/{product_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_product(
    product_id: int,
    current_user: DecodedToken = Depends(get_current_user("delete:products")),
    service: ProductService = Depends(ProductService)
):
    return await service.delete_product(product_id)


@router.put(
    '/{product_id}',
    status_code=status.HTTP_200_OK
)
async def update_product(
    product_id: int,
    product_data: UpdateProductRequest,
    current_user: DecodedToken = Depends(get_current_user("update:products")),
    service: ProductService = Depends(ProductService)
):
    return await service.update_product(product_id, product_data)

@router.get(
    '/{product_id}',
    status_code=status.HTTP_200_OK
)
async def get_product(
    product_id: int,
    current_user: DecodedToken = Depends(get_current_user("read:products")),
    service: ProductService = Depends(ProductService)
):
    return await service.get_product(product_id)



