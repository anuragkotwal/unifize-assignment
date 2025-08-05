from src.models.product import Product
from src.models.cart import CartItem
from src.models.customer import CustomerProfile
from src.services.validation_service import ValidationService
from decimal import Decimal
import pytest

@pytest.fixture
def setup_data():
    # Create dummy products and cart items for testing
    product1 = Product(
        id="1",
        brand="PUMA",
        brand_tier="premium",
        category="T-shirts",
        base_price=Decimal("100.00"),
        current_price=Decimal("60.00")  # After brand discount
    )
    
    cart_item1 = CartItem(product=product1, quantity=1, size="M")
    
    customer = CustomerProfile(
        id="cust1",
        tier="regular"
    )
    
    return cart_item1, customer

def test_validate_discount_code_valid(setup_data):
    cart_item, customer = setup_data
    validation_service = ValidationService()
    
    valid_code = "SUPER69"
    result = validation_service.validate_discount_code(valid_code, [cart_item], customer)
    
    assert result is True

def test_validate_discount_code_invalid(setup_data):
    cart_item, customer = setup_data
    validation_service = ValidationService()
    
    invalid_code = "INVALIDCODE"
    result = validation_service.validate_discount_code(invalid_code, [cart_item], customer)
    
    assert result is False

def test_validate_discount_code_exclusions(setup_data):
    cart_item, customer = setup_data
    validation_service = ValidationService()
    
    excluded_code = "BRAND_EXCLUSION"
    result = validation_service.validate_discount_code(excluded_code, [cart_item], customer)
    
    assert result is False

def test_validate_discount_code_category_restriction(setup_data):
    cart_item, customer = setup_data
    validation_service = ValidationService()
    
    restricted_code = "CATEGORY_RESTRICTION"
    result = validation_service.validate_discount_code(restricted_code, [cart_item], customer)
    
    assert result is False

def test_validate_discount_code_tier_requirement(setup_data):
    cart_item, customer = setup_data
    validation_service = ValidationService()
    
    tier_code = "TIER_DISCOUNT"
    result = validation_service.validate_discount_code(tier_code, [cart_item], customer)
    
    assert result is True  # Assuming the customer meets the tier requirement