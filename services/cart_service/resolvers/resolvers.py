from fastapi import HTTPException
from httpx import AsyncClient
from strawberry.types import Info
from typing_extensions import Optional

from services.cart_service.graphql.types import CartType, CartItemType
from services.cart_service.resolvers.cache_utils import (
    cache_product,
    get_cached_product,
)


async def get_cart(info: Info) -> CartType:
    user_id = info.context["request"].state.user
    cart_repo = info.context["cart_repository"]

    return cart_repo.get_cart_by_user_id(user_id)


async def validate_product_id(product_id: int):
    if product_info := get_cached_product(product_id):
        return product_info

    async with AsyncClient() as client:
        # TODO: change URL
        response = await client.get(
            f"http://product_service:8001/api/products/{product_id}"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=404, detail=f"Product ID {product_id} not found"
        )

    product_info = response.json()
    cache_product(product_id, product_info)
    return product_info


async def add_item_to_cart(
    info: Info, product_id: int, quantity: Optional[int]
) -> CartItemType:
    # TODO: simplify this logic, too messy rn

    user_id = info.context["request"].state.user
    cart_repo = info.context["cart_repository"]

    # Check if it is a valid product
    try:
        product_info = await validate_product_id(product_id)
    except HTTPException as e:
        raise e

    with cart_repo.db.begin():
        # Retrieve the cart for the authenticated user
        cart = await get_cart(info)

        # If quantity is 0, remove the item from the cart
        if quantity == 0:
            if not cart:
                raise HTTPException(status_code=404, detail="Cart does not exist")

            # Get the cart item to remove
            if not (cart_item := cart_repo.get_cart_item(cart.id, product_id)):
                raise HTTPException(status_code=404, detail="Cart item does not exist")

            cart_repo.remove_item_from_cart(cart_item)
            cart_item.quantity = 0

            # If the cart is empty, delete it
            if not cart.items:
                cart_repo.delete_cart(cart)

            return CartItemType(
                id=cart_item.id,
                cart_id=cart_item.cart_id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
            )

        # Create cart if it doesn't exist
        if not cart:
            cart = cart_repo.create_cart(user_id)

        # Get the cart item to create or update
        cart_item = cart_repo.get_cart_item(cart.id, product_id)

        # Increment quantity if not provided
        if quantity is None:
            quantity = cart_item.quantity + 1 if cart_item else 1

        # Check if there is enough stock
        if quantity > product_info["stock"]:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for product ID {product_id}, only {product_info['stock']} available",
            )

        # Update or create the cart item
        if cart_item:
            cart_item = cart_repo.update_cart_item(cart_item, quantity)
        else:
            cart_item = cart_repo.add_item_to_cart(cart.id, product_id, quantity)

    # Return the cart item
    return CartItemType(
        id=cart_item.id,
        cart_id=cart_item.cart_id,
        product_id=cart_item.product_id,
        quantity=cart_item.quantity,
    )
