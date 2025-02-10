from abc import ABC, abstractmethod
from typing import Optional

from services.cart_service.models.models import Cart


class CartRepository(ABC):

    @abstractmethod
    def get_cart_by_user_id(self, user_id: int) -> Optional[Cart]:
        pass
