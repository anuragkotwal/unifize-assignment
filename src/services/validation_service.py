from typing import List
from src.models.cart import CartItem
from src.models.customer import CustomerProfile

class ValidationService:
    @staticmethod
    def validate_discount_code(
        code: str,
        cart_items: List[CartItem],
        customer: CustomerProfile
    ) -> bool:
        # Define discount codes and their rules
        discount_codes = {
            "SUPER69": {
                "tier_requirement": None,
                "excluded_brands": [],
                "allowed_categories": [],
                "min_cart_value": 0
            },
            "PREMIUM20": {
                "tier_requirement": "premium",
                "excluded_brands": [],
                "allowed_categories": [],
                "min_cart_value": 1000
            },
            "NEWUSER15": {
                "tier_requirement": None,
                "excluded_brands": [],
                "allowed_categories": [],
                "min_cart_value": 500
            },
            "BRAND_EXCLUSION": {
                "tier_requirement": None,
                "excluded_brands": ["PUMA", "NIKE"],
                "allowed_categories": [],
                "min_cart_value": 0
            },
            "CATEGORY_RESTRICTION": {
                "tier_requirement": None,
                "excluded_brands": [],
                "allowed_categories": ["Shoes", "Jackets"],
                "min_cart_value": 0
            },
            "TIER_DISCOUNT": {
                "tier_requirement": "regular",
                "excluded_brands": [],
                "allowed_categories": [],
                "min_cart_value": 2000
            }
        }
        
        # Check if code exists
        if code not in discount_codes:
            return False
        
        code_rules = discount_codes[code]
        
        # Check minimum cart value
        total_cart_value = sum(item.price * item.quantity for item in cart_items)
        if total_cart_value < code_rules["min_cart_value"]:
            return False
        
        # Check customer tier requirements
        if not ValidationService.check_customer_tier_requirements(code, customer):
            return False
        
        # Check brand exclusions
        if not ValidationService.check_brand_exclusions(code, cart_items):
            return False
        
        # Check category restrictions
        if not ValidationService.check_category_restrictions(code, cart_items):
            return False
        
        return True

    @staticmethod
    def check_brand_exclusions(code: str, cart_items: List[CartItem]) -> bool:
        # Implement logic to check for brand exclusions
        return True

    @staticmethod
    def check_category_restrictions(code: str, cart_items: List[CartItem]) -> bool:
        # Implement logic to check for category restrictions
        return True

    @staticmethod
    def check_customer_tier_requirements(code: str, customer: CustomerProfile) -> bool:
        # Implement logic to check for customer tier requirements
        return True