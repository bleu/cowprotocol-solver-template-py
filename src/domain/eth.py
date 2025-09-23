from typing import NewType, Optional
from decimal import Decimal

class Address:
    """
    Ethereum address with validation.
    
    - Must start with 0x
    - Must have 42 characters total (0x + 40 hex)
    - Store as lowercase for comparisons
    """
    def __init__(self, value: str):
        if not value.startswith("0x") or len(value) != 42:
            raise ValueError(f"Invalid address: {value}")
        # Validate hex characters
        try:
            int(value[2:], 16)
        except ValueError:
            raise ValueError(f"Invalid hex in address: {value}")
        self.value = value.lower()
    
    def __eq__(self, other) -> bool:
        return isinstance(other, Address) and self.value == other.value
    
    def __hash__(self) -> int:
        return hash(self.value)
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"Address('{self.value}')"


class U256:
    """
    256-bit unsigned integer as used in Ethereum.
    """
    MAX = 2**256 - 1
    
    def __init__(self, value: int | str | Decimal):
        if isinstance(value, str):
            # Handle hex strings
            if value.startswith("0x"):
                value = int(value, 16)
            else:
                value = int(value)
        elif isinstance(value, Decimal):
            value = int(value)
        
        if value < 0 or value > self.MAX:
            raise ValueError(f"Value out of U256 range: {value}")
        self.value = value
    
    def __add__(self, other: "U256") -> "U256":
        result = self.value + other.value
        if result > self.MAX:
            raise OverflowError("U256 addition overflow")
        return U256(result)
    
    def __sub__(self, other: "U256") -> "U256":
        if self.value < other.value:
            raise ValueError("U256 subtraction underflow")
        return U256(self.value - other.value)
    
    def __mul__(self, other: "U256") -> "U256":
        result = self.value * other.value
        if result > self.MAX:
            raise OverflowError("U256 multiplication overflow")
        return U256(result)
    
    def __truediv__(self, other: "U256") -> "U256":
        """Integer division"""
        if other.value == 0:
            raise ZeroDivisionError("Division by zero")
        return U256(self.value // other.value)
    
    def __floordiv__(self, other: "U256") -> "U256":
        if other.value == 0:
            raise ZeroDivisionError("Division by zero")
        return U256(self.value // other.value)
    
    def __mod__(self, other: "U256") -> "U256":
        if other.value == 0:
            raise ZeroDivisionError("Division by zero")
        return U256(self.value % other.value)
    
    def __lt__(self, other: "U256") -> bool:
        return self.value < other.value
    
    def __le__(self, other: "U256") -> bool:
        return self.value <= other.value
    
    def __gt__(self, other: "U256") -> bool:
        return self.value > other.value
    
    def __ge__(self, other: "U256") -> bool:
        return self.value >= other.value
    
    def __eq__(self, other) -> bool:
        return isinstance(other, U256) and self.value == other.value
    
    def __str__(self) -> str:
        return str(self.value)
    
    def __repr__(self) -> str:
        return f"U256({self.value})"
    
    def to_decimal(self, decimals: int = 18) -> Decimal:
        """Convert to decimal with given decimals (default 18 for ETH)"""
        return Decimal(str(self.value)) / Decimal(10 ** decimals)
    
    @classmethod
    def from_decimal(cls, value: Decimal, decimals: int = 18) -> "U256":
        """Create from decimal value with given decimals"""
        wei_value = int(value * Decimal(10 ** decimals))
        return cls(wei_value)


class Asset:
    """Token amount pair."""
    def __init__(self, token: Address, amount: U256):
        self.token = token
        self.amount = amount
    
    def __repr__(self) -> str:
        return f"Asset(token={self.token}, amount={self.amount})"


class WethAddress(Address):
    """Wrapper for WETH address."""
    pass