from abc import ABC, abstractmethod
from typing import Optional

from services.cart_service.models.models import Cart, CartItem


class CartRepository(ABC):

    @abstractmethod
    def get_cart_by_user_id(self, user_id: int) -> Optional[Cart]:
        pass

    @abstractmethod
    def create_cart(self, user_id) -> Cart:
        pass

    def delete_cart(self, cart: Cart) -> None:
        pass


    @abstractmethod
    def get_cart_item(self, cart_id: int, product_id: int) -> Optional[CartItem]:
        pass

    @abstractmethod
    def add_item_to_cart(self, user_id: str, product_id: int, quantity: int) -> CartItem:
        pass

    @abstractmethod
    def update_cart_item(self, cart_item: CartItem, quantity: int) -> CartItem:
        pass

    @abstractmethod
    def remove_item_from_cart(self, cart_item: CartItem) -> None:
        pass
