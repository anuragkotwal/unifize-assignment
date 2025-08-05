from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List, Optional, Union

from src.discount_types.base_discount import BaseDiscount
from src.models.cart import CartItem
from src.models.customer import CustomerProfile
from src.models.payment import PaymentInfo

class VoucherDiscount(BaseDiscount):
    """
    Voucher-based discount implementation.
    Applies discounts when a valid voucher code is provided.
    """
    
    def __init__(self, code: str, discount_percentage: Union[float, Decimal], max_discount_amount: Union[float, Decimal]):
        super().__init__(
            discount_id=f"VOUCHER_{code.upper()}",
            discount_name=f"Voucher {code} Discount"
        )
        self.code = code
        # Ensure discount_percentage and max_discount_amount are Decimal
        self.discount_percentage = Decimal(str(discount_percentage))
        self.max_discount_amount = Decimal(str(max_discount_amount))

    async def is_applicable(
        self, 
        cart_items: List[CartItem], 
        customer: CustomerProfile,
        payment_info: Optional[PaymentInfo] = None,
        **kwargs
    ) -> bool:
        """Check if voucher code is valid and applicable"""
        # Check if voucher code is provided in kwargs
        provided_code = kwargs.get('voucher_code', '')
        return self.validate_code(provided_code)

    def apply_discount(self, original_price: Decimal) -> Decimal:
        discount_amount = (original_price * self.discount_percentage) / Decimal("100")
        if discount_amount > self.max_discount_amount:
            discount_amount = self.max_discount_amount
        return original_price - discount_amount
    
    async def calculate_discount(
        self, 
        cart_items: List[CartItem], 
        customer: CustomerProfile,
        payment_info: Optional[PaymentInfo] = None,
        **kwargs
    ) -> Decimal:
        """Calculate voucher discount amount"""
        if not await self.is_applicable(cart_items, customer, payment_info, **kwargs):
            return Decimal("0")
            
        original_price = self.calculate_original_price(cart_items)
        discount_amount = (original_price * self.discount_percentage) / Decimal("100")
        
        # Apply maximum discount limit
        if discount_amount > self.max_discount_amount:
            discount_amount = self.max_discount_amount
            
        return discount_amount
    
    def calculate_original_price(self, cart_items: List[CartItem]) -> Decimal:
        return sum(item.product.current_price * item.quantity for item in cart_items)

    def validate_code(self, code: str) -> bool:
        return self.code == code