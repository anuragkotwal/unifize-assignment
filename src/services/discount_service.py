from typing import List, Optional, Dict
from decimal import Decimal

from src.models.cart import CartItem
from src.models.customer import CustomerProfile
from src.models.discount import DiscountedPrice
from src.discount_types.brand_discount import BrandDiscount
from src.discount_types.category_discount import CategoryDiscount
from src.discount_types.bank_discount import BankDiscount
from src.discount_types.voucher_discount import VoucherDiscount

class DiscountService:
    async def calculate_cart_discounts(
        self,
        cart_items: List[CartItem],
        customer: CustomerProfile,
        payment_info: Optional[PaymentInfo] = None
    ) -> DiscountedPrice:
        original_price = sum(item.product.current_price * item.quantity for item in cart_items)
        final_price = original_price
        applied_discounts = {}
        messages = []

        # Apply brand-specific discounts
        brand_discount = BrandDiscount()
        brand_discount_amount, brand_message = brand_discount.apply(cart_items)
        if brand_discount_amount > 0:
            final_price -= brand_discount_amount
            applied_discounts["Brand Discount"] = brand_discount_amount
            messages.append(brand_message)

        # Apply category-specific discounts
        category_discount = CategoryDiscount()
        category_discount_amount, category_message = category_discount.apply(cart_items)
        if category_discount_amount > 0:
            final_price -= category_discount_amount
            applied_discounts["Category Discount"] = category_discount_amount
            messages.append(category_message)

        # Apply voucher discounts
        voucher_discount = VoucherDiscount()
        voucher_discount_amount, voucher_message = voucher_discount.apply(cart_items)
        if voucher_discount_amount > 0:
            final_price -= voucher_discount_amount
            applied_discounts["Voucher Discount"] = voucher_discount_amount
            messages.append(voucher_message)

        # Apply bank offers
        if payment_info:
            bank_discount = BankDiscount()
            bank_discount_amount, bank_message = bank_discount.apply(payment_info, final_price)
            if bank_discount_amount > 0:
                final_price -= bank_discount_amount
                applied_discounts["Bank Offer"] = bank_discount_amount
                messages.append(bank_message)

        return DiscountedPrice(
            original_price=Decimal(original_price),
            final_price=Decimal(final_price),
            applied_discounts=applied_discounts,
            message="; ".join(messages)
        )

    async def validate_discount_code(
        self,
        code: str,
        cart_items: List[CartItem],
        customer: CustomerProfile
    ) -> bool:
        # Implement validation logic for discount codes
        # This could involve checking against brand exclusions, category restrictions, etc.
        # For now, we will return True as a placeholder
        return True