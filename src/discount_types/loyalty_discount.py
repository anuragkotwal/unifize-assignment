from decimal import Decimal
from datetime import date
from typing import List, Optional

from src.services.discount_service import DiscountService
from src.models.product import Product, BrandTier
from src.models.cart import CartItem
from src.models.customer import CustomerProfile
from src.models.payment import PaymentInfo
from src.discount_types.base_discount import BaseDiscount

# Example: Create a custom loyalty discount
class LoyaltyDiscount(BaseDiscount):
    """Custom loyalty points discount implementation"""
    
    def __init__(self, points_threshold: int, discount_percentage: Decimal):
        super().__init__(
            discount_id="LOYALTY_POINTS",
            discount_name="Loyalty Points Discount"
        )
        self.points_threshold = points_threshold
        self.discount_percentage = discount_percentage
    
    async def calculate_discount(
        self, 
        cart_items: List[CartItem], 
        customer: CustomerProfile,
        payment_info: Optional[PaymentInfo] = None,
        **kwargs
    ) -> Decimal:
        if not await self.is_applicable(cart_items, customer, payment_info, **kwargs):
            return Decimal("0")
        
        cart_total = self.calculate_cart_total(cart_items)
        return cart_total * (self.discount_percentage / Decimal("100"))
    
    async def is_applicable(
        self, 
        cart_items: List[CartItem], 
        customer: CustomerProfile,
        payment_info: Optional[PaymentInfo] = None,
        **kwargs
    ) -> bool:
        return customer.loyalty_points >= self.points_threshold