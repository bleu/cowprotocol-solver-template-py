from decimal import Decimal


def to_decimal(value: int, decimals: int = 18) -> Decimal:
    """Convert to decimal with given decimals (default 18 for ETH)"""
    return Decimal(str(value)) / Decimal(10**decimals)


def from_decimal(value: Decimal, decimals: int = 18) -> int:
    """Create from decimal value with given decimals"""
    return int(value * Decimal(10**decimals))
