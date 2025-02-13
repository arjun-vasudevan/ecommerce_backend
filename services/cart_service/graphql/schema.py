from strawberry import field, mutation, Schema, type
from strawberry.types import Info
from typing import Optional

from services.cart_service.graphql.types import CartType, CartItemType
from services.cart_service.resolvers.resolvers import get_cart, add_item_to_cart


@type
class Query:
    cart: Optional[CartType] = field(resolver=get_cart)


@type
class Mutation:

    @mutation()
    async def add_cart_item(
        self, info: Info, product_id: int, quantity: Optional[int] = None
    ) -> CartItemType:
        return await add_item_to_cart(info, product_id, quantity)


schema = Schema(query=Query, mutation=Mutation)
