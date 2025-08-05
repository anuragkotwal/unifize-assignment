from decimal import Decimal
from src.models.product import Product, BrandTier
from src.models.cart import CartItem
from src.models.customer import CustomerProfile
from src.models.payment import PaymentInfo
from src.models.discount import DiscountedPrice


class TestProduct:
    """Test suite for Product model"""

    def test_product_creation(self):
        """Test Product model creation"""
        product = Product(
            id="TEST001",
            brand="NIKE",
            brand_tier=BrandTier.PREMIUM,
            category="Shoes",
            base_price=Decimal('5000'),
            current_price=Decimal('4500')
        )

        assert product.id == "TEST001"
        assert product.brand == "NIKE"
        assert product.brand_tier == BrandTier.PREMIUM
        assert product.category == "Shoes"
        assert product.base_price == Decimal('5000')
        assert product.current_price == Decimal('4500')

    def test_product_with_equal_prices(self):
        """Test Product with base price equal to current price"""
        product = Product(
            id="TEST002",
            brand="PUMA",
            brand_tier=BrandTier.REGULAR,
            category="T-shirts",
            base_price=Decimal('1000'),
            current_price=Decimal('1000')
        )

        assert product.base_price == product.current_price

    def test_brand_tier_enum(self):
        """Test BrandTier enum values"""
        assert BrandTier.PREMIUM.value == "premium"
        assert BrandTier.REGULAR.value == "regular"


class TestCartItem:
    """Test suite for CartItem model"""

    def test_cart_item_creation(self):
        """Test CartItem model creation"""
        product = Product(
            id="TEST001",
            brand="NIKE",
            brand_tier=BrandTier.PREMIUM,
            category="Shoes",
            base_price=Decimal('5000'),
            current_price=Decimal('4500')
        )

        cart_item = CartItem(
            product=product,
            quantity=2,
            size="9",
            price=product.current_price
        )

        assert cart_item.product == product
        assert cart_item.quantity == 2
        assert cart_item.size == "9"
        assert cart_item.price == Decimal('4500')

    def test_cart_item_total_calculation(self):
        """Test cart item total price calculation"""
        product = Product(
            id="TEST001",
            brand="PUMA",
            brand_tier=BrandTier.REGULAR,
            category="T-shirts",
            base_price=Decimal('1000'),
            current_price=Decimal('800')
        )

        cart_item = CartItem(
            product=product,
            quantity=3,
            size="L",
            price=product.current_price
        )

        # Calculate total manually
        expected_total = cart_item.price * cart_item.quantity
        assert expected_total == Decimal('2400')


class TestCustomerProfile:
    """Test suite for CustomerProfile model"""

    def test_customer_profile_creation(self):
        """Test CustomerProfile model creation"""
        customer = CustomerProfile(
            id="CUST001",
            name="John Doe",
            email="john.doe@example.com",
            tier="premium",
            loyalty_points=1500
        )

        assert customer.id == "CUST001"
        assert customer.name == "John Doe"
        assert customer.email == "john.doe@example.com"
        assert customer.tier == "premium"
        assert customer.loyalty_points == 1500

    def test_customer_profile_with_optional_fields(self):
        """Test CustomerProfile with minimal required fields"""
        customer = CustomerProfile(
            id="CUST002",
            name="Jane Smith",
            email="jane@example.com",
            tier="regular",
            loyalty_points=0
        )

        assert customer.id == "CUST002"
        assert customer.name == "Jane Smith"
        assert customer.email == "jane@example.com"
        # Optional fields should have default values or be None
        assert hasattr(customer, 'tier')
        assert hasattr(customer, 'loyalty_points')

    def test_different_customer_tiers(self):
        """Test different customer tier values"""
        tiers = ["premium", "gold", "silver"]
        
        for tier in tiers:
            customer = CustomerProfile(
                id=f"CUST_{tier.upper()}",
                name=f"Test {tier.title()}",
                email=f"test.{tier}@example.com",
                tier=tier,
                loyalty_points=1000
            )
            
            assert customer.tier == tier


class TestPaymentInfo:
    """Test suite for PaymentInfo model"""

    def test_payment_info_creation(self):
        """Test PaymentInfo model creation"""
        payment = PaymentInfo(
            method="CARD",
            bank_name="ICICI",
            card_type="CREDIT"
        )

        assert payment.method == "CARD"
        assert payment.bank_name == "ICICI"
        assert payment.card_type == "CREDIT"

    def test_different_payment_methods(self):
        """Test different payment method types"""
        methods = ["CARD", "UPI", "NETBANKING", "WALLET"]
        
        for method in methods:
            payment = PaymentInfo(
                method=method,
                bank_name="HDFC" if method == "CARD" else None,
                card_type="DEBIT" if method == "CARD" else None
            )
            
            assert payment.method == method

    def test_different_banks(self):
        """Test different bank names"""
        banks = ["ICICI", "HDFC", "SBI", "AXIS", "KOTAK"]
        
        for bank in banks:
            payment = PaymentInfo(
                method="CARD",
                bank_name=bank,
                card_type="CREDIT"
            )
            
            assert payment.bank_name == bank

    def test_different_card_types(self):
        """Test different card types"""
        card_types = ["CREDIT", "DEBIT"]
        
        for card_type in card_types:
            payment = PaymentInfo(
                method="CARD",
                bank_name="ICICI",
                card_type=card_type
            )
            
            assert payment.card_type == card_type


