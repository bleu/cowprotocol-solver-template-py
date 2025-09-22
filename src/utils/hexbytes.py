"""
Hex string and bytes utilities.

This module provides utilities for working with hex strings and bytes.
"""

from typing import Union
import binascii


def to_hex(value: Union[int, bytes, str]) -> str:
    """
    Convert a value to hex string.
    
    Args:
        value: Value to convert
        
    Returns:
        Hex string with 0x prefix
    """
    if isinstance(value, int):
        return hex(value)
    elif isinstance(value, bytes):
        return '0x' + value.hex()
    elif isinstance(value, str):
        if value.startswith('0x'):
            return value
        else:
            return '0x' + value
    else:
        raise TypeError(f"Cannot convert {type(value)} to hex string")


def from_hex(value: str) -> bytes:
    """
    Convert hex string to bytes.
    
    Args:
        value: Hex string
        
    Returns:
        Bytes object
    """
    if value.startswith('0x'):
        return bytes.fromhex(value[2:])
    else:
        return bytes.fromhex(value)


def to_bytes(value: Union[int, str]) -> bytes:
    """
    Convert value to bytes.
    
    Args:
        value: Value to convert
        
    Returns:
        Bytes object
    """
    if isinstance(value, int):
        return value.to_bytes((value.bit_length() + 7) // 8, 'big')
    elif isinstance(value, str):
        if value.startswith('0x'):
            return bytes.fromhex(value[2:])
        else:
            return bytes.fromhex(value)
    else:
        raise TypeError(f"Cannot convert {type(value)} to bytes")


def from_bytes(value: bytes) -> str:
    """
    Convert bytes to hex string.
    
    Args:
        value: Bytes object
        
    Returns:
        Hex string with 0x prefix
    """
    return '0x' + value.hex()


def pad_hex(value: str, length: int) -> str:
    """
    Pad hex string to specified length.
    
    Args:
        value: Hex string
        length: Target length
        
    Returns:
        Padded hex string
    """
    if value.startswith('0x'):
        value = value[2:]
    
    # Pad with leading zeros
    padded = value.zfill(length)
    return '0x' + padded


def strip_hex_prefix(value: str) -> str:
    """
    Strip 0x prefix from hex string.
    
    Args:
        value: Hex string
        
    Returns:
        Hex string without prefix
    """
    if value.startswith('0x'):
        return value[2:]
    return value


def add_hex_prefix(value: str) -> str:
    """
    Add 0x prefix to hex string.
    
    Args:
        value: Hex string
        
    Returns:
        Hex string with prefix
    """
    if value.startswith('0x'):
        return value
    return '0x' + value


def is_valid_hex(value: str) -> bool:
    """
    Check if string is valid hex.
    
    Args:
        value: String to check
        
    Returns:
        True if valid hex, False otherwise
    """
    try:
        if value.startswith('0x'):
            value = value[2:]
        int(value, 16)
        return True
    except ValueError:
        return False


def hex_to_int(value: str) -> int:
    """
    Convert hex string to integer.
    
    Args:
        value: Hex string
        
    Returns:
        Integer value
    """
    if value.startswith('0x'):
        return int(value, 16)
    else:
        return int(value, 16)


def int_to_hex(value: int, length: int = None) -> str:
    """
    Convert integer to hex string.
    
    Args:
        value: Integer value
        length: Optional length for padding
        
    Returns:
        Hex string
    """
    hex_str = hex(value)
    if length is not None:
        hex_str = pad_hex(hex_str, length)
    return hex_str


def bytes_to_hex(value: bytes) -> str:
    """
    Convert bytes to hex string.
    
    Args:
        value: Bytes object
        
    Returns:
        Hex string with 0x prefix
    """
    return '0x' + value.hex()


def hex_to_bytes(value: str) -> bytes:
    """
    Convert hex string to bytes.
    
    Args:
        value: Hex string
        
    Returns:
        Bytes object
    """
    if value.startswith('0x'):
        return bytes.fromhex(value[2:])
    else:
        return bytes.fromhex(value)
