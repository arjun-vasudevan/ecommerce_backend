from strawberry.types import Info
from typing_extensions import Optional

from services.cart_service.graphql.types import CartType, CartItemType


async def get_cart(info: Info) -> CartType:
    user_id = info.context["request"].state.user
    cart_repo = info.context["cart_repository"]

    return cart_repo.get_cart_by_user_id(user_id)


async def add_item_to_cart(info: Info, product_id: int, quantity: Optional[int]) -> CartItemType:
    # TODO: simplify this logic, too messy rn

    user_id = info.context["request"].state.user
    cart_repo = info.context["cart_repository"]

    with cart_repo.db.begin():
        cart = cart_repo.get_cart_by_user_id(user_id)

        # If quantity is 0, remove the item from the cart
        if quantity == 0:
            if not cart:
                raise Exception("Cart not found")

            cart_item = cart_repo.get_cart_item(cart.id, product_id)

            if not cart_item:
                raise Exception("Item not found in cart")

            cart_repo.remove_item_from_cart(cart_item)
            cart_item.quantity = 0

            remaining_items = cart_repo.get_cart_by_user_id(user_id).items
            if not remaining_items:
                cart_repo.delete_cart(cart)

            return CartItemType(
                id=cart_item.id,
                cart_id=cart_item.cart_id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity
            )


        if not cart:
            cart = cart_repo.create_cart(user_id)

        cart_item = cart_repo.get_cart_item(cart.id, product_id)

        if quantity is None:
            quantity = cart_item.quantity + 1 if cart_item else 1

        if cart_item:
            cart_item = cart_repo.update_cart_item(cart_item, quantity)
        else:
            cart_item = cart_repo.add_item_to_cart(cart.id, product_id, quantity)

    return CartItemType(
        id=cart_item.id,
        cart_id=cart_item.cart_id,
        product_id=cart_item.product_id,
        quantity=cart_item.quantity
    )
