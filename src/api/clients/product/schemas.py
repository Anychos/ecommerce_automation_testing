from typing import List

from pydantic import BaseModel, Field

from src.api.tools.data_generator import fake_ru


class ProductSchema(BaseModel):
    name: str
    description: str
    price: float
    category: str
    is_available: bool
    image_url: str
    stock_quantity: int


class CreateProductRequestSchema(ProductSchema):
    name: str = Field(default_factory=fake_ru.object_name)
    description: str = Field(default_factory=fake_ru.description)
    price: float = Field(default_factory=fake_ru.price)
    category: str = Field(default_factory=fake_ru.category)
    is_available: bool = Field(default_factory=fake_ru.availability)
    image_url: str = Field(default_factory=fake_ru.image_url)
    stock_quantity: int = Field(default_factory=fake_ru.quantity)


class CreateProductResponseSchema(ProductSchema):
    id: int


class FullUpdateProductRequestSchema(CreateProductRequestSchema):
    pass


class PartialUpdateProductRequestSchema(ProductSchema):
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)
    price: float | None = Field(default=None)
    category: str | None = Field(default=None)
    is_available: bool | None = Field(default=None)
    image_url: str | None = Field(default=None)
    stock_quantity: int | None = Field(default=None)


class UpdateProductResponseSchema(CreateProductResponseSchema):
    pass


class GetProductResponseSchema(CreateProductResponseSchema):
    pass


GetProductsResponseSchema = List[GetProductResponseSchema]


class DeleteProductResponseSchema(BaseModel):
    message: str
