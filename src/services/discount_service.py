from typing import List, Optional, Dict
from decimal import Decimal

from src.models.cart import CartItem
from src.models.customer import CustomerProfile
from src.models.discount import DiscountedPrice
from src.discount_types.brand_discount import BrandDiscount
from src.discount_types.category_discount import CategoryDiscount
from src.discount_types.bank_discount import BankDiscount
from src.discount_types.voucher_discount import VoucherDiscount
from src.models.payment import PaymentInfo

class DiscountService:
    async def calculate_cart_discounts(
    self,
    cart_items: List[CartItem],
    customer: CustomerProfile,
    payment_info: Optional[PaymentInfo] = None,
    voucher_code: Optional[str] = None
    ) -> DiscountedPrice:
        # Initialize with cart total from current prices
        original_price = sum(item.product.current_price * item.quantity for item in cart_items)
        final_price = original_price
        applied_discounts = {}
        
        # Apply bank discount if payment info provided
        if payment_info:
            bank_discount = BankDiscount(payment_info.bank_name, 10.0)  # Example: 10% discount
            bank_result = await bank_discount.calculate_discount(cart_items, customer)
            if bank_result > 0:
                applied_discounts[f"{payment_info.bank_name} Bank Offer"] = bank_result
                final_price -= bank_result
        
        # Apply voucher discount if voucher code provided
        if voucher_code:
            voucher_discount = VoucherDiscount(voucher_code, 15.0, 100.0)  # Example: 15% discount, max $100
            voucher_result = await voucher_discount.calculate_discount(cart_items, customer)
            if voucher_result > 0:
                applied_discounts[f"Voucher {voucher_code}"] = voucher_result
                final_price -= voucher_result
        
        return DiscountedPrice(
            original_price=original_price,
            final_price=max(final_price, Decimal('0')),  # Ensure non-negative
            applied_discounts=applied_discounts,
            message="Discounts applied successfully"
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