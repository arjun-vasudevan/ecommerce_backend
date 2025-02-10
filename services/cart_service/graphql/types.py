from strawberry import type
from typing import List


@type
class CartItemType:
    id: int
    productId: int
    quantity: int


@type
class CartType:
    id: int
    userId: str
    items: List[CartItemType]
