from typing import List, Optional, Dict
from decimal import Decimal

from src.models.cart import CartItem
from src.models.customer import CustomerProfile
from src.models.discount import DiscountedPrice
from src.discount_types.brand_discount import BrandDiscount
from src.discount_types.category_discount import CategoryDiscount
from src.discount_types.bank_discount import BankDiscount
from src.discount_types.voucher_discount import VoucherDiscount
from src.discount_types.discount_factory import DiscountFactory
from src.discount_types.tier_discount import TierDiscount
from src.discount_types.seasonal_discount import SeasonalDiscount
from src.models.payment import PaymentInfo
from src.services.validation_service import ValidationService

class DiscountService:
    def __init__(self):
        self.validation_service = ValidationService()
        self.discount_factory = DiscountFactory()
        self._register_custom_discounts()
        
        # Define available discount codes with their properties
        self.discount_codes = {
            "SUPER69": {
                "discount_percentage": Decimal("69"),
                "max_discount": Decimal("1000"),
                "tier_requirement": None,
                "excluded_brands": [],
                "allowed_categories": [],
                "min_cart_value": Decimal("0")
            },
            "PREMIUM20": {
                "discount_percentage": Decimal("20"),
                "max_discount": Decimal("500"),
                "tier_requirement": "premium",
                "excluded_brands": [],
                "allowed_categories": [],
                "min_cart_value": Decimal("1000")
            },
            "NEWUSER15": {
                "discount_percentage": Decimal("15"),
                "max_discount": Decimal("300"),
                "tier_requirement": None,
                "excluded_brands": [],
                "allowed_categories": [],
                "min_cart_value": Decimal("500")
            },
            "BRAND_EXCLUSION": {
                "discount_percentage": Decimal("10"),
                "max_discount": Decimal("200"),
                "tier_requirement": None,
                "excluded_brands": ["PUMA", "NIKE"],
                "allowed_categories": [],
                "min_cart_value": Decimal("0")
            },
            "CATEGORY_RESTRICTION": {
                "discount_percentage": Decimal("25"),
                "max_discount": Decimal("600"),
                "tier_requirement": None,
                "excluded_brands": [],
                "allowed_categories": ["Shoes", "Jackets"],
                "min_cart_value": Decimal("0")
            },
            "TIER_DISCOUNT": {
                "discount_percentage": Decimal("30"),
                "max_discount": Decimal("800"),
                "tier_requirement": "regular",
                "excluded_brands": [],
                "allowed_categories": [],
                "min_cart_value": Decimal("2000")
            }
        }

    def _register_custom_discounts(self):
        """Register custom discount types with the factory"""
        self.discount_factory.register_discount_type("tier", TierDiscount)
        self.discount_factory.register_discount_type("seasonal", SeasonalDiscount)
        self.discount_factory.register_discount_type("brand", BrandDiscount)
    
    def add_discount_type(self, discount_type_name: str, discount_class):
        """
        Public method to add new discount types.
        
        Args:
            discount_type_name: Unique name for the discount type
            discount_class: Class implementing BaseDiscount interface
        """
        self.discount_factory.register_discount_type(discount_type_name, discount_class)
    
    async def calculate_cart_discounts(
        self,
        cart_items: List[CartItem],
        customer: CustomerProfile,
        payment_info: Optional[PaymentInfo] = None,
        voucher_code: Optional[str] = None
    ) -> DiscountedPrice:
        # Initialize with cart total from current prices
        original_price = sum(item.product.current_price * item.quantity for item in cart_items)
        applied_discounts = {}
        
        # Apply brand discounts for premium brands automatically
        premium_brands = ["NIKE", "ADIDAS", "PUMA"]  # Example premium brands
        cart_brands = {item.product.brand for item in cart_items}
        
        for brand in cart_brands:
            if brand in premium_brands:
                brand_discount = BrandDiscount(brand, Decimal("10"), Decimal("200"))
                if await brand_discount.is_applicable(cart_items, customer, payment_info):
                    brand_result = await brand_discount.calculate_discount(cart_items, customer, payment_info)
                    if brand_result > 0:
                        applied_discounts[f"{brand} Brand Discount"] = brand_result
        
        # Apply bank discount if payment info provided
        if payment_info:
            bank_discount = BankDiscount(payment_info.bank_name, 10.0)  # Example: 10% discount
            bank_result = await bank_discount.calculate_discount(cart_items, customer)
            if bank_result > 0:
                applied_discounts[f"{payment_info.bank_name} Bank Offer"] = bank_result
        
        # Apply voucher discount if voucher code provided and valid
        if voucher_code:
            is_valid = await self.validate_discount_code(voucher_code, cart_items, customer)
            if is_valid:
                discount_config = self.discount_codes.get(voucher_code, {})
                discount_percentage = float(discount_config.get("discount_percentage", Decimal("15")))
                max_discount_amount = float(discount_config.get("max_discount", Decimal("100")))
                voucher_discount = self.discount_factory.create_discount(
                    "voucher",
                    code=voucher_code,
                    discount_percentage=discount_percentage,
                    max_discount_amount=max_discount_amount
                )
                if await voucher_discount.is_applicable(cart_items, customer, payment_info, voucher_code=voucher_code):
                    voucher_result = await voucher_discount.calculate_discount(cart_items, customer, payment_info, voucher_code=voucher_code)
                    if voucher_result > 0:
                        applied_discounts[f"Voucher {voucher_code}"] = voucher_result
        
        # Calculate final price
        total_discount = sum(applied_discounts.values())
        final_price = max(original_price - total_discount, Decimal('0'))
        
        return DiscountedPrice(
            original_price=original_price,
            final_price=final_price,
            applied_discounts=applied_discounts,
            message="Discounts applied successfully"
        )

    async def apply_advanced_discounts(
        self,
        cart_items: List[CartItem],
        customer: CustomerProfile,
        payment_info: Optional[PaymentInfo] = None,
        discount_configs: Optional[List[Dict]] = None
    ) -> DiscountedPrice:
        """
        Apply multiple discount types using the factory pattern.
        
        Args:
            cart_items: List of cart items
            customer: Customer profile
            payment_info: Optional payment information
            discount_configs: List of discount configurations to apply
            
        Returns:
            DiscountedPrice with all applicable discounts applied
        """
        original_price = sum(item.product.current_price * item.quantity for item in cart_items)
        applied_discounts = {}
        
        if discount_configs:
            # Create discount instances from configurations
            discounts = []
            for config in discount_configs:
                discount_type = config.pop("type")
                discount = self.discount_factory.create_discount(discount_type, **config)
                discounts.append(discount)
            
            # Apply all configured discounts
            discount_results = await self.discount_factory.apply_multiple_discounts(
                discounts, cart_items, customer, payment_info
            )
            applied_discounts.update(discount_results)
        
        # Calculate final price
        total_discount = sum(applied_discounts.values())
        final_price = max(original_price - total_discount, Decimal('0'))
        
        return DiscountedPrice(
            original_price=original_price,
            final_price=final_price,
            applied_discounts=applied_discounts,
            message="Advanced discounts applied successfully"
        )

    async def validate_discount_code(
        self,
        code: str,
        cart_items: List[CartItem],
        customer: CustomerProfile
    ) -> bool:
        """
        Validate if a discount code can be applied to the current cart and customer.
        
        Args:
            code: The discount code to validate
            cart_items: List of items in the cart
            customer: Customer profile
            
        Returns:
            bool: True if the discount code is valid and can be applied, False otherwise
        """
        # Check if code exists in our system
        if code not in self.discount_codes:
            return False
        
        discount_config = self.discount_codes[code]
        
        # Use ValidationService for basic validation
        if not self.validation_service.validate_discount_code(code, cart_items, customer):
            return False
                
        # Additional validation checks
        
        # 1. Check customer tier requirement
        if discount_config["tier_requirement"]:
            if not self._check_customer_tier(customer, discount_config["tier_requirement"]):
                return False
        
        # 2. Check brand exclusions
        if discount_config["excluded_brands"]:
            if self._check_excluded_brands(cart_items, discount_config["excluded_brands"]):
                return False
        
        # 3. Check category restrictions (if specified, cart must contain allowed categories)
        if discount_config["allowed_categories"]:
            if not self._check_allowed_categories(cart_items, discount_config["allowed_categories"]):
                return False
        
        # 4. Check minimum cart value
        cart_value = sum(item.product.current_price * item.quantity for item in cart_items)
        if cart_value < discount_config["min_cart_value"]:
            return False
        
        return True
    
    def _check_customer_tier(self, customer: CustomerProfile, required_tier: str) -> bool:
        """Check if customer meets the tier requirement"""
        # Define tier hierarchy
        tier_hierarchy = {
            "budget": 1,
            "regular": 2, 
            "premium": 3,
            "gold": 4,
            "platinum": 5
        }
        
        customer_tier_level = tier_hierarchy.get(customer.tier.lower(), 0)
        required_tier_level = tier_hierarchy.get(required_tier.lower(), 0)
        
        return customer_tier_level >= required_tier_level
    
    def _check_excluded_brands(self, cart_items: List[CartItem], excluded_brands: List[str]) -> bool:
        """Check if cart contains any excluded brands"""
        cart_brands = {item.product.brand for item in cart_items}
        return bool(cart_brands.intersection(excluded_brands))
    
    def _check_allowed_categories(self, cart_items: List[CartItem], allowed_categories: List[str]) -> bool:
        """Check if cart contains at least one item from allowed categories"""
        cart_categories = {item.product.category for item in cart_items}
        return bool(cart_categories.intersection(allowed_categories))