"""
CoW Protocol Auction models that match the solvers_dto structure.
"""
from __future__ import annotations

from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field
from decimal import Decimal


class Token(BaseModel):
    """Token information matching solvers_dto::auction::Token"""
    decimals: Optional[int] = None
    symbol: Optional[str] = None
    reference_price: Optional[Decimal] = None
    available_balance: str = "0"  # U256 as string
    trusted: bool = False


class FeePolicy(BaseModel):
    """Fee policy matching solvers_dto::auction::FeePolicy"""
    volume: Optional[Decimal] = None
    price: Optional[Decimal] = None


class InteractionData(BaseModel):
    """Interaction data matching solvers_dto::auction::InteractionData"""
    target: str  # H160 as string
    value: str = "0"  # U256 as string
    call_data: str = "0x"  # bytes as hex string


class FlashloanHint(BaseModel):
    """Flashloan hint matching solvers_dto::auction::FlashloanHint"""
    lender: str  # H160 as string
    borrower: str  # H160 as string
    token: str  # H160 as string
    amount: str = "0"  # U256 as string


class Order(BaseModel):
    """Order matching solvers_dto::auction::Order"""
    uid: str  # [u8; 56] as hex string
    sell_token: str = Field(alias="sellToken")  # H160 as string
    buy_token: str = Field(alias="buyToken")  # H160 as string
    sell_amount: str = Field(default="0", alias="sellAmount")  # U256 as string
    full_sell_amount: str = Field(default="0", alias="fullSellAmount")  # U256 as string
    buy_amount: str = Field(default="0", alias="buyAmount")  # U256 as string
    full_buy_amount: str = Field(default="0", alias="fullBuyAmount")  # U256 as string
    valid_to: int = Field(default=0, alias="validTo")
    kind: str = "sell"  # "sell" or "buy"
    receiver: Optional[str] = None  # H160 as string
    owner: str = "0x0000000000000000000000000000000000000000"  # H160 as string
    partially_fillable: bool = Field(default=False, alias="partiallyFillable")
    pre_interactions: List[InteractionData] = Field(default=[], alias="preInteractions")
    post_interactions: List[InteractionData] = Field(default=[], alias="postInteractions")
    sell_token_source: str = Field(default="erc20", alias="sellTokenSource")  # "erc20", "external", "internal"
    buy_token_destination: str = Field(default="erc20", alias="buyTokenDestination")  # "erc20", "internal"
    class_: str = "market"  # "market" or "limit"
    app_data: str = Field(default="0x0000000000000000000000000000000000000000000000000000000000000000", alias="appData")  # AppDataHash as hex
    signing_scheme: str = Field(default="eip712", alias="signingScheme")  # "eip712", "ethsign", "presign", "eip1271"
    signature: str = "0x"  # bytes as hex string
    
    class Config:
        allow_population_by_field_name = True


class ConstantProductReserve(BaseModel):
    """Constant product reserve matching solvers_dto::auction::ConstantProductReserve"""
    token: str  # H160 as string
    balance: str = "0"  # U256 as string


class ConstantProductPool(BaseModel):
    """Constant product pool matching solvers_dto::auction::ConstantProductPool"""
    reserves: List[ConstantProductReserve] = []
    fee: str = "0.003"  # Decimal as string
    cost: Optional[InteractionData] = None


class WeightedProductReserve(BaseModel):
    """Weighted product reserve matching solvers_dto::auction::WeightedProductReserve"""
    token: str  # H160 as string
    balance: str = "0"  # U256 as string
    weight: str = "0.5"  # Decimal as string


class WeightedProductPool(BaseModel):
    """Weighted product pool matching solvers_dto::auction::WeightedProductPool"""
    reserves: List[WeightedProductReserve] = []
    fee: str = "0.003"  # Decimal as string
    cost: Optional[InteractionData] = None


class StableReserve(BaseModel):
    """Stable reserve matching solvers_dto::auction::StableReserve"""
    token: str  # H160 as string
    balance: str = "0"  # U256 as string


class StablePool(BaseModel):
    """Stable pool matching solvers_dto::auction::StablePool"""
    reserves: List[StableReserve] = []
    fee: str = "0.003"  # Decimal as string
    cost: Optional[InteractionData] = None


class ConcentratedLiquidityReserve(BaseModel):
    """Concentrated liquidity reserve matching solvers_dto::auction::ConcentratedLiquidityReserve"""
    token: str  # H160 as string
    balance: str = "0"  # U256 as string


class ConcentratedLiquidityPool(BaseModel):
    """Concentrated liquidity pool matching solvers_dto::auction::ConcentratedLiquidityPool"""
    reserves: List[ConcentratedLiquidityReserve] = []
    fee: str = "0.003"  # Decimal as string
    cost: Optional[InteractionData] = None


class LimitOrder(BaseModel):
    """Limit order matching solvers_dto::auction::LimitOrder"""
    order: Order
    cost: Optional[InteractionData] = None


class Liquidity(BaseModel):
    """Liquidity matching solvers_dto::auction::Liquidity"""
    constant_product: Optional[ConstantProductPool] = None
    weighted_product: Optional[WeightedProductPool] = None
    stable: Optional[StablePool] = None
    concentrated_liquidity: Optional[ConcentratedLiquidityPool] = None
    limit_order: Optional[LimitOrder] = None


class CowAuction(BaseModel):
    """Auction matching solvers_dto::auction::Auction"""
    id: Optional[str] = None  # String, not int
    tokens: Dict[str, Token] = {}  # H160 -> Token
    orders: List[Order] = []
    liquidity: List[Liquidity] = []
    effective_gas_price: str = Field(default="0", alias="effectiveGasPrice")  # U256 as string
    deadline: str = ""  # DateTime as ISO string
    surplus_capturing_jit_order_owners: List[str] = Field(default=[], alias="surplusCapturingJitOrderOwners")  # List of H160 as strings
    
    class Config:
        allow_population_by_field_name = True
