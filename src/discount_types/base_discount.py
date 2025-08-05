from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Dict, Optional
from src.models.cart import CartItem
from src.models.customer import CustomerProfile
from src.models.payment import PaymentInfo

class BaseDiscount(ABC):
    """
    Abstract base class for all discount types.
    Provides a consistent interface for implementing different discount strategies.
    """
    
    def __init__(self, discount_id: str, discount_name: str):
        self.discount_id = discount_id
        self.discount_name = discount_name
    
    @abstractmethod
    async def calculate_discount(
        self, 
        cart_items: List[CartItem], 
        customer: CustomerProfile,
        payment_info: Optional[PaymentInfo] = None,
        **kwargs
    ) -> Decimal:
        """
        Calculate the discount amount for the given cart and customer.
        
        Args:
            cart_items: List of items in the cart
            customer: Customer profile
            payment_info: Optional payment information
            **kwargs: Additional parameters specific to discount type
            
        Returns:
            Decimal: The discount amount to be applied
        """
        pass
    
    @abstractmethod
    async def is_applicable(
        self, 
        cart_items: List[CartItem], 
        customer: CustomerProfile,
        payment_info: Optional[PaymentInfo] = None,
        **kwargs
    ) -> bool:
        """
        Check if this discount can be applied to the given cart and customer.
        
        Args:
            cart_items: List of items in the cart
            customer: Customer profile
            payment_info: Optional payment information
            **kwargs: Additional parameters specific to discount type
            
        Returns:
            bool: True if discount can be applied, False otherwise
        """
        pass
    
    def get_discount_info(self) -> Dict[str, str]:
        """
        Get basic information about this discount type.
        
        Returns:
            Dict containing discount ID and name
        """
        return {
            "id": self.discount_id,
            "name": self.discount_name
        }
    
    def calculate_cart_total(self, cart_items: List[CartItem]) -> Decimal:
        """
        Helper method to calculate total cart value.
        
        Args:
            cart_items: List of cart items
            
        Returns:
            Decimal: Total cart value using current prices
        """
        return sum(item.product.current_price * item.quantity for item in cart_items)
    
    def get_cart_brands(self, cart_items: List[CartItem]) -> set:
        """
        Helper method to get all brands in the cart.
        
        Args:
            cart_items: List of cart items
            
        Returns:
            Set of brand names
        """
        return {item.product.brand for item in cart_items}
    
    def get_cart_categories(self, cart_items: List[CartItem]) -> set:
        """
        Helper method to get all categories in the cart.
        
        Args:
            cart_items: List of cart items
            
        Returns:
            Set of category names
        """
        return {item.product.category for item in cart_items}