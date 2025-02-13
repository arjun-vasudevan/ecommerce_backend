from strawberry import type
from typing import List


@type
class CartItemType:
    id: int
    cart_id: int
    product_id: int
    quantity: int


@type
class CartType:
    id: int
    user_id: str
    items: List[CartItemType]
