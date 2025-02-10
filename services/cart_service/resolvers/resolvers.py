from strawberry.types import Info

from services.cart_service.graphql.types import CartType, CartItemType


async def get_cart(info: Info) -> CartType:
    user_id = info.context["request"].state.user
    repository = info.context["cart_repository"]

    return repository.get_cart_by_user_id(user_id)
