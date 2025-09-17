"""
CoW Protocol Solution models that match the solvers_dto structure.
"""
from __future__ import annotations

from typing import Dict, List, Optional
from pydantic import BaseModel


class OrderUid(BaseModel):
    """Order UID matching solvers_dto::solution::OrderUid"""
    uid: str  # [u8; 56] as hex string


class Fulfillment(BaseModel):
    """Fulfillment matching solvers_dto::solution::Fulfillment"""
    order: OrderUid
    executed_amount: str = "0"  # U256 as string
    fee: Optional[str] = None  # U256 as string


class JitOrder(BaseModel):
    """JIT Order matching solvers_dto::solution::JitOrder"""
    sell_token: str  # H160 as string
    buy_token: str  # H160 as string
    receiver: str  # H160 as string
    sell_amount: str = "0"  # U256 as string
    buy_amount: str = "0"  # U256 as string
    partially_fillable: bool = False
    valid_to: int = 0
    app_data: str = "0x0000000000000000000000000000000000000000000000000000000000000000"  # AppDataHash as hex
    kind: str = "sell"  # "sell" or "buy"
    sell_token_balance: str = "erc20"  # "erc20", "internal", "external"
    buy_token_balance: str = "erc20"  # "erc20", "internal"
    signing_scheme: str = "eip712"  # "eip712", "ethsign", "presign", "eip1271"
    signature: str = "0x"  # bytes as hex string


class JitTrade(BaseModel):
    """JIT Trade matching solvers_dto::solution::JitTrade"""
    order: JitOrder
    executed_amount: str = "0"  # U256 as string
    fee: Optional[str] = None  # U256 as string


class Trade(BaseModel):
    """Trade matching solvers_dto::solution::Trade"""
    kind: str  # "fulfillment" or "jit"
    fulfillment: Optional[Fulfillment] = None
    jit: Optional[JitTrade] = None


class Call(BaseModel):
    """Call matching solvers_dto::solution::Call"""
    target: str  # H160 as string
    value: str = "0"  # U256 as string
    call_data: str = "0x"  # bytes as hex string


class LiquidityInteraction(BaseModel):
    """Liquidity interaction matching solvers_dto::solution::LiquidityInteraction"""
    target: str  # H160 as string
    value: str = "0"  # U256 as string
    call_data: str = "0x"  # bytes as hex string
    input: str = "0"  # U256 as string
    output: str = "0"  # U256 as string
    internalize: bool = False


class CustomInteraction(BaseModel):
    """Custom interaction matching solvers_dto::solution::CustomInteraction"""
    target: str  # H160 as string
    value: str = "0"  # U256 as string
    call_data: str = "0x"  # bytes as hex string
    inputs: List[str] = []  # List of U256 as strings
    outputs: List[str] = []  # List of U256 as strings
    internalize: bool = False


class Interaction(BaseModel):
    """Interaction matching solvers_dto::solution::Interaction"""
    kind: str  # "liquidity" or "custom"
    liquidity: Optional[LiquidityInteraction] = None
    custom: Optional[CustomInteraction] = None


class Flashloan(BaseModel):
    """Flashloan matching solvers_dto::solution::Flashloan"""
    token: str  # H160 as string
    amount: str = "0"  # U256 as string


class Solution(BaseModel):
    """Solution matching solvers_dto::solution::Solution"""
    id: int = 1
    prices: Dict[str, str] = {}  # H160 -> U256 as string
    trades: List[Trade] = []
    pre_interactions: List[Call] = []
    interactions: List[Interaction] = []
    post_interactions: List[Call] = []
    gas: Optional[int] = None
    flashloans: Optional[Dict[str, Flashloan]] = None  # OrderUid -> Flashloan


class Solutions(BaseModel):
    """Solutions matching solvers_dto::solution::Solutions"""
    solutions: List[Solution] = []
