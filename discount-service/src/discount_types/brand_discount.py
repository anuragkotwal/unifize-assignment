from decimal import Decimal
from typing import List, Dict
from src.models.product import Product
from src.models.discount import DiscountedPrice

class BrandDiscount:
    def __init__(self, brand: str, discount_percentage: Decimal):
        self.brand = brand
        self.discount_percentage = discount_percentage

    def apply_discount(self, product: Product) -> Decimal:
        if product.brand == self.brand:
            discount_amount = product.base_price * (self.discount_percentage / Decimal(100))
            return discount_amount
        return Decimal(0)

def calculate_brand_discounts(cart_items: List[Product], brand_discounts: List[BrandDiscount]) -> DiscountedPrice:
    original_price = sum(item.base_price for item in cart_items)
    total_discount = Decimal(0)
    applied_discounts = {}

    for discount in brand_discounts:
        for item in cart_items:
            discount_amount = discount.apply_discount(item)
            if discount_amount > 0:
                total_discount += discount_amount
                applied_discounts[discount.brand] = applied_discounts.get(discount.brand, Decimal(0)) + discount_amount

    final_price = original_price - total_discount
    message = f"Total discounts applied: {len(applied_discounts)}"

    return DiscountedPrice(original_price=original_price, final_price=final_price, applied_discounts=applied_discounts, message=message)