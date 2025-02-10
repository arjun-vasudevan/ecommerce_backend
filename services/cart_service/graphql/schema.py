from strawberry import field, Schema, type
from typing import Optional

from services.cart_service.graphql.types import CartType
from services.cart_service.resolvers.resolvers import get_cart

@type
class Query:
    cart: Optional[CartType] = field(resolver=get_cart)


schema = Schema(query=Query)
