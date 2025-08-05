from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

class CustomerTier(Enum):
    PREMIUM = "premium"
    REGULAR = "regular"
    BUDGET = "budget"

@dataclass
class CustomerProfile:
    id: str
    name: str
    email: str
    tier: CustomerTier
    loyalty_points: Decimal  # Points accumulated by the customer for discounts or offers