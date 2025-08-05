from decimal import Decimal
from typing import List, Optional
from src.discount_types.base_discount import BaseDiscount
from src.models.cart import CartItem
from src.models.customer import CustomerProfile
from src.models.payment import PaymentInfo

class BrandDiscount(BaseDiscount):
    """
    Brand-specific discount implementation.
    Applies discounts to products from specific brands.
    """
    
    def __init__(self, brand: str, discount_percentage: Decimal, max_discount: Optional[Decimal] = None):
        super().__init__(
            discount_id=f"BRAND_{brand.upper()}",
            discount_name=f"{brand} Brand Discount"
        )
        self.brand = brand
        self.discount_percentage = discount_percentage
        self.max_discount = max_discount

    async def calculate_discount(
        self, 
        cart_items: List[CartItem], 
        customer: CustomerProfile,
        payment_info: Optional[PaymentInfo] = None,
        **kwargs
    ) -> Decimal:
        """Calculate brand-specific discount amount"""
        if not await self.is_applicable(cart_items, customer, payment_info, **kwargs):
            return Decimal("0")
        
        # Calculate discount only for items from the specific brand
        brand_items_total = sum(
            item.product.current_price * item.quantity
            for item in cart_items
            if item.product.brand.upper() == self.brand.upper()
        )
        
        discount_amount = brand_items_total * (self.discount_percentage / Decimal("100"))
        
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
        """Check if cart contains items from the specific brand"""
        cart_brands = self.get_cart_brands(cart_items)
        return self.brand.upper() in {brand.upper() for brand in cart_brands}

    def apply_discount(self, product) -> Decimal:
        """Legacy method for backward compatibility"""
        if product.brand.upper() == self.brand.upper():
            discount_amount = product.base_price * (self.discount_percentage / Decimal(100))
            return discount_amount
        return Decimal(0)

# Legacy function for backward compatibility
def calculate_brand_discounts(cart_items: List, brand_discounts: List[BrandDiscount]):
    """Legacy function - use DiscountFactory.apply_multiple_discounts instead"""
    from src.models.discount import DiscountedPrice
    
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