class TestDiscountedPrice:
    """Test suite for DiscountedPrice model"""

    def test_discounted_price_creation(self):
        """Test DiscountedPrice model creation"""
        applied_discounts = {
            "Brand Discount": Decimal('500'),
            "Bank Offer": Decimal('200'),
            "Voucher SUPER69": Decimal('300')
        }

        discounted_price = DiscountedPrice(
            original_price=Decimal('8000'),
            final_price=Decimal('7000'),
            applied_discounts=applied_discounts,
            message="Discounts applied successfully"
        )

        assert discounted_price.original_price == Decimal('8000')
        assert discounted_price.final_price == Decimal('7000')
        assert discounted_price.applied_discounts == applied_discounts
        assert discounted_price.message == "Discounts applied successfully"

    def test_discounted_price_no_discounts(self):
        """Test DiscountedPrice with no discounts applied"""
        discounted_price = DiscountedPrice(
            original_price=Decimal('5000'),
            final_price=Decimal('5000'),
            applied_discounts={},
            message="No discounts applicable"
        )

        assert discounted_price.original_price == discounted_price.final_price
        assert len(discounted_price.applied_discounts) == 0

    def test_discounted_price_calculations(self):
        """Test discount calculations"""
        applied_discounts = {
            "PUMA Brand Discount": Decimal('400'),  # 40% of 1000
            "NIKE Brand Discount": Decimal('1750'), # 35% of 5000
            "ICICI Bank Offer": Decimal('500')      # Bank offer
        }

        original_price = Decimal('8000')
        total_discount = sum(applied_discounts.values())
        final_price = original_price - total_discount

        discounted_price = DiscountedPrice(
            original_price=original_price,
            final_price=final_price,
            applied_discounts=applied_discounts,
            message="Multiple discounts applied"
        )

        # Verify total savings
        actual_savings = discounted_price.original_price - discounted_price.final_price
        expected_savings = sum(applied_discounts.values())
        assert actual_savings == expected_savings

    def test_decimal_precision_in_discounted_price(self):
        """Test that all price fields maintain Decimal precision"""
        applied_discounts = {
            "Test Discount": Decimal('123.45')
        }

        discounted_price = DiscountedPrice(
            original_price=Decimal('1000.00'),
            final_price=Decimal('876.55'),
            applied_discounts=applied_discounts,
            message="Precision test"
        )

        # Check that all numeric fields are Decimal type
        assert isinstance(discounted_price.original_price, Decimal)
        assert isinstance(discounted_price.final_price, Decimal)
        
        for discount_amount in discounted_price.applied_discounts.values():
            assert isinstance(discount_amount, Decimal)


class TestModelIntegration:
    """Test suite for model integration scenarios"""

    def test_complete_shopping_scenario(self):
        """Test a complete shopping scenario with all models"""
        # Create products
        products = [
            Product(
                id="PUMA001",
                brand="PUMA",
                brand_tier=BrandTier.REGULAR,
                category="T-shirts",
                base_price=Decimal('1000'),
                current_price=Decimal('1000')
            ),
            Product(
                id="NIKE001",
                brand="NIKE",
                brand_tier=BrandTier.PREMIUM,
                category="Shoes",
                base_price=Decimal('5000'),
                current_price=Decimal('5000')
            )
        ]

        # Create cart items
        cart_items = [
            CartItem(product=products[0], quantity=2, size="M", price=products[0].current_price),
            CartItem(product=products[1], quantity=1, size="9", price=products[1].current_price)
        ]

        # Create customer
        customer = CustomerProfile(
            id="CUST001",
            name="John Doe",
            email="john@example.com",
            tier="premium",
            loyalty_points=1500
        )

        # Create payment info
        payment = PaymentInfo(
            method="CARD",
            bank_name="ICICI",
            card_type="CREDIT"
        )

        # Create discount result
        applied_discounts = {
            "PUMA Brand Discount": Decimal('800'),    # 40% of 2000
            "NIKE Brand Discount": Decimal('1750'),  # 35% of 5000
            "ICICI Bank Offer": Decimal('500')       # Bank offer
        }

        original_price = sum(item.price * item.quantity for item in cart_items)
        final_price = original_price - sum(applied_discounts.values())

        result = DiscountedPrice(
            original_price=original_price,
            final_price=final_price,
            applied_discounts=applied_discounts,
            message="Multiple discounts applied successfully"
        )

        # Verify the integration
        assert original_price == Decimal('7000')  # 2*1000 + 1*5000
        assert len(applied_discounts) == 3
        assert result.final_price == Decimal('3950')  # 7000 - 3050
        assert customer.tier == "premium"
        assert payment.bank_name == "ICICI"

    def test_empty_cart_scenario(self):
        """Test scenario with empty cart"""
        cart_items = []
        customer = CustomerProfile(
            id="CUST002",
            name="Empty Cart Customer",
            email="empty@example.com",
            tier="regular",
            loyalty_points=0
        )

        original_price = sum(item.price * item.quantity for item in cart_items)
        
        result = DiscountedPrice(
            original_price=original_price,
            final_price=original_price,
            applied_discounts={},
            message="No items in cart"
        )

        assert result.original_price == Decimal('0')
        assert result.final_price == Decimal('0')
        assert len(result.applied_discounts) == 0
        assert customer.id == "CUST002"  # Use customer to avoid unused variable warning