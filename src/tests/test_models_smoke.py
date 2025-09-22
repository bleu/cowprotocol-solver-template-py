"""
Smoke tests for model validation.

This module contains basic tests to ensure models can be instantiated and validated.
"""

import pytest
from decimal import Decimal
from src.models.auction import Auction, Token, Order, Liquidity
from src.models.order import Order as OrderModel
from src.models.solution import Solution, Solutions, Trade
from src.models.liquidity import Liquidity as LiquidityModel


class TestAuctionModel:
    """Test auction model validation."""
    
    def test_auction_creation(self):
        """Test basic auction creation."""
        auction = Auction(
            id="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            tokens={
                "0x1234567890123456789012345678901234567890": Token(
                    decimals=18,
                    symbol="WETH",
                    reference_price=2000000000000000000000,
                    reference_price_denominator=1000000000000000000
                )
            },
            orders=[
                Order(
                    uid="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
                    sell_token="0x1234567890123456789012345678901234567890",
                    buy_token="0x0987654321098765432109876543210987654321",
                    sell_amount=1000000000000000000,
                    buy_amount=2000000000000000000000,
                    fee_amount=1000000000000000,
                    kind="sell",
                    partially_fillable=False,
                    **{"class": "market"},
                    signature="0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
                    app_data="0x0000000000000000000000000000000000000000000000000000000000000000"
                )
            ],
            liquidity=[],
            effective_gas_price=20000000000,
            deadline="2024-12-19T12:00:00Z"
        )
        
        assert auction.id == "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
        assert len(auction.tokens) == 1
        assert len(auction.orders) == 1
        assert len(auction.liquidity) == 0
    
    def test_auction_validation_empty_orders(self):
        """Test auction validation with empty orders."""
        with pytest.raises(ValueError, match="orders cannot be empty"):
            Auction(
                id="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
                tokens={
                    "0x1234567890123456789012345678901234567890": Token(
                        decimals=18,
                        symbol="WETH"
                    )
                },
                orders=[],
                liquidity=[],
                effective_gas_price=20000000000,
                deadline="2024-12-19T12:00:00Z"
            )
    
    def test_auction_validation_empty_tokens(self):
        """Test auction validation with empty tokens."""
        with pytest.raises(Exception):  # Pydantic validation error
            Auction(
                id="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
                tokens={},
                orders=[
                Order(
                    uid="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
                    sell_token="0x1234567890123456789012345678901234567890",
                    buy_token="0x0987654321098765432109876543210987654321",
                    sell_amount=1000000000000000000,
                    buy_amount=2000000000000000000000,
                    fee_amount=1000000000000000,
                    kind="sell",
                    partially_fillable=False,
                    **{"class": "market"},
                    signature="0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
                    app_data="0x0000000000000000000000000000000000000000000000000000000000000000"
                )
                ],
                liquidity=[],
                effective_gas_price=20000000000,
                deadline="2024-12-19T12:00:00Z"
            )


class TestSolutionModel:
    """Test solution model validation."""
    
    def test_solution_creation(self):
        """Test basic solution creation."""
        solution = Solution(
            id="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            trades=[
                Trade(
                    order_uid="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
                    sell_token="0x1234567890123456789012345678901234567890",
                    buy_token="0x0987654321098765432109876543210987654321",
                    sell_amount=1000000000000000000,
                    buy_amount=2000000000000000000000,
                    fee_amount=1000000000000000
                )
            ],
            prices={
                "0x1234567890123456789012345678901234567890": 2000000000000000000000,
                "0x0987654321098765432109876543210987654321": 1000000000000000000
            },
            interactions=[]
        )
        
        assert solution.id == "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
        assert len(solution.trades) == 1
        assert len(solution.prices) == 2
        assert len(solution.interactions) == 0
    
    def test_solutions_creation(self):
        """Test solutions collection creation."""
        solution = Solution(
            id="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            trades=[],
            prices={},
            interactions=[]
        )
        
        solutions = Solutions(solutions=[solution])
        
        assert len(solutions.solutions) == 1
        assert solutions.solutions[0].id == "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"


class TestOrderModel:
    """Test order model validation."""
    
    def test_order_creation(self):
        """Test basic order creation."""
        order = OrderModel(
            uid="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            sell_token="0x1234567890123456789012345678901234567890",
            buy_token="0x0987654321098765432109876543210987654321",
            sell_amount=1000000000000000000,
            buy_amount=2000000000000000000000,
            fee_amount=1000000000000000,
            kind="sell",
            partially_fillable=False,
            **{"class": "market"},
            signature="0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
            app_data="0x0000000000000000000000000000000000000000000000000000000000000000"
        )
        
        assert order.uid == "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
        assert order.sell_token == "0x1234567890123456789012345678901234567890"
        assert order.buy_token == "0x0987654321098765432109876543210987654321"
        assert order.kind == "sell"
        assert order.class_ == "market"
    
    def test_order_validation_invalid_kind(self):
        """Test order validation with invalid kind."""
        with pytest.raises(Exception):  # Pydantic validation error
            OrderModel(
                uid="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
                sell_token="0x1234567890123456789012345678901234567890",
                buy_token="0x0987654321098765432109876543210987654321",
                sell_amount=1000000000000000000,
                buy_amount=2000000000000000000000,
                fee_amount=1000000000000000,
                kind="invalid",
                partially_fillable=False,
                **{"class": "market"},
                signature="0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
                app_data="0x0000000000000000000000000000000000000000000000000000000000000000"
            )
    
    def test_order_validation_invalid_uid(self):
        """Test order validation with invalid UID."""
        with pytest.raises(ValueError, match="uid must start with 0x"):
            OrderModel(
                uid="invalid_uid",
                sell_token="0x1234567890123456789012345678901234567890",
                buy_token="0x0987654321098765432109876543210987654321",
                sell_amount=1000000000000000000,
                buy_amount=2000000000000000000000,
                fee_amount=1000000000000000,
                kind="sell",
                partially_fillable=False,
                **{"class": "market"},
                signature="0xabcdef1234567890abcdef1234567890abcdef1234567890abcdef1234567890",
                app_data="0x0000000000000000000000000000000000000000000000000000000000000000"
            )


class TestLiquidityModel:
    """Test liquidity model validation."""
    
    def test_liquidity_creation(self):
        """Test basic liquidity creation."""
        liquidity = LiquidityModel(
            id="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
            kind="constant_product",
            tokens={
                "0x1234567890123456789012345678901234567890": 1000000000000000000000,
                "0x0987654321098765432109876543210987654321": 2000000000000000000000
            }
        )
        
        assert liquidity.id == "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef"
        assert liquidity.kind == "constant_product"
        assert len(liquidity.tokens) == 2
    
    def test_liquidity_validation_invalid_kind(self):
        """Test liquidity validation with invalid kind."""
        with pytest.raises(Exception):  # Pydantic validation error
            LiquidityModel(
                id="0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
                kind="invalid",
                tokens={
                    "0x1234567890123456789012345678901234567890": 1000000000000000000000
                }
            )
