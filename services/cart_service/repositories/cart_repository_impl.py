from sqlalchemy.orm import Session
from typing import Optional

from services.cart_service.models.models import Cart, CartItem
from services.cart_service.repositories.cart_repository_interface import CartRepository


class CartRepositoryImpl(CartRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_cart_by_user_id(self, user_id: str) -> Optional[Cart]:
        return self.db.query(Cart).filter(Cart.user_id == user_id).first()

    def create_cart(self, user_id) -> Cart:
        cart = Cart(user_id=user_id)
        self.db.add(cart)
        self.db.flush()
        return cart

    def delete_cart(self, cart: Cart) -> None:
        self.db.delete(cart)
        self.db.flush()


    def get_cart_item(self, cart_id: int, product_id: int) -> Optional[CartItem]:
        return self.db.query(CartItem).filter(CartItem.cart_id == cart_id, CartItem.product_id == product_id).first()

    def add_item_to_cart(self, cart_id: int, product_id: int, quantity: int) -> CartItem:
        cart_item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
        self.db.add(cart_item)
        self.db.flush()
        return cart_item

    def update_cart_item(self, cart_item: CartItem, quantity: int) -> CartItem:
        cart_item.quantity = quantity
        self.db.flush()
        return cart_item

    def remove_item_from_cart(self, cart_item: CartItem) -> None:
        self.db.delete(cart_item)
        self.db.flush()
