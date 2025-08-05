from decimal import Decimal
import pytest
from src.models.product import Product
from src.models.cart import CartItem
from src.models.discount import DiscountedPrice
from src.services.discount_service import DiscountService
from src.models.customer import CustomerProfile
from src.models.payment import PaymentInfo

@pytest.fixture
def setup_data():
    product = Product(
        id="1",
        brand="PUMA",
        brand_tier="premium",
        category="T-shirt",
        base_price=Decimal("100.00"),
        current_price=Decimal("60.00")  # After brand discount
    )
    cart_item = CartItem(product=product, quantity=1, size="M")
    customer = CustomerProfile(tier="regular")
    payment_info = PaymentInfo(method="CARD", bank_name="ICICI", card_type="CREDIT")
    
    return cart_item, customer, payment_info

@pytest.mark.asyncio
async def test_calculate_cart_discounts(setup_data):
    cart_item, customer, payment_info = setup_data
    discount_service = DiscountService()

    discounted_price = await discount_service.calculate_cart_discounts(
        cart_items=[cart_item],
        customer=customer,
        payment_info=payment_info
    )

    assert discounted_price.original_price == Decimal("100.00")
    assert discounted_price.final_price < discounted_price.original_price
    assert "Min 40% off on PUMA" in discounted_price.applied_discounts
    assert "Extra 10% off on T-shirts" in discounted_price.applied_discounts
    assert "10% instant discount on ICICI Bank cards" in discounted_price.applied_discounts
    assert discounted_price.message == "Discounts applied successfully."

@pytest.mark.asyncio
async def test_validate_discount_code(setup_data):
    cart_item, customer, _ = setup_data
    discount_service = DiscountService()

    valid_code = "SUPER69"
    is_valid = await discount_service.validate_discount_code(valid_code, [cart_item], customer)

    assert is_valid is True

    invalid_code = "INVALIDCODE"
    is_valid = await discount_service.validate_discount_code(invalid_code, [cart_item], customer)

    assert is_valid is False