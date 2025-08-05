# Discount Service

This project implements a discount service for a fashion e-commerce website, capable of handling various discount scenarios including brand-specific discounts, bank card offers, category-specific deals, and voucher codes.

## Features

- **Brand-Specific Discounts**: Apply discounts based on the brand of the product (e.g., "Min 40% off on PUMA").
- **Bank Card Offers**: Instant discounts for specific bank card transactions (e.g., "10% instant discount on ICICI Bank cards").
- **Category-Specific Deals**: Additional discounts based on product categories (e.g., "Extra 10% off on T-shirts").
- **Vouchers**: Support for discount codes that can be applied to any product (e.g., 'SUPER69' for 69% off).
- **Multiple Discount Stacking**: Apply multiple discounts in the correct order for maximum savings.

## Project Structure

```
discount-service/
├── src/
│   ├── models/
│   │   ├── __init__.py           # Model exports
│   │   ├── product.py            # Product and BrandTier definitions
│   │   ├── cart.py               # CartItem and PaymentInfo definitions
│   │   ├── customer.py           # CustomerProfile and CustomerTier definitions
│   │   └── discount.py           # DiscountedPrice definition
│   ├── services/
│   │   ├── __init__.py           # Service exports
│   │   ├── discount_service.py   # Main DiscountService implementation
│   │   └── validation_service.py # Voucher validation logic
│   ├── discount_types/
│   │   ├── __init__.py           # Discount calculator exports
│   │   ├── brand_discount.py     # Brand-specific discount logic
│   │   ├── category_discount.py  # Category-specific discount logic
│   │   ├── bank_discount.py      # Bank offer discount logic
│   │   └── voucher_discount.py   # Voucher discount logic
│   └── utils/
│       ├── __init__.py           # Utility exports
│       └── helpers.py            # Helper functions
├── tests/
│   ├── __init__.py               # Test package
│   ├── test_discount_service.py  # Main service tests
│   ├── test_validation_service.py # Validation tests
│   └── fake_data.py              # Test data and fixtures
├── demo_usage.py                 # Comprehensive usage example
├── requirements.txt              # Project dependencies
├── setup.py                      # Package setup
└── README.md                     # This file
```

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Setup Steps

1. **Clone or download the repository:**

   ```bash
   cd "Unifize Assignment/discount-service"
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

## Usage

### Quick Start - Run the Demo

The easiest way to see the discount service in action is to run the interactive demo:

```bash
python demo_usage.py
```

This will show you:

- ✅ Multiple discount scenarios
- ✅ Brand and category discounts
- ✅ Bank card offers
- ✅ Voucher code applications
- ✅ Discount validation
- ✅ Real-world pricing examples

### Basic Usage Example

```python
import asyncio
from decimal import Decimal
from src.services.discount_service import DiscountService
from src.models import Product, BrandTier, CartItem, CustomerProfile, CustomerTier, PaymentInfo

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
        current_price=Decimal('500')  # After brand/category discounts
    )

    # Create cart
    cart_items = [CartItem(product=product, quantity=2, size="M")]

    # Create customer
    customer = CustomerProfile(
        id="CUST001",
        name="John Doe",
        email="john@example.com",
        tier=CustomerTier.GOLD
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

# Run the example
asyncio.run(basic_example())
```

### Testing

Run the complete test suite:

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_discount_service.py -v

# Run with coverage
pip install pytest-cov
pytest tests/ --cov=src --cov-report=html
```

### Test Coverage

The test suite covers:

- ✅ Multiple discount scenarios
- ✅ Individual discount types
- ✅ Voucher validation logic
- ✅ Edge cases and error conditions
- ✅ Different customer tiers
- ✅ Various bank offers

## Key Features Demonstrated

### 1. Multiple Discount Scenario

```
PUMA T-shirt (₹1000) → ₹500 (40% brand + 10% category discount)
+ SUPER69 voucher (69% off)
+ ICICI bank offer (10% instant discount)
= Maximum savings!
```

### 2. Discount Stacking Order

1. **Brand/Category discounts** (applied to current_price)
2. **Voucher codes** (applied to cart total)
3. **Bank offers** (applied last)

### 3. Supported Discounts

#### Brand Discounts

- PUMA: 40% off
- NIKE: 35% off
- ADIDAS: 30% off
- ZARA: 25% off
- H&M: 20% off

#### Category Discounts

- T-shirts: 10% off
- Jeans: 15% off
- Shoes: 20% off
- Accessories: 5% off
- Jackets: 25% off

#### Bank Offers

- ICICI: 10% off (max ₹500)
- HDFC: 8% off (max ₹400)
- SBI: 5% off (max ₹250)
- AXIS: 12% off (max ₹600)

#### Voucher Codes

- SUPER69: 69% off (max ₹1000)
- PREMIUM20: 20% off (max ₹500, Gold+ customers)
- NEWUSER15: 15% off (max ₹300)

## API Reference

### DiscountService

```python
class DiscountService:
    async def calculate_cart_discounts(
        self,
        cart_items: List[CartItem],
        customer: CustomerProfile,
        payment_info: Optional[PaymentInfo] = None,
        voucher_code: Optional[str] = None
    ) -> DiscountedPrice

    async def validate_discount_code(
        self,
        code: str,
        cart_items: List[CartItem],
        customer: CustomerProfile
    ) -> bool
```

## Troubleshooting

### Common Issues

1. **Import Errors**

   ```bash
   # Make sure you're in the project root directory
   pwd  # Should show: .../discount-service

   # Check Python path
   python -c "import sys; print('\n'.join(sys.path))"
   ```

2. **Module Not Found**

   ```bash
   # Reinstall requirements
   pip install -r requirements.txt

   # Check if src directory exists
   ls -la src/
   ```

3. **Test Failures**
   ```bash
   # Run tests in verbose mode to see detailed output
   pytest tests/ -v -s
   ```

### Getting Help

If you encounter issues:

1. Check that all dependencies are installed
2. Verify you're using Python 3.7+
3. Make sure you're in the correct directory
4. Run the demo script to verify setup

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

**Happy Shopping with Maximum Savings! 🛒💰**
