from decimal import Decimal
from typing import List, Optional
from datetime import datetime, date
from src.discount_types.base_discount import BaseDiscount
from src.models.cart import CartItem
from src.models.customer import CustomerProfile
from src.models.payment import PaymentInfo

class SeasonalDiscount(BaseDiscount):
    """
    Example seasonal discount implementation.
    Shows how to create time-based discounts using the BaseDiscount interface.
    """
    
    def __init__(
        self,
        season_name: str,
        start_date: date,
        end_date: date,
        discount_percentage: Decimal,
        applicable_categories: Optional[List[str]] = None,
        max_discount: Optional[Decimal] = None
    ):
        super().__init__(
            discount_id=f"SEASONAL_{season_name.upper()}",
            discount_name=f"{season_name} Seasonal Discount"
        )
        self.season_name = season_name
        self.start_date = start_date
        self.end_date = end_date
        self.discount_percentage = discount_percentage
        self.applicable_categories = applicable_categories or []
        self.max_discount = max_discount
    
    async def calculate_discount(
        self, 
        cart_items: List[CartItem], 
        customer: CustomerProfile,
        payment_info: Optional[PaymentInfo] = None,
        **kwargs
    ) -> Decimal:
        """Calculate seasonal discount amount"""
        if not await self.is_applicable(cart_items, customer, payment_info, **kwargs):
            return Decimal("0")
        
        # Calculate discount only for applicable categories (if specified)
        if self.applicable_categories:
            applicable_total = sum(
                item.product.current_price * item.quantity
                for item in cart_items
                if item.product.category in self.applicable_categories
            )
        else:
            applicable_total = self.calculate_cart_total(cart_items)
        
        discount_amount = applicable_total * (self.discount_percentage / Decimal("100"))
        
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
        """Check if seasonal discount is currently active"""
        current_date = datetime.now().date()
        
        # Check if we're within the discount period
        if not (self.start_date <= current_date <= self.end_date):
            return False
        
        # Check if cart has applicable categories (if specified)
        if self.applicable_categories:
            cart_categories = self.get_cart_categories(cart_items)
            if not cart_categories.intersection(self.applicable_categories):
                return False
        
        return True