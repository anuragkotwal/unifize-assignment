from dataclasses import dataclass
from typing import Optional
from enum import Enum


class PaymentMethod(Enum):
    CARD = "CARD"
    UPI = "UPI"
    NET_BANKING = "NET_BANKING"
    WALLET = "WALLET"
    COD = "COD"


class CardType(Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"


@dataclass
class PaymentInfo:
    """Payment information for processing bank offers and payment-specific discounts"""
    method: str  # PaymentMethod enum value as string
    bank_name: Optional[str] = None
    card_type: Optional[str] = None  # CardType enum value as string
    
    def __post_init__(self):
        """Validate payment information"""
        if self.method == PaymentMethod.CARD.value and not self.bank_name:
            raise ValueError("Bank name is required for card payments")
        
        if self.method == PaymentMethod.CARD.value and not self.card_type:
            raise ValueError("Card type is required for card payments")