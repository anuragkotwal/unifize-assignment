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
        # Example validation logic
        if code.startswith("SUPER"):
            return True  # Assume all SUPER codes are valid
        
        # Add more validation rules based on brand exclusions, category restrictions, etc.
        return False

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