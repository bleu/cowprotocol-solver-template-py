"""
Baseline solver engine implementation for CoW Protocol.
"""

import logging
from typing import List, Set, Optional

import networkx as nx

from src.domain.auction import Auction
from src.domain.solution import  Solutions
from src.domain.order import Order

from src.engines.baseline.cow_matcher import CowMatcher
from src.engines.baseline.pathfinder import PathFinder
from src.engines.baseline.solution_builder import SolutionBuilder
from src.utils.validation import validate_auction


class BaselineEngine:
    """
    Baseline solver engine implementation for CoW Protocol.
    
    Implements a two-phase solving approach:
    1. Find CoW (Coincidence of Wants) matches between orders
    2. Route remaining liquidity through AMM pools
    """
    
    def __init__(
        self,
        weth_address: str,
        base_tokens: List[str],
        max_hops: int = 2,
        max_partial_attempts: int = 5,
        solution_gas_offset: int = 50000,
        native_token_price_estimation_amount: str = "1000000000000000000"
    ):
        """Initialize baseline solver with configuration."""
        self.logger = logging.getLogger(__name__)
        
        # Store configuration
        self.weth_address = weth_address.lower()
        self.base_tokens: Set[str] = {token.lower() for token in base_tokens}
        self.max_hops = max_hops
        self.max_partial_attempts = max_partial_attempts
        self.solution_gas_offset = solution_gas_offset
        self.native_token_price_estimation_amount = int(native_token_price_estimation_amount)
        
        # Add WETH to base tokens if not present
        self.base_tokens.add(self.weth_address)
        
        # Initialize components
        self.cow_matcher = CowMatcher()
        self.path_finder = PathFinder(max_hops=max_hops)
        self.solution_builder = SolutionBuilder(solution_gas_offset=solution_gas_offset)
        
        self.logger.info(
            f"Initialized BaselineEngine: "
            f"chain={weth_address}, "
            f"base_tokens={len(self.base_tokens)}, "
            f"max_hops={max_hops}"
        )
    
    async def solve(self, auction: Auction) -> Solutions:
        """
        Solve auction using baseline algorithm.
        
        Steps:
        1. Find direct CoW matches
        2. Build liquidity graph from AMM pools
        3. Find paths for remaining orders
        4. Optimize prices
        5. Build final solution
        """
        if not validate_auction(auction):
            return Solutions(solutions=[])
            
        try:
            # Phase 1: Find CoW matches
            cow_trades = self.cow_matcher.find_matches(auction.orders)
            
            # Phase 2: Build liquidity graph
            graph = None
            if auction.liquidity:
                graph = self.path_finder.build_graph(auction.liquidity)
            
            # AMM routing will be implemented
            
            # Build prices (simplified - use reference prices)
            prices = {}
            for token_addr, token_info in auction.tokens.items():
                # Use reference price if available
                prices[token_addr.lower()] = 10**18  # Default 1:1 for now
            
            # Phase 5: Build solution
            solution = self.solution_builder.build_solution(
                auction_id=auction.id,
                trades=cow_trades,
                interactions=[],  # No AMM interactions yet
                prices=prices
            )
            
            return Solutions(solutions=[solution])
            
        except Exception as e:
            self.logger.error(f"Error solving auction: {e}")
            return Solutions(solutions=[])
    


class AmmRouter:
    """Routes orders through AMM liquidity pools."""
    
    def __init__(self, max_hops: int = 2):
        self.max_hops = max_hops
        self.logger = logging.getLogger(__name__)
    
    def find_path(
        self,
        order: Order,
        graph: nx.DiGraph,
        base_tokens: Set[str]
    ) -> Optional[List[str]]:
        """
        Find optimal trading path for an order.
        
        Uses BFS with max_hops constraint.
        """
        sell_token = order.sell_token.lower()
        buy_token = order.buy_token.lower()
        
        # Try direct path first
        if graph.has_edge(sell_token, buy_token):
            return [sell_token, buy_token]
        
        # Find paths through base tokens
        for base_token in base_tokens:
            if base_token == sell_token or base_token == buy_token:
                continue
                
            path = self._find_path_through_base(
                graph, sell_token, buy_token, base_token
            )
            if path and len(path) - 1 <= self.max_hops:
                return path
        
        # BFS for any valid path
        try:
            paths = list(nx.all_simple_paths(
                graph, sell_token, buy_token,
                cutoff=self.max_hops + 1
            ))
            if paths:
                # Return shortest path
                return min(paths, key=len)
        except nx.NetworkXNoPath:
            pass
        
        return None
    
    def _find_path_through_base(
        self,
        graph: nx.DiGraph,
        sell_token: str,
        buy_token: str,
        base_token: str
    ) -> Optional[List[str]]:
        """Find path through a specific base token."""
        if (graph.has_edge(sell_token, base_token) and 
            graph.has_edge(base_token, buy_token)):
            return [sell_token, base_token, buy_token]
        return None

