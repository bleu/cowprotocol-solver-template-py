"""
Example: Basic Solver Implementation
This shows how to implement a simple solver using the new CoW Protocol models.
"""
from __future__ import annotations

from typing import List
from src.models.cow_auction import CowAuction
from src.models.cow_solution import Solutions, Solution, Trade


class BasicSolver:
    """
    Example solver that demonstrates how to work with CoW Protocol auctions.
    
    This is a template - implement your own solver logic here.
    """
    
    def __init__(self):
        self.name = "BasicSolver"
    
    def solve(self, auction: CowAuction) -> Solutions:
        """
        Solve a CoW Protocol auction.
        
        Args:
            auction: The auction to solve
            
        Returns:
            Solutions: List of solutions for the auction
        """
        print(f"🔍 {self.name}: Analyzing auction {auction.id}")
        print(f"   Orders: {len(auction.orders)}")
        print(f"   Tokens: {len(auction.tokens)}")
        print(f"   Liquidity: {len(auction.liquidity)}")
        
        # Example: Simple solver that creates one trade per order
        solutions = []
        
        for i, order in enumerate(auction.orders):
            if order.kind == "sell":
                # Create a simple trade
                trade = Trade(
                    order_uid=order.uid,
                    executed_amount=order.sell_amount,
                    fee=0  # No fee for simplicity
                )
                
                solution = Solution(
                    id=i,
                    prices={order.sell_token: "1", order.buy_token: "1"},  # Simple 1:1 pricing
                    trades=[trade],
                    interactions=[],
                    pre_interactions=[],
                    post_interactions=[]
                )
                
                solutions.append(solution)
        
        print(f"✅ {self.name}: Created {len(solutions)} solutions")
        return Solutions(solutions=solutions)


# Example usage:
if __name__ == "__main__":
    # This would be called from the /solve endpoint
    solver = BasicSolver()
    
    # Example auction (in real usage, this comes from the API)
    from src.models.cow_auction import CowAuction, Order, Token
    
    example_auction = CowAuction(
        id="example_auction",
        tokens={
            "0x1234...": Token(decimals=18, symbol="WETH"),
            "0x5678...": Token(decimals=6, symbol="USDC")
        },
        orders=[
            Order(
                uid="0xabcd...",
                sell_token="0x1234...",
                buy_token="0x5678...",
                sell_amount="1000000000000000000",  # 1 WETH
                buy_amount="2000000000"  # 2000 USDC
            )
        ],
        liquidity=[],
        effective_gas_price="20000000000",  # 20 gwei
        deadline="2025-09-16T20:00:00Z"
    )
    
    # Solve the auction
    solutions = solver.solve(example_auction)
    print(f"Generated {len(solutions.solutions)} solutions")
