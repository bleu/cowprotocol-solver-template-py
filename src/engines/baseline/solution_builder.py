"""
Solution builder for creating valid settlement solutions.

Constructs the final solution with trades, interactions, and prices.
"""

from typing import List, Dict, Optional
from src.domain.solution import Solution, Trade, Interaction


class SolutionBuilder:
    """
    Builds valid solutions for the settlement contract.
    
    Formats trades, interactions, and prices according to the protocol.
    """
    
    def __init__(self, solution_gas_offset: int = 50000):
        self.solution_gas_offset = solution_gas_offset
        self.logger = __import__('logging').getLogger(__name__)
    
    def build_solution(
        self,
        auction_id: str,
        trades: List[Trade],
        interactions: List[Interaction],
        prices: Dict[str, int]
    ) -> Solution:
        """
        Build a complete solution.
        
        Args:
            auction_id: Auction identifier
            trades: List of executed trades
            interactions: List of AMM interactions
            prices: Clearing prices for all tokens
            
        Returns:
            Complete Solution object
        """
        # Ensure all traded tokens have prices
        for trade in trades:
            if trade.sell_token.lower() not in prices:
                prices[trade.sell_token.lower()] = 10**18  # Default price
            if trade.buy_token.lower() not in prices:
                prices[trade.buy_token.lower()] = 10**18  # Default price
        
        # Calculate solution ID (can be auction block number or unique ID)
        solution_id = self._generate_solution_id(auction_id)
        
        # Build the solution
        solution = Solution(
            id=solution_id,
            trades=trades,
            interactions=interactions,
            prices=prices
        )
        
        # Log solution details
        self.logger.info(
            f"Built solution {solution_id} with {len(trades)} trades, "
            f"{len(interactions)} interactions, {len(prices)} token prices"
        )
        
        return solution
    
    def _generate_solution_id(self, auction_id: str) -> int:
        """
        Generate a unique solution ID.
        
        In production, this would be the block number or a unique identifier.
        """
        # Simple hash-based ID for now
        return abs(hash(auction_id)) % (10**9)
    
    def validate_solution(self, solution: Solution) -> bool:
        """
        Validate that a solution is well-formed.
        
        Args:
            solution: Solution to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Check basic requirements
        if not solution.prices:
            self.logger.error("Solution has no prices")
            return False
        
        # Check all trades have prices
        for trade in solution.trades:
            if trade.sell_token.lower() not in solution.prices:
                self.logger.error(f"No price for sell token {trade.sell_token}")
                return False
            if trade.buy_token.lower() not in solution.prices:
                self.logger.error(f"No price for buy token {trade.buy_token}")
                return False
        
        # Validate interactions
        for interaction in solution.interactions:
            if not interaction.target:
                self.logger.error("Interaction missing target")
                return False
            if not interaction.call_data:
                self.logger.error("Interaction missing call data")
                return False
        
        return True