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

def calculate_final_price(cart_items: List[CartItem], payment_info, voucher_code: str) -> DiscountedPrice:
    original_price = sum(item.product.base_price * item.quantity for item in cart_items)
    brand_discount = sum(calculate_brand_discount(item.product) * item.quantity for item in cart_items)
    category_discount = calculate_category_discount(cart_items)
    total_discount = brand_discount + category_discount
    
    total_price_after_discount = original_price - total_discount
    bank_discount = calculate_bank_discount(payment_info, total_price_after_discount)
    total_price_after_discount -= bank_discount
    
    voucher_discount = apply_voucher_discount(voucher_code, total_price_after_discount)
    final_price = total_price_after_discount - voucher_discount
    
    applied_discounts = {
        "Brand Discount": brand_discount,
        "Category Discount": category_discount,
        "Bank Discount": bank_discount,
        "Voucher Discount": voucher_discount
    }
    
    message = "Discounts applied successfully."
    
    return DiscountedPrice(original_price=original_price, final_price=final_price, applied_discounts=applied_discounts, message=message)