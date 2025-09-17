"""
Base types for reference and utility.
"""
from __future__ import annotations

from typing import Union, Any
from decimal import Decimal


# Type aliases for better code readability
NumericType = Union[int, float, Decimal, str]
TokenAmount = str  # U256 as string
TokenAddress = str  # H160 as string
OrderUid = str  # [u8; 56] as hex string


def is_valid_address(address: str) -> bool:
    """Check if address is a valid Ethereum address"""
    return address.startswith('0x') and len(address) == 42


def is_valid_hex(hex_str: str) -> bool:
    """Check if string is valid hex"""
    try:
        int(hex_str, 16)
        return True
    except ValueError:
        return False
