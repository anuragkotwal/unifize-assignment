from decimal import Decimal
from src.models.product import Product
from src.models.cart import CartItem
from src.models.discount import DiscountedPrice
from src.models.customer import CustomerProfile
from src.models import BrandTier

# Dummy data creation for testing multiple discount scenarios

# Create a sample customer profile
customer_profile = CustomerProfile(
    id="customer_1",
    name="John Doe",
    email="john.doe@example.com",
    tier=BrandTier.REGULAR
)

# Create a sample product (PUMA T-shirt)
puma_tshirt = Product(
    id="product_1",
    brand="PUMA",
    brand_tier=BrandTier.PREMIUM,
    category="T-shirts",
    base_price=Decimal("100.00"),
    current_price=Decimal("60.00")  # After applying brand discount
)

# Create a cart item for the PUMA T-shirt
cart_item = CartItem(
    product=puma_tshirt,
    quantity=1,
    size="M"
)

# Create a list of cart items
cart_items = [cart_item]

# Expected discounted price after applying all discounts
expected_discounted_price = DiscountedPrice(
    original_price=Decimal("100.00"),
    final_price=Decimal("50.00"),  # After applying all discounts
    applied_discounts={
        "Brand Discount": Decimal("40.00"),
        "Category Discount": Decimal("10.00"),
        "Bank Offer": Decimal("10.00")
    },
    message="Discounts applied successfully."
)