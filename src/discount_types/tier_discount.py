from decimal import Decimal
from typing import List, Optional
from src.discount_types.base_discount import BaseDiscount
from src.models.cart import CartItem
from src.models.customer import CustomerProfile
from src.models.payment import PaymentInfo

class TierDiscount(BaseDiscount):
    """
    Example implementation of a tier-based discount.
    Demonstrates how to implement the BaseDiscount interface.
    """
    
    def __init__(
        self, 
        required_tier: str, 
        discount_percentage: Decimal, 
        max_discount: Optional[Decimal] = None,
        min_cart_value: Optional[Decimal] = None
    ):
        super().__init__(
            discount_id=f"TIER_{required_tier.upper()}",
            discount_name=f"{required_tier.title()} Tier Discount"
        )
        self.required_tier = required_tier.lower()
        self.discount_percentage = discount_percentage
        self.max_discount = max_discount
        self.min_cart_value = min_cart_value or Decimal("0")
    
    async def calculate_discount(
        self, 
        cart_items: List[CartItem], 
        customer: CustomerProfile,
        payment_info: Optional[PaymentInfo] = None,
        **kwargs
    ) -> Decimal:
        """Calculate tier-based discount amount"""
        if not await self.is_applicable(cart_items, customer, payment_info, **kwargs):
            return Decimal("0")
        
        cart_total = self.calculate_cart_total(cart_items)
        discount_amount = cart_total * (self.discount_percentage / Decimal("100"))
        
        # Apply maximum discount limit if specified
        if self.max_discount and discount_amount > self.max_discount:
            discount_amount = self.max_discount
        
        return discount_amount
    
    async def is_applicable(
        self, 
        cart_items: List[CartItem], 
        customer: CustomerProfile,
        payment_info: Optional[PaymentInfo] = None,
        **kwargs
    ) -> bool:
        """Check if customer meets tier requirements"""
        # Check customer tier
        if not self._check_customer_tier(customer):
            return False
        
        # Check minimum cart value
        cart_total = self.calculate_cart_total(cart_items)
        if cart_total < self.min_cart_value:
            return False
        
        return True
    
    def _check_customer_tier(self, customer: CustomerProfile) -> bool:
        """Check if customer meets the tier requirement"""
        tier_hierarchy = {
            "budget": 1,
            "regular": 2,
            "premium": 3,
            "gold": 4,
            "platinum": 5
        }
        
        customer_tier_level = tier_hierarchy.get(customer.tier.lower(), 0)
        required_tier_level = tier_hierarchy.get(self.required_tier, 0)
        
        return customer_tier_level >= required_tier_level