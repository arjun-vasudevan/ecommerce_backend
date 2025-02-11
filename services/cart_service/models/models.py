from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from services.database import Base


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, index=True, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    items = relationship("CartItem", back_populates="cart")

    def __str__(self):
        return f"Cart(id={self.id}, user_id={self.user_id})"


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, index=True, primary_key=True)
    cart_id = Column(Integer, ForeignKey("carts.id"))
    product_id = Column(Integer, nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    cart = relationship("Cart", back_populates="items")

    def __str__(self):
        return f"CartItem(id={self.id}, cart_id={self.cart_id}, product_id={self.product_id}, quantity={self.quantity})"
