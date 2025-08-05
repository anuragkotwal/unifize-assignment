from dataclasses import dataclass
from decimal import Decimal
from typing import List, Dict
from src.models.product import Product
from src.models.discount import DiscountedPrice

@dataclass
class CategoryDiscount:
    category: str
    discount_percentage: Decimal

    def apply_discount(self, products: List[Product]) -> Dict[str, Decimal]:
        applied_discounts = {}
        for product in products:
            if product.category == self.category:
                discount_amount = product.base_price * (self.discount_percentage / Decimal(100))
                product.current_price -= discount_amount
                applied_discounts[f"{self.category} discount"] = discount_amount
        return applied_discounts

def calculate_category_discount(products: List[Product], category_discounts: List[CategoryDiscount]) -> DiscountedPrice:
    original_price = sum(product.base_price for product in products)
    applied_discounts = {}

    for category_discount in category_discounts:
        discounts = category_discount.apply_discount(products)
        applied_discounts.update(discounts)

    final_price = sum(product.current_price for product in products)
    message = f"Applied category discounts: {', '.join(applied_discounts.keys())}" if applied_discounts else "No category discounts applied."

    return DiscountedPrice(original_price=original_price, final_price=final_price, applied_discounts=applied_discounts, message=message)