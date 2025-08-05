from decimal import Decimal
from typing import List, Dict
from src.models.discount import DiscountedPrice
from src.models.cart import CartItem
from src.models.payment import PaymentInfo

class BankDiscount:
    def __init__(self, bank_name: str, discount_percentage: Decimal):
        self.bank_name = bank_name
        self.discount_percentage = discount_percentage

    def apply_discount(self, cart_items: List[CartItem], payment_info: PaymentInfo) -> DiscountedPrice:
        if payment_info.bank_name != self.bank_name:
            return DiscountedPrice(
                original_price=self.calculate_original_price(cart_items),
                final_price=self.calculate_original_price(cart_items),
                applied_discounts={},
                message="No bank discount applied."
            )

        original_price = self.calculate_original_price(cart_items)
        discount_amount = (self.discount_percentage / Decimal(100)) * original_price
        final_price = original_price - discount_amount

        return DiscountedPrice(
            original_price=original_price,
            final_price=final_price,
            applied_discounts={f"{self.bank_name} discount": discount_amount},
            message=f"{self.discount_percentage}% discount applied for {self.bank_name}."
        )

    def calculate_original_price(self, cart_items: List[CartItem]) -> Decimal:
        return sum(item.product.current_price * item.quantity for item in cart_items)