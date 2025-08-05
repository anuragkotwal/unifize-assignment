from decimal import Decimal
from typing import List, Dict
from models import Product, CartItem, DiscountedPrice

def calculate_brand_discount(product: Product) -> Decimal:
    if product.brand == "PUMA":
        return product.base_price * Decimal('0.40')  # 40% off
    return Decimal('0.00')

def calculate_category_discount(cart_items: List[CartItem]) -> Decimal:
    total_discount = Decimal('0.00')
    for item in cart_items:
        if item.product.category == "T-shirt":
            total_discount += item.product.base_price * Decimal('0.10') * item.quantity  # 10% off
    return total_discount

def calculate_bank_discount(payment_info, total_price: Decimal) -> Decimal:
    if payment_info and payment_info.bank_name == "ICICI":
        return total_price * Decimal('0.10')  # 10% off
    return Decimal('0.00')

def apply_voucher_discount(voucher_code: str, total_price: Decimal) -> Decimal:
    if voucher_code == "SUPER69":
        return total_price * Decimal('0.69')  # 69% off
    return Decimal('0.00')