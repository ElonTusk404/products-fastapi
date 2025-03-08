from dataclasses import dataclass

from fastapi import Query
from pydantic import UUID4, BaseModel, Field




class CreateProductRequest(BaseModel):
    name: str = Field(..., min_length=3, max_length=255)
    description: str = Field(..., min_length=3, max_length=255)
    price: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)

class CreateProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: int
    quantity: int

class UpdateProductRequest(BaseModel):
    name: str = Field(None, min_length=3, max_length=255)
    description: str = Field(None, min_length=3, max_length=255)
    price: int = Field(None, gt=0)
    quantity: int = Field(None, gt=0)

class UpdateProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: int
    quantity: int

class GetProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: int
    quantity: int
    created_at: str
    updated_at: str