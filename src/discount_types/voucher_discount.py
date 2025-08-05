from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List

from src.models.cart import CartItem

@dataclass
class VoucherDiscount:
    code: str
    discount_percentage: Decimal
    max_discount_amount: Decimal

    def apply_discount(self, original_price: Decimal) -> Decimal:
        discount_amount = (original_price * self.discount_percentage) / Decimal(100)
        if discount_amount > self.max_discount_amount:
            discount_amount = self.max_discount_amount
        return original_price - discount_amount
    
    async def calculate_discount(self, cart_items: List[CartItem], customer) -> Decimal:
        original_price = self.calculate_original_price(cart_items)
        return (Decimal(str(self.discount_percentage)) / Decimal(100)) * original_price
    
    def calculate_original_price(self, cart_items: List[CartItem]) -> Decimal:
        return sum(item.product.current_price * item.quantity for item in cart_items)

    def validate_code(self, code: str) -> bool:
        return self.code == code