"""
Base Token model for reference and utility.
This is a simplified version of the original token model.
"""
from __future__ import annotations

from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """Base token model for reference"""
    address: str  # H160 as string
    symbol: Optional[str] = None
    decimals: Optional[int] = None
    name: Optional[str] = None
    
    def __str__(self) -> str:
        return f"Token({self.symbol or 'Unknown'})"
    
    def __repr__(self) -> str:
        return f"Token(address={self.address}, symbol={self.symbol}, decimals={self.decimals})"
