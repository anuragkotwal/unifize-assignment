from dataclasses import dataclass
from decimal import Decimal

@dataclass
class CustomerProfile:
    id: str
    name: str
    email: str
    tier: str  # e.g., "premium", "regular", "budget"
    loyalty_points: Decimal  # Points accumulated by the customer for discounts or offers