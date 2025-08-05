from typing import Dict, Type, List, Optional
from decimal import Decimal
from src.discount_types.base_discount import BaseDiscount
from src.models.cart import CartItem
from src.models.customer import CustomerProfile
from src.models.payment import PaymentInfo

class DiscountFactory:
    """
    Factory class for creating and managing different discount types.
    Provides a clean interface for adding new discount types to the system.
    """
    
    def __init__(self):
        self._discount_types: Dict[str, Type[BaseDiscount]] = {}
        self._register_default_discounts()
    
    def _register_default_discounts(self):
        """Register the default discount types"""
        from src.discount_types.brand_discount import BrandDiscount
        from src.discount_types.voucher_discount import VoucherDiscount
        from src.discount_types.bank_discount import BankDiscount
        from src.discount_types.tier_discount import TierDiscount
        from src.discount_types.category_discount import CategoryDiscount
        from src.discount_types.loyalty_discount import LoyaltyDiscount
        from src.discount_types.seasonal_discount import SeasonalDiscount
        
        # Register all discount types
        self._discount_types["brand"] = BrandDiscount
        self._discount_types["voucher"] = VoucherDiscount
        self._discount_types["bank"] = BankDiscount
        self._discount_types["tier"] = TierDiscount
        self._discount_types["category"] = CategoryDiscount
        self._discount_types["loyalty"] = LoyaltyDiscount
        self._discount_types["seasonal"] = SeasonalDiscount
    
    def register_discount_type(self, discount_type: str, discount_class: Type[BaseDiscount]):
        """
        Register a new discount type.
        
        Args:
            discount_type: Unique identifier for the discount type
            discount_class: Class that implements BaseDiscount interface
        """
        if not issubclass(discount_class, BaseDiscount):
            raise ValueError(f"Discount class must inherit from BaseDiscount")
        
        self._discount_types[discount_type] = discount_class
    
    def create_discount(self, discount_type: str, **kwargs) -> BaseDiscount:
        """
        Create a discount instance of the specified type.
        
        Args:
            discount_type: Type of discount to create
            **kwargs: Parameters to pass to the discount constructor
            
        Returns:
            BaseDiscount: Instance of the requested discount type
        """
        if discount_type not in self._discount_types:
            raise ValueError(f"Unknown discount type: {discount_type}")
        
        discount_class = self._discount_types[discount_type]
        return discount_class(**kwargs)
    
    def get_available_discount_types(self) -> List[str]:
        """
        Get list of all registered discount types.
        
        Returns:
            List of discount type identifiers
        """
        return list(self._discount_types.keys())
    
    async def apply_multiple_discounts(
        self,
        discounts: List[BaseDiscount],
        cart_items: List[CartItem],
        customer: CustomerProfile,
        payment_info: Optional[PaymentInfo] = None
    ) -> Dict[str, Decimal]:
        """
        Apply multiple discounts and return the results.
        
        Args:
            discounts: List of discount instances to apply
            cart_items: List of cart items
            customer: Customer profile
            payment_info: Optional payment information
            
        Returns:
            Dict mapping discount names to discount amounts
        """
        applied_discounts = {}
        
        for discount in discounts:
            if await discount.is_applicable(cart_items, customer, payment_info):
                discount_amount = await discount.calculate_discount(
                    cart_items, customer, payment_info
                )
                if discount_amount > 0:
                    applied_discounts[discount.discount_name] = discount_amount
                
        return applied_discounts