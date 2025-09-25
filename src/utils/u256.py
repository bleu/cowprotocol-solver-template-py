"""
U256 arithmetic utilities.

This module provides U256 arithmetic operations using Python int.
"""

from typing import Union
import math


def to_u256(value: Union[int, str, float]) -> int:
    """
    Convert a value to U256 (256-bit unsigned integer).

    Args:
        value: Value to convert

    Returns:
        U256 value as Python int
    """
    if isinstance(value, str):
        if value.startswith("0x"):
            return int(value, 16)
        else:
            return int(value)
    elif isinstance(value, float):
        return int(value)
    elif isinstance(value, int):
        return value
    else:
        raise TypeError(f"Cannot convert {type(value)} to U256")


def from_u256(value: int) -> str:
    """
    Convert U256 to hex string.

    Args:
        value: U256 value

    Returns:
        Hex string representation
    """
    return hex(value)


def add_u256(a: int, b: int) -> int:
    """
    Add two U256 values.

    Args:
        a: First U256 value
        b: Second U256 value

    Returns:
        Sum as U256
    """
    return (a + b) & ((1 << 256) - 1)


def sub_u256(a: int, b: int) -> int:
    """
    Subtract two U256 values.

    Args:
        a: First U256 value
        b: Second U256 value

    Returns:
        Difference as U256
    """
    return (a - b) & ((1 << 256) - 1)


def mul_u256(a: int, b: int) -> int:
    """
    Multiply two U256 values.

    Args:
        a: First U256 value
        b: Second U256 value

    Returns:
        Product as U256
    """
    return (a * b) & ((1 << 256) - 1)


def div_u256(a: int, b: int) -> int:
    """
    Divide two U256 values.

    Args:
        a: Dividend
        b: Divisor

    Returns:
        Quotient as U256

    Raises:
        ZeroDivisionError: If divisor is zero
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a // b


def mod_u256(a: int, b: int) -> int:
    """
    Modulo operation for U256 values.

    Args:
        a: Dividend
        b: Divisor

    Returns:
        Remainder as U256

    Raises:
        ZeroDivisionError: If divisor is zero
    """
    if b == 0:
        raise ZeroDivisionError("Cannot modulo by zero")
    return a % b


def pow_u256(base: int, exp: int) -> int:
    """
    Power operation for U256 values.

    Args:
        base: Base value
        exp: Exponent

    Returns:
        Result as U256
    """
    return pow(base, exp, 1 << 256)


def sqrt_u256(value: int) -> int:
    """
    Square root of U256 value.

    Args:
        value: U256 value

    Returns:
        Square root as U256
    """
    return int(math.sqrt(value))


def is_zero(value: int) -> bool:
    """
    Check if U256 value is zero.

    Args:
        value: U256 value

    Returns:
        True if zero, False otherwise
    """
    return value == 0


def is_positive(value: int) -> bool:
    """
    Check if U256 value is positive.

    Args:
        value: U256 value

    Returns:
        True if positive, False otherwise
    """
    return value > 0


def max_u256(a: int, b: int) -> int:
    """
    Maximum of two U256 values.

    Args:
        a: First U256 value
        b: Second U256 value

    Returns:
        Maximum value
    """
    return max(a, b)


def min_u256(a: int, b: int) -> int:
    """
    Minimum of two U256 values.

    Args:
        a: First U256 value
        b: Second U256 value

    Returns:
        Minimum value
    """
    return min(a, b)


def clamp_u256(value: int, min_val: int, max_val: int) -> int:
    """
    Clamp U256 value between min and max.

    Args:
        value: Value to clamp
        min_val: Minimum value
        max_val: Maximum value

    Returns:
        Clamped value
    """
    return max(min_val, min(value, max_val))
