"""
Solution domain model for CoW Protocol.

This module contains the Solution model and related types.
"""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field
from .common import Address, U256


class Trade(BaseModel):
    """Trade in a solution."""
    
    order_uid: str = Field(..., description="Order identifier")
    sell_token: Address = Field(..., description="Token to sell")
    buy_token: Address = Field(..., description="Token to buy")
    sell_amount: U256 = Field(..., description="Amount to sell in wei")
    buy_amount: U256 = Field(..., description="Amount to buy in wei")
    fee_amount: U256 = Field(..., description="Fee amount in wei")


class Fulfillment(BaseModel):
    """Order fulfillment."""
    
    order_uid: str = Field(..., description="Order identifier")
    executed_amount: U256 = Field(..., description="Executed amount in wei")


class Fee(BaseModel):
    """Fee information."""
    
    token: Address = Field(..., description="Fee token")
    amount: U256 = Field(..., description="Fee amount in wei")


class JitTrade(BaseModel):
    """Just-in-time trade."""
    
    order_uid: str = Field(..., description="JIT order identifier")
    sell_token: Address = Field(..., description="Token to sell")
    buy_token: Address = Field(..., description="Token to buy")
    sell_amount: U256 = Field(..., description="Amount to sell in wei")
    buy_amount: U256 = Field(..., description="Amount to buy in wei")
    fee_amount: U256 = Field(..., description="Fee amount in wei")


class Interaction(BaseModel):
    """Smart contract interaction."""
    
    target: Address = Field(..., description="Target contract address")
    value: U256 = Field(..., description="ETH value to send")
    call_data: str = Field(..., description="Call data")


class LiquidityInteraction(BaseModel):
    """Liquidity source interaction."""
    
    liquidity_id: str = Field(..., description="Liquidity source identifier")
    interaction: Interaction = Field(..., description="Interaction details")


class CustomInteraction(BaseModel):
    """Custom interaction."""
    
    interaction: Interaction = Field(..., description="Interaction details")


class Allowance(BaseModel):
    """Token allowance."""
    
    token: Address = Field(..., description="Token address")
    spender: Address = Field(..., description="Spender address")
    amount: U256 = Field(..., description="Allowance amount in wei")


class ClearingPrices(BaseModel):
    """Clearing prices for tokens."""
    
    prices: Dict[Address, U256] = Field(..., description="Token prices in wei")


class Single(BaseModel):
    """Single solution."""
    
    id: int = Field(..., description="Solution identifier")
    trades: List[Trade] = Field(..., description="Trades in the solution")
    prices: Dict[Address, U256] = Field(..., description="Clearing prices")
    interactions: List[Interaction] = Field(..., description="Smart contract interactions")
    fulfillments: List[Fulfillment] = Field(default_factory=list, description="Order fulfillments")
    fees: List[Fee] = Field(default_factory=list, description="Fees")
    jit_trades: List[JitTrade] = Field(default_factory=list, description="JIT trades")
    liquidity_interactions: List[LiquidityInteraction] = Field(default_factory=list, description="Liquidity interactions")
    custom_interactions: List[CustomInteraction] = Field(default_factory=list, description="Custom interactions")
    allowances: List[Allowance] = Field(default_factory=list, description="Token allowances")


class Solution(BaseModel):
    """CoW Protocol solution."""
    
    id: int = Field(..., description="Solution identifier")
    trades: List[Trade] = Field(..., description="Trades in the solution")
    prices: Dict[Address, U256] = Field(..., description="Clearing prices")
    interactions: List[Interaction] = Field(..., description="Smart contract interactions")
    fulfillments: List[Fulfillment] = Field(default_factory=list, description="Order fulfillments")
    fees: List[Fee] = Field(default_factory=list, description="Fees")
    jit_trades: List[JitTrade] = Field(default_factory=list, description="JIT trades")
    liquidity_interactions: List[LiquidityInteraction] = Field(default_factory=list, description="Liquidity interactions")
    custom_interactions: List[CustomInteraction] = Field(default_factory=list, description="Custom interactions")
    allowances: List[Allowance] = Field(default_factory=list, description="Token allowances")
    
    model_config = {
        "json_encoders": {
            U256: str  # convert U256 to string automatically
        }
    }


class Solutions(BaseModel):
    """Collection of solutions."""
    
    solutions: List[Solution] = Field(..., description="List of solutions")
