from dataclasses import dataclass
from decimal import Decimal
from typing import Dict

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

    def validate_code(self, code: str) -> bool:
        return self.code == code