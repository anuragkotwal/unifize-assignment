# Fashion E-Commerce Discount Service

A comprehensive discount service for fashion e-commerce platforms, capable of handling various discount scenarios including brand-specific discounts, bank card offers, category-specific deals, and voucher codes with advanced stacking capabilities.

## 🌟 Features

- **Brand-Specific Discounts**: Apply discounts based on product brands (e.g., "Min 40% off on PUMA")
- **Bank Card Offers**: Instant discounts for specific bank card transactions (e.g., "10% instant discount on ICICI Bank cards")
- **Category-Specific Deals**: Additional discounts based on product categories (e.g., "Extra 10% off on T-shirts")
- **Voucher Codes**: Support for discount codes that can be applied to any product (e.g., 'SUPER69' for special offers)
- **Customer Tier Benefits**: Special discounts for premium customers
- **Advanced Discount Stacking**: Apply multiple discounts with intelligent priority handling
- **Factory Pattern**: Extensible discount system for easy addition of new discount types

## 📁 Project Structure

```
unifize-assignment/
├── src/
│   ├── models/
│   │   ├── __init__.py           # Model exports
│   │   ├── product.py            # Product and BrandTier definitions
│   │   ├── cart.py               # CartItem definition
│   │   ├── customer.py           # CustomerProfile definition
│   │   ├── payment.py            # PaymentInfo definition
│   │   └── discount.py           # DiscountedPrice definition
│   ├── services/
│   │   ├── __init__.py           # Service exports
│   │   └── discount_service.py   # Main DiscountService implementation
│   ├── discount_types/
│   │   ├── __init__.py           # Discount type exports
│   │   ├── base_discount.py      # Abstract base discount class
│   │   ├── discount_factory.py   # Factory for creating discount instances
│   │   ├── brand_discount.py     # Brand-specific discount logic
│   │   ├── category_discount.py  # Category-specific discount logic
│   │   ├── bank_discount.py      # Bank offer discount logic
│   │   ├── voucher_discount.py   # Voucher discount logic
│   │   ├── tier_discount.py      # Customer tier discount logic
│   │   ├── loyalty_discount.py   # Loyalty points discount logic
│   │   └── seasonal_discount.py  # Seasonal discount logic
│   └── utils/
│       ├── __init__.py           # Utility exports
│       └── helpers.py            # Helper functions
├── examples/
│   └── demo_usage.py             # Comprehensive usage example
├── tests/
│   ├── __init__.py               # Test package
│   ├── test_discount_service.py  # Main service tests
│   └── test_models.py            # Model tests
├── requirements.txt              # Project dependencies
└── README.md                     # This file
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Steps

1. **Clone the repository:**

   ```bash
   git clone https://github.com/anuragkotwal/unifize-assignment.git
   cd unifize-assignment
   ```

2. **Create a virtual environment (recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # OR on Windows: venv\Scripts\activate
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Verify installation:**
   ```bash
   python -c "from src.services.discount_service import DiscountService; print('✅ Installation successful!')"
   ```

## 🎯 Usage

### Quick Start - Run the Demo

The easiest way to see the discount service in action is to run the interactive demo:

```bash
python examples/demo_usage.py
```

This comprehensive demo showcases:

- ✅ Multiple discount scenarios
- ✅ Brand and category discounts
- ✅ Bank card offers
- ✅ Voucher code applications
- ✅ Advanced discount combinations
- ✅ Customer tier benefits
- ✅ Real-world pricing examples

### Basic Usage Example

```python
import asyncio
from decimal import Decimal
from src.services.discount_service import DiscountService
from src.models.product import Product, BrandTier
from src.models.cart import CartItem
from src.models.customer import CustomerProfile
from src.models.payment import PaymentInfo

async def basic_example():
    # Initialize the service
    discount_service = DiscountService()

    # Create a product
    product = Product(
        id="PUMA001",
        brand="PUMA",
        brand_tier=BrandTier.REGULAR,
        category="T-shirts",
        base_price=Decimal('1000'),
        current_price=Decimal('1000')
    )

    # Create cart
    cart_items = [CartItem(product=product, quantity=2, size="M", price=product.base_price)]

    # Create customer
    customer = CustomerProfile(
        id="CUST001",
        name="John Doe",
        email="john@example.com",
        tier="premium",
        loyalty_points=1500
    )

    # Create payment info
    payment_info = PaymentInfo(
        method="CARD",
        bank_name="ICICI",
        card_type="CREDIT"
    )

    # Calculate discounts
    result = await discount_service.calculate_cart_discounts(
        cart_items=cart_items,
        customer=customer,
        payment_info=payment_info,
        voucher_code="SUPER69"
    )

    print(f"Original Price: ₹{result.original_price}")
    print(f"Final Price: ₹{result.final_price}")
    print(f"Total Savings: ₹{result.original_price - result.final_price}")
    print(f"Applied Discounts: {result.applied_discounts}")

# Run the example
asyncio.run(basic_example())
```

### Advanced Usage - Custom Discount Configurations

```python
async def advanced_example():
    discount_service = DiscountService()

    # Define custom discount configurations
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

    # Apply advanced discounts
    result = await discount_service.apply_advanced_discounts(
        cart_items=cart_items,
        customer=customer,
        payment_info=payment_info,
        discount_configs=discount_configs
    )

    print(f"Advanced Discount Result: {result}")
```

## 🧪 Testing

Run the test suite to verify functionality:

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_discount_service.py -v

# Run with coverage (install pytest-cov first)
pip install pytest-cov
python -m pytest tests/ --cov=src --cov-report=html
```

### Test Coverage

The test suite covers:

- ✅ Individual discount type calculations
- ✅ Multiple discount combinations
- ✅ Voucher validation logic
- ✅ Edge cases and error conditions
- ✅ Customer tier validations
- ✅ Bank offer applications
- ✅ Factory pattern functionality

## 🎨 Key Features Demonstrated

### 1. Intelligent Discount Stacking

```
Example Cart: NIKE Shoes (₹5000) + PUMA T-shirt (₹1000)
↓
Brand Discounts Applied: NIKE 35% + PUMA 40%
↓
Bank Offer: ICICI 10% instant discount
↓
Voucher Code: SUPER69 for additional savings
↓
Final Price with Maximum Savings!
```

### 2. Supported Discount Types

#### 🏷️ Brand Discounts

- **PUMA**: 40% off
- **NIKE**: 35% off
- **ADIDAS**: 30% off
- **ZARA**: 25% off
- **H&M**: 20% off

#### 🏪 Category Discounts

- **T-shirts**: 10% off
- **Jeans**: 15% off
- **Shoes**: 20% off
- **Accessories**: 5% off
- **Jackets**: 25% off

#### 💳 Bank Offers

- **ICICI**: 10% off (max ₹500)
- **HDFC**: 8% off (max ₹400)
- **SBI**: 5% off (max ₹250)
- **AXIS**: 12% off (max ₹600)

#### 🎫 Voucher Codes

- **SUPER69**: Special discount (max ₹1000)
- **PREMIUM20**: 20% off (max ₹500, Premium customers only)
- **NEWUSER15**: 15% off (max ₹300, New users only)

#### 👑 Customer Tiers

- **Premium**: Exclusive discounts and higher limits
- **Gold**: Enhanced discount percentages
- **Silver**: Standard discount access

## 📚 API Reference

### DiscountService

The main service class that orchestrates all discount calculations:

```python
class DiscountService:
    async def calculate_cart_discounts(
        self,
        cart_items: List[CartItem],
        customer: CustomerProfile,
        payment_info: Optional[PaymentInfo] = None,
        voucher_code: Optional[str] = None
    ) -> DiscountedPrice

    async def apply_advanced_discounts(
        self,
        cart_items: List[CartItem],
        customer: CustomerProfile,
        payment_info: Optional[PaymentInfo] = None,
        discount_configs: Optional[List[Dict]] = None
    ) -> DiscountedPrice

    async def validate_discount_code(
        self,
        code: str,
        cart_items: List[CartItem],
        customer: CustomerProfile
    ) -> bool
```

### DiscountedPrice

Result object containing discount calculation details:

```python
@dataclass
class DiscountedPrice:
    original_price: Decimal
    final_price: Decimal
    applied_discounts: Dict[str, Decimal]
    message: str
```

## 🔧 Troubleshooting

### Common Issues

1. **Import Errors**

   ```bash
   # Ensure you're in the project root directory
   pwd  # Should show: .../unifize-assignment

   # Verify Python path includes current directory
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

2. **Module Not Found**

   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt

   # Check project structure
   ls -la src/
   ```

3. **Test Failures**

   ```bash
   # Run tests with detailed output
   python -m pytest tests/ -v -s
   ```

4. **Decimal Type Errors**
   - Ensure all price values use `Decimal` type instead of `float`
   - Import: `from decimal import Decimal`

### Getting Help

If you encounter issues:

1. ✅ Check that all dependencies are installed
2. ✅ Verify you're using Python 3.8+
3. ✅ Ensure you're in the correct directory
4. ✅ Run the demo script to verify setup
5. ✅ Check the test suite for working examples

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/new-discount-type`
3. **Add tests for new functionality**
4. **Ensure all tests pass**: `python -m pytest tests/`
5. **Follow the existing code style**
6. **Submit a pull request**

### Adding New Discount Types

The system uses a factory pattern for easy extensibility:

```python
# 1. Create new discount class inheriting from BaseDiscount
# 2. Implement required abstract methods
# 3. Register in DiscountFactory
# 4. Add tests for the new discount type
```

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

**🛒 Happy Shopping with Maximum Savings! 💰**

_Built with ❤️ for fashion e-commerce platforms_
