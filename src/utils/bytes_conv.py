"""
Byte conversion utilities.

This module provides utilities for converting between different byte representations.
"""

from typing import Union, List
import struct


def to_bytes32(value: Union[int, str, bytes]) -> bytes:
    """
    Convert value to 32-byte representation.

    Args:
        value: Value to convert

    Returns:
        32-byte representation
    """
    if isinstance(value, int):
        return value.to_bytes(32, "big")
    elif isinstance(value, str):
        if value.startswith("0x"):
            hex_str = value[2:]
        else:
            hex_str = value
        return bytes.fromhex(hex_str.zfill(64))
    elif isinstance(value, bytes):
        if len(value) > 32:
            return value[-32:]  # Take last 32 bytes
        else:
            return value.rjust(32, b"\x00")
    else:
        raise TypeError(f"Cannot convert {type(value)} to bytes32")


def from_bytes32(value: bytes) -> int:
    """
    Convert 32-byte representation to integer.

    Args:
        value: 32-byte value

    Returns:
        Integer value
    """
    if len(value) != 32:
        raise ValueError("Value must be exactly 32 bytes")
    return int.from_bytes(value, "big")


def to_bytes20(value: Union[int, str, bytes]) -> bytes:
    """
    Convert value to 20-byte representation (Ethereum address).

    Args:
        value: Value to convert

    Returns:
        20-byte representation
    """
    if isinstance(value, int):
        return value.to_bytes(20, "big")
    elif isinstance(value, str):
        if value.startswith("0x"):
            hex_str = value[2:]
        else:
            hex_str = value
        return bytes.fromhex(hex_str.zfill(40))
    elif isinstance(value, bytes):
        if len(value) > 20:
            return value[-20:]  # Take last 20 bytes
        else:
            return value.rjust(20, b"\x00")
    else:
        raise TypeError(f"Cannot convert {type(value)} to bytes20")


def from_bytes20(value: bytes) -> int:
    """
    Convert 20-byte representation to integer.

    Args:
        value: 20-byte value

    Returns:
        Integer value
    """
    if len(value) != 20:
        raise ValueError("Value must be exactly 20 bytes")
    return int.from_bytes(value, "big")


def to_bytes4(value: Union[int, str, bytes]) -> bytes:
    """
    Convert value to 4-byte representation.

    Args:
        value: Value to convert

    Returns:
        4-byte representation
    """
    if isinstance(value, int):
        return value.to_bytes(4, "big")
    elif isinstance(value, str):
        if value.startswith("0x"):
            hex_str = value[2:]
        else:
            hex_str = value
        return bytes.fromhex(hex_str.zfill(8))
    elif isinstance(value, bytes):
        if len(value) > 4:
            return value[-4:]  # Take last 4 bytes
        else:
            return value.rjust(4, b"\x00")
    else:
        raise TypeError(f"Cannot convert {type(value)} to bytes4")


def from_bytes4(value: bytes) -> int:
    """
    Convert 4-byte representation to integer.

    Args:
        value: 4-byte value

    Returns:
        Integer value
    """
    if len(value) != 4:
        raise ValueError("Value must be exactly 4 bytes")
    return int.from_bytes(value, "big")


def pack_uint256(value: int) -> bytes:
    """
    Pack uint256 value into bytes.

    Args:
        value: Uint256 value

    Returns:
        Packed bytes
    """
    return value.to_bytes(32, "big")


def unpack_uint256(value: bytes) -> int:
    """
    Unpack bytes to uint256 value.

    Args:
        value: Packed bytes

    Returns:
        Uint256 value
    """
    if len(value) != 32:
        raise ValueError("Value must be exactly 32 bytes")
    return int.from_bytes(value, "big")


def pack_uint128(value: int) -> bytes:
    """
    Pack uint128 value into bytes.

    Args:
        value: Uint128 value

    Returns:
        Packed bytes
    """
    return value.to_bytes(16, "big")


def unpack_uint128(value: bytes) -> int:
    """
    Unpack bytes to uint128 value.

    Args:
        value: Packed bytes

    Returns:
        Uint128 value
    """
    if len(value) != 16:
        raise ValueError("Value must be exactly 16 bytes")
    return int.from_bytes(value, "big")


def pack_uint64(value: int) -> bytes:
    """
    Pack uint64 value into bytes.

    Args:
        value: Uint64 value

    Returns:
        Packed bytes
    """
    return value.to_bytes(8, "big")


def unpack_uint64(value: bytes) -> int:
    """
    Unpack bytes to uint64 value.

    Args:
        value: Packed bytes

    Returns:
        Uint64 value
    """
    if len(value) != 8:
        raise ValueError("Value must be exactly 8 bytes")
    return int.from_bytes(value, "big")


def pack_uint32(value: int) -> bytes:
    """
    Pack uint32 value into bytes.

    Args:
        value: Uint32 value

    Returns:
        Packed bytes
    """
    return value.to_bytes(4, "big")


def unpack_uint32(value: bytes) -> int:
    """
    Unpack bytes to uint32 value.

    Args:
        value: Packed bytes

    Returns:
        Uint32 value
    """
    if len(value) != 4:
        raise ValueError("Value must be exactly 4 bytes")
    return int.from_bytes(value, "big")


def pack_uint8(value: int) -> bytes:
    """
    Pack uint8 value into bytes.

    Args:
        value: Uint8 value

    Returns:
        Packed bytes
    """
    return value.to_bytes(1, "big")


def unpack_uint8(value: bytes) -> int:
    """
    Unpack bytes to uint8 value.

    Args:
        value: Packed bytes

    Returns:
        Uint8 value
    """
    if len(value) != 1:
        raise ValueError("Value must be exactly 1 byte")
    return int.from_bytes(value, "big")


def concat_bytes(*values: bytes) -> bytes:
    """
    Concatenate multiple byte values.

    Args:
        *values: Byte values to concatenate

    Returns:
        Concatenated bytes
    """
    return b"".join(values)


def split_bytes(value: bytes, chunk_size: int) -> List[bytes]:
    """
    Split bytes into chunks of specified size.

    Args:
        value: Bytes to split
        chunk_size: Size of each chunk

    Returns:
        List of byte chunks
    """
    return [value[i : i + chunk_size] for i in range(0, len(value), chunk_size)]
