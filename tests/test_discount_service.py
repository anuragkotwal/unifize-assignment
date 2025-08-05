import pytest
import asyncio
from decimal import Decimal
from unittest.mock import Mock, patch

from src.services.discount_service import DiscountService
from src.models.product import Product, BrandTier
from src.models.cart import CartItem
from src.models.customer import CustomerProfile
from src.models.payment import PaymentInfo
from src.models.discount import DiscountedPrice


class TestDiscountService:
    """Test suite for DiscountService class"""

    @pytest.fixture
    def discount_service(self):
        """Create a DiscountService instance for testing"""
        return DiscountService()

    @pytest.fixture
    def sample_products(self):
        """Create sample products for testing"""
        return [
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
            ),
            Product(
                id="ZARA001",
                brand="ZARA",
                brand_tier=BrandTier.REGULAR,
                category="Jeans",
                base_price=Decimal('2000'),
                current_price=Decimal('2000')
            )
        ]

    @pytest.fixture
    def sample_cart_items(self, sample_products):
        """Create sample cart items for testing"""
        return [
            CartItem(product=sample_products[0], quantity=1, size="M", price=sample_products[0].base_price),
            CartItem(product=sample_products[1], quantity=1, size="9", price=sample_products[1].base_price),
            CartItem(product=sample_products[2], quantity=1, size="32", price=sample_products[2].base_price)
        ]

    @pytest.fixture
    def sample_customer(self):
        """Create a sample customer for testing"""
        return CustomerProfile(
            id="CUST001",
            name="John Doe",
            email="john.doe@example.com",
            tier="premium",
            loyalty_points=1500
        )

    @pytest.fixture
    def sample_payment_info(self):
        """Create sample payment information for testing"""
        return PaymentInfo(
            method="CARD",
            bank_name="ICICI",
            card_type="CREDIT"
        )

    @pytest.mark.asyncio
    async def test_calculate_cart_discounts_with_brand_discounts(
        self, discount_service, sample_cart_items, sample_customer
    ):
        """Test brand discount calculation"""
        result = await discount_service.calculate_cart_discounts(
            cart_items=sample_cart_items,
            customer=sample_customer
        )

        assert isinstance(result, DiscountedPrice)
        print(result)
        assert result.original_price == Decimal('8000')
        assert result.final_price < result.original_price
        assert len(result.applied_discounts) > 0
        assert "Brand Discount" in str(result.applied_discounts)

    @pytest.mark.asyncio
    async def test_calculate_cart_discounts_with_bank_offer(
        self, discount_service, sample_cart_items, sample_customer, sample_payment_info
    ):
        """Test bank offer discount calculation"""
        result = await discount_service.calculate_cart_discounts(
            cart_items=sample_cart_items,
            customer=sample_customer,
            payment_info=sample_payment_info
        )

        assert isinstance(result, DiscountedPrice)
        assert result.original_price == Decimal('8000')
        assert result.final_price < result.original_price
        assert len(result.applied_discounts) > 0
        assert any("Bank Offer" in discount_name for discount_name in result.applied_discounts.keys())

    @pytest.mark.asyncio
    async def test_calculate_cart_discounts_with_voucher_code(
        self, discount_service, sample_cart_items, sample_customer
    ):
        """Test voucher code discount calculation"""
        result = await discount_service.calculate_cart_discounts(
            cart_items=sample_cart_items,
            customer=sample_customer,
            voucher_code="SUPER69"
        )

        assert isinstance(result, DiscountedPrice)
        assert result.original_price == Decimal('8000')
        assert result.final_price < result.original_price
        assert len(result.applied_discounts) > 0
        assert any("Voucher" in discount_name for discount_name in result.applied_discounts.keys())

    @pytest.mark.asyncio
    async def test_calculate_cart_discounts_with_all_discounts(
        self, discount_service, sample_cart_items, sample_customer, sample_payment_info
    ):
        """Test combination of all discount types"""
        result = await discount_service.calculate_cart_discounts(
            cart_items=sample_cart_items,
            customer=sample_customer,
            payment_info=sample_payment_info,
            voucher_code="SUPER69"
        )

        assert isinstance(result, DiscountedPrice)
        assert result.original_price == Decimal('8000')
        assert result.final_price < result.original_price
        assert len(result.applied_discounts) >= 2  # At least brand + bank/voucher

    @pytest.mark.asyncio
    async def test_apply_advanced_discounts(
        self, discount_service, sample_cart_items, sample_customer
    ):
        """Test advanced discount configurations"""
        discount_configs = [
            {
                "type": "brand",
                "brand": "NIKE",
                "discount_percentage": Decimal("25"),
                "max_discount": Decimal("1000")
            },
            {
                "type": "tier",
                "required_tier": "premium",
                "discount_percentage": Decimal("15"),
                "max_discount": Decimal("500")
            }
        ]

        result = await discount_service.apply_advanced_discounts(
            cart_items=sample_cart_items,
            customer=sample_customer,
            discount_configs=discount_configs
        )

        assert isinstance(result, DiscountedPrice)
        assert result.original_price == Decimal('8000')
        assert result.final_price < result.original_price
        assert len(result.applied_discounts) > 0

    @pytest.mark.asyncio
    async def test_validate_discount_code_valid(
        self, discount_service, sample_cart_items, sample_customer
    ):
        """Test validation of valid discount codes"""
        valid_codes = ["SUPER69", "PREMIUM20", "NEWUSER15"]
        
        for code in valid_codes:
            is_valid = await discount_service.validate_discount_code(
                code, sample_cart_items, sample_customer
            )
            assert isinstance(is_valid, bool)

    @pytest.mark.asyncio
    async def test_validate_discount_code_invalid(
        self, discount_service, sample_cart_items, sample_customer
    ):
        """Test validation of invalid discount codes"""
        invalid_codes = ["INVALID123", "EXPIRED", "NOTFOUND"]
        
        for code in invalid_codes:
            is_valid = await discount_service.validate_discount_code(
                code, sample_cart_items, sample_customer
            )
            assert is_valid is False

    @pytest.mark.asyncio
    async def test_empty_cart(self, discount_service, sample_customer):
        """Test behavior with empty cart"""
        empty_cart = []
        
        result = await discount_service.calculate_cart_discounts(
            cart_items=empty_cart,
            customer=sample_customer
        )

        assert isinstance(result, DiscountedPrice)
        assert result.original_price == Decimal('0')
        assert result.final_price == Decimal('0')
        assert len(result.applied_discounts) == 0

    @pytest.mark.asyncio
    async def test_single_item_cart(self, discount_service, sample_products, sample_customer):
        """Test behavior with single item cart"""
        single_item_cart = [
            CartItem(product=sample_products[0], quantity=1, size="M", price=sample_products[0].base_price)
        ]
        
        result = await discount_service.calculate_cart_discounts(
            cart_items=single_item_cart,
            customer=sample_customer
        )

        assert isinstance(result, DiscountedPrice)
        assert result.original_price == Decimal('1000')
        assert result.final_price <= result.original_price

    @pytest.mark.asyncio
    async def test_different_bank_offers(
        self, discount_service, sample_cart_items, sample_customer
    ):
        """Test different bank offers"""
        banks = ["ICICI", "HDFC", "SBI", "AXIS"]
        
        for bank in banks:
            payment_info = PaymentInfo(
                method="CARD",
                bank_name=bank,
                card_type="CREDIT"
            )
            
            result = await discount_service.calculate_cart_discounts(
                cart_items=sample_cart_items,
                customer=sample_customer,
                payment_info=payment_info
            )

            assert isinstance(result, DiscountedPrice)
            assert result.original_price == Decimal('8000')

    @pytest.mark.asyncio
    async def test_customer_tier_impact(self, discount_service, sample_cart_items):
        """Test impact of different customer tiers"""
        tiers = ["premium", "gold", "silver"]
        
        for tier in tiers:
            customer = CustomerProfile(
                id=f"CUST_{tier.upper()}",
                name=f"Test {tier.title()}",
                email=f"test.{tier}@example.com",
                tier=tier,
                loyalty_points=1000
            )
            
            result = await discount_service.calculate_cart_discounts(
                cart_items=sample_cart_items,
                customer=customer
            )

            assert isinstance(result, DiscountedPrice)
            assert result.original_price == Decimal('8000')

    @pytest.mark.asyncio
    async def test_discount_factory_integration(self, discount_service):
        """Test discount factory integration"""
        # Test that factory can create different discount types
        available_types = discount_service.discount_factory.get_available_discount_types()
        
        expected_types = ["brand", "voucher", "bank", "tier", "category", "loyalty", "seasonal"]
        
        for discount_type in expected_types:
            assert discount_type in available_types

    @pytest.mark.asyncio
    async def test_large_cart_performance(self, discount_service, sample_products, sample_customer):
        """Test performance with large cart"""
        # Create a large cart with multiple items
        large_cart = []
        for i in range(10):  # 10 different items
            for product in sample_products:
                large_cart.append(
                    CartItem(
                        product=product, 
                        quantity=i+1, 
                        size=f"Size{i}", 
                        price=product.base_price
                    )
                )
        
        result = await discount_service.calculate_cart_discounts(
            cart_items=large_cart,
            customer=sample_customer
        )

        assert isinstance(result, DiscountedPrice)
        assert result.original_price > Decimal('0')
        assert result.final_price >= Decimal('0')

    @pytest.mark.asyncio
    async def test_decimal_precision(self, discount_service, sample_cart_items, sample_customer):
        """Test decimal precision in calculations"""
        result = await discount_service.calculate_cart_discounts(
            cart_items=sample_cart_items,
            customer=sample_customer
        )

        # Check that all prices are Decimal types
        assert isinstance(result.original_price, Decimal)
        assert isinstance(result.final_price, Decimal)
        
        # Check that discount amounts are Decimal types
        for discount_amount in result.applied_discounts.values():
            assert isinstance(discount_amount, Decimal)

    @pytest.mark.asyncio
    async def test_negative_price_protection(self, discount_service, sample_customer):
        """Test that final price cannot go below zero"""
        # Create a low-price item that could result in negative final price
        low_price_product = Product(
            id="LOW001",
            brand="PUMA",
            brand_tier=BrandTier.REGULAR,
            category="T-shirts",
            base_price=Decimal('10'),
            current_price=Decimal('10')
        )
        
        low_price_cart = [
            CartItem(product=low_price_product, quantity=1, size="S", price=low_price_product.base_price)
        ]
        
        result = await discount_service.calculate_cart_discounts(
            cart_items=low_price_cart,
            customer=sample_customer,
            voucher_code="SUPER69"
        )

        assert result.final_price >= Decimal('0')

    def test_discount_service_initialization(self):
        """Test DiscountService initialization"""
        service = DiscountService()
        
        # Check that all required components are initialized
        assert hasattr(service, 'discount_factory')
        assert hasattr(service, 'discount_codes')
        assert service.discount_factory is not None
        assert service.discount_codes is not None