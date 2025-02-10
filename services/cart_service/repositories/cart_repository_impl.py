from sqlalchemy.orm import Session
from typing import Optional

from services.cart_service.models.models import Cart
from services.cart_service.repositories.cart_repository_interface import CartRepository


class CartRepositoryImpl(CartRepository):

    def __init__(self, db: Session):
        self.db = db

    def get_cart_by_user_id(self, user_id: str) -> Optional[Cart]:
        return self.db.query(Cart).filter(Cart.user_id == user_id).first()
