from dataclasses import dataclass
from typing import List
from decimal import Decimal

@dataclass
class CartItem:
    product: 'Product'  # Forward declaration for Product type
    quantity: int
    size: str
    price: Decimal

@dataclass
class Cart:
    items: List[CartItem]

    def total_price(self) -> Decimal:
        return sum(item.price * item.quantity for item in self.items)