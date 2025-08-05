#!/usr/bin/env python3
"""
Fashion E-Commerce Discount Service Usage Example

This script demonstrates how to use the DiscountService class for calculating
various types of discounts in a fashion e-commerce platform.

Run this script to see examples of:
1. Brand-specific discounts
2. Category-specific discounts  
3. Bank card offers
4. Voucher codes
5. Multiple discount combinations
"""

import asyncio
import os
import sys
from decimal import Decimal
from typing import List

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.services.discount_service import DiscountService
from src.models.product import Product, BrandTier
from src.models.cart import CartItem
from src.models.customer import CustomerProfile
from src.models.payment import PaymentInfo


class DiscountServiceDemo:
    def __init__(self):
        self.discount_service = DiscountService()
        
    def create_sample_products(self) -> List[Product]:
        """Create sample products for demonstration"""
        return [
            Product(
                id="PUMA001",
                brand="PUMA",
                brand_tier=BrandTier.REGULAR,
                category="T-shirts",
                base_price=Decimal('1000'),
                current_price=Decimal('1000')  # Use base price for clean interface demo
            ),
            Product(
                id="NIKE001", 
                brand="NIKE",
                brand_tier=BrandTier.PREMIUM,
                category="Shoes",
                base_price=Decimal('5000'),
                current_price=Decimal('5000')  # Use base price for clean interface demo
            ),
            Product(
                id="ZARA001",
                brand="ZARA", 
                brand_tier=BrandTier.REGULAR,
                category="Jeans",
                base_price=Decimal('2000'),
                current_price=Decimal('2000')  # Use base price for clean interface demo
            )
        ]
    
    def create_sample_customer(self) -> CustomerProfile:
        """Create a sample customer"""
        return CustomerProfile(
            id="CUST001",
            name="John Doe",
            email="john.doe@example.com", 
            tier="premium",
            loyalty_points=1500
        )
    
    def create_cart_items(self, products: List[Product]) -> List[CartItem]:
        """Create cart items from products"""
        return [
            CartItem(product=products[0], quantity=2, size="M", price=products[0].base_price),    # 2x PUMA T-shirts
            CartItem(product=products[1], quantity=1, size="9", price=products[1].base_price),    # 1x NIKE Shoes  
            CartItem(product=products[2], quantity=1, size="32", price=products[2].base_price)    # 1x ZARA Jeans
        ]
    
    def print_cart_summary(self, cart_items: List[CartItem]):
        """Print cart summary"""
        print("🛒 Shopping Cart:")
        print("-" * 50)
        total_base = Decimal('0')
        total_current = Decimal('0')
        
        for item in cart_items:
            item_base = item.product.base_price * item.quantity
            item_current = item.product.current_price * item.quantity
            total_base += item_base
            total_current += item_current
            
            print(f"📦 {item.product.brand} {item.product.category} (Size: {item.size})")
            print(f"   Quantity: {item.quantity}")
            print(f"   Base Price: ₹{item.product.base_price} → Current: ₹{item.product.current_price}")
            print(f"   Subtotal: ₹{item_base} → ₹{item_current}")
            print()
        
        print(f"💰 Cart Total (Base): ₹{total_base}")
        print(f"💰 Cart Total (Current): ₹{total_current}")
        print("=" * 60)
    
    def print_discount_result(self, result, scenario_name: str):
        """Print discount calculation results"""
        print(f"\n🎯 {scenario_name}")
        print("-" * 50)
        print(f"Original Price: ₹{result.original_price}")
        
        if result.applied_discounts:
            print("Applied Discounts:")
            for discount_name, amount in result.applied_discounts.items():
                print(f"  • {discount_name}: -₹{amount}")
        
        print(f"Final Price: ₹{result.final_price}")
        print(f"Total Savings: ₹{result.original_price - result.final_price}")
        savings_percent = ((result.original_price - result.final_price) / result.original_price) * 100 if result.original_price > 0 else 0
        print(f"Savings Percentage: {savings_percent:.1f}%")
        print(f"Status: {result.message}")
        print("=" * 60)

    async def run_demo(self):
        """Run the complete demonstration"""
        print("🎉 Welcome to Fashion E-Commerce Discount Service Demo!")
        print("=" * 60)
        
        # Setup
        products = self.create_sample_products()
        customer = self.create_sample_customer()
        cart_items = self.create_cart_items(products)
        
        # Display cart
        self.print_cart_summary(cart_items)
        
        # Scenario 1: Brand discounts using new interface
        print("\n📊 SCENARIO 1: Brand Discounts Only")
        brand_discount_configs = [
            {
                "type": "brand",
                "brand": "PUMA",
                "discount_percentage": Decimal("40")  # 40% discount on PUMA
            },
            {
                "type": "brand", 
                "brand": "NIKE",
                "discount_percentage": Decimal("35")  # 35% discount on NIKE
            },
            {
                "type": "brand",
                "brand": "ZARA", 
                "discount_percentage": Decimal("25")  # 25% discount on ZARA
            }
        ]
        
        result1 = await self.discount_service.apply_advanced_discounts(
            cart_items=cart_items,
            customer=customer,
            discount_configs=brand_discount_configs
        )
        self.print_discount_result(result1, "Brand Discounts Applied")
        
        # Scenario 2: Add Bank Offer
        print("\n📊 SCENARIO 2: Brand Discounts + Bank Card Offer")
        icici_payment = PaymentInfo(
            method="CARD",
            bank_name="ICICI", 
            card_type="CREDIT"
        )
        
        result2 = await self.discount_service.calculate_cart_discounts(
            cart_items=cart_items,
            customer=customer,
            payment_info=icici_payment
        )
        self.print_discount_result(result2, "With ICICI Bank Offer")
        
        # Scenario 3: Add Voucher Code
        print("\n📊 SCENARIO 3: Brand Discounts + Bank Offer + Voucher Code")
        result3 = await self.discount_service.calculate_cart_discounts(
            cart_items=cart_items,
            customer=customer,
            payment_info=icici_payment,
            voucher_code="SUPER69"
        )
        self.print_discount_result(result3, "With SUPER69 Voucher")
        
        # Scenario 4: Different Bank
        print("\n📊 SCENARIO 4: Different Bank Offer")
        hdfc_payment = PaymentInfo(
            method="CARD",
            bank_name="HDFC",
            card_type="CREDIT"
        )
        
        result4 = await self.discount_service.calculate_cart_discounts(
            cart_items=cart_items,
            customer=customer,
            payment_info=hdfc_payment,
            voucher_code="SUPER69"
        )
        self.print_discount_result(result4, "With HDFC Bank Offer")
        
        # Scenario 5: Advanced discounts with multiple types
        print("\n📊 SCENARIO 5: Advanced Multi-Type Discounts")
        advanced_configs = [
            {
                "type": "brand",
                "brand": "NIKE",
                "discount_percentage": Decimal("20"),
                "max_discount": Decimal("800")
            },
            {
                "type": "tier",
                "required_tier": "premium",
                "discount_percentage": Decimal("10"),
                "max_discount": Decimal("500")
            }
        ]
        
        result5 = await self.discount_service.apply_advanced_discounts(
            cart_items=cart_items,
            customer=customer,
            payment_info=icici_payment,
            discount_configs=advanced_configs
        )
        self.print_discount_result(result5, "Advanced Multi-Type Discounts")
        
        # Voucher Validation Demo
        print("\n📊 VOUCHER VALIDATION DEMO")
        print("-" * 50)
        
        voucher_codes = ["SUPER69", "PREMIUM20", "NEWUSER15", "INVALID123"]
        
        for code in voucher_codes:
            is_valid = await self.discount_service.validate_discount_code(
                code, cart_items, customer
            )
            status = "✅ Valid" if is_valid else "❌ Invalid"
            print(f"Voucher '{code}': {status}")
        
        print("\n🎉 Demo completed! Thank you for using the Discount Service!")


async def main():
    """Main function to run the demo"""
    demo = DiscountServiceDemo()
    await demo.run_demo()


if __name__ == "__main__":
    print("Starting Discount Service Demo...")
    asyncio.run(main())