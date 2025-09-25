"""
Price finder for calculating clearing prices.

Determines uniform clearing prices for all tokens based on
executed trades and reference prices.

Based on the Rust baseline solver implementation.
"""

from typing import Dict, List, Optional
from decimal import Decimal
from collections import defaultdict
import logging

try:
    import networkx as nx
except ImportError:
    nx = None

from src.domain.solution import Trade


class PriceFinder:
    """
    Calculates uniform clearing prices for settlements.

    Implements price finding logic similar to the Rust baseline solver,
    ensuring all trades clear at consistent prices.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def find_clearing_prices(
        self,
        trades: List[Trade],
        reference_prices: Optional[Dict[str, int]] = None,
        base_token: Optional[str] = None,
    ) -> Dict[str, int]:
        """
        Calculate uniform clearing prices for all tokens.

        Args:
            trades: List of executed trades
            reference_prices: Optional reference prices from auction
            base_token: Optional base token for price normalization (e.g., WETH)

        Returns:
            Dictionary mapping token addresses to prices in wei
        """
        if not trades and not reference_prices:
            return {}

        # Start with reference prices if available
        prices = {}
        if reference_prices:
            prices = {k.lower(): int(v) for k, v in reference_prices.items()}

        # If no trades, return reference prices
        if not trades:
            return prices

        # Build price graph from trades
        if nx:
            price_graph = self._build_price_graph(trades)

            # Find connected components
            components = list(nx.connected_components(price_graph.to_undirected()))

            # Process each component
            for component in components:
                # Find anchor token (prefer base token or highest liquidity)
                anchor = self._find_anchor_token(component, base_token, prices)

                if anchor and anchor in prices:
                    # Propagate prices from anchor
                    component_prices = self._propagate_prices(
                        price_graph, anchor, prices[anchor]
                    )
                    prices.update(component_prices)
                else:
                    # No anchor, use relative pricing
                    component_prices = self._calculate_relative_prices(
                        price_graph, component, trades
                    )
                    prices.update(component_prices)
        else:
            # Fallback without networkx
            prices = self._calculate_prices_simple(trades, prices, base_token)

        # Normalize prices to ensure they're positive integers
        prices = self._normalize_prices(prices)

        self.logger.info(f"Calculated prices for {len(prices)} tokens")
        return prices

    def _build_price_graph(self, trades: List[Trade]):
        """
        Build a directed graph representing price relationships.

        Each edge represents a trade and stores the exchange rate.
        """
        if not nx:
            return None

        graph = nx.DiGraph()

        for trade in trades:
            sell_token = trade.sell_token.lower()
            buy_token = trade.buy_token.lower()

            sell_amount = int(trade.sell_amount)
            buy_amount = int(trade.buy_amount)

            if sell_amount > 0:
                # Add edge with exchange rate
                rate = Decimal(buy_amount) / Decimal(sell_amount)

                # Add bidirectional edges with rates
                graph.add_edge(
                    sell_token, buy_token, rate=rate, trade_id=trade.order_uid
                )
                graph.add_edge(
                    buy_token,
                    sell_token,
                    rate=Decimal(1) / rate,
                    trade_id=trade.order_uid,
                )

        return graph

    def _find_anchor_token(
        self, component: set, base_token: Optional[str], existing_prices: Dict[str, int]
    ) -> Optional[str]:
        """
        Find the best anchor token for price propagation.

        Priority:
        1. Base token if in component
        2. Token with existing price
        3. Token with most connections
        """
        # Check if base token is in component
        if base_token and base_token.lower() in component:
            return base_token.lower()

        # Check for tokens with existing prices
        for token in component:
            if token in existing_prices:
                return token

        # Return token with most connections (highest liquidity)
        # This would need the graph to determine connections
        return next(iter(component)) if component else None

    def _propagate_prices(
        self, graph, anchor: str, anchor_price: int
    ) -> Dict[str, int]:
        """
        Propagate prices from anchor token using exchange rates.

        Uses BFS to propagate prices through the graph.
        """
        prices = {anchor: anchor_price}
        visited = {anchor}
        queue = [anchor]

        while queue:
            current = queue.pop(0)
            current_price = prices[current]

            # Check all neighbors
            for neighbor in graph.neighbors(current):
                if neighbor not in visited:
                    # Calculate price based on exchange rate
                    edge_data = graph.get_edge_data(current, neighbor)
                    rate = edge_data["rate"]

                    neighbor_price = int(Decimal(current_price) * rate)
                    prices[neighbor] = neighbor_price

                    visited.add(neighbor)
                    queue.append(neighbor)

        return prices

    def _calculate_relative_prices(
        self, graph, component: set, trades: List[Trade]
    ) -> Dict[str, int]:
        """
        Calculate relative prices when no anchor is available.

        Sets one token to a base price and calculates others relative to it.
        """
        # Pick arbitrary token as base
        base_token = next(iter(component))
        base_price = 10**18  # 1 token in wei

        # Use propagation from this base
        return self._propagate_prices(graph, base_token, base_price)

    def _calculate_prices_simple(
        self,
        trades: List[Trade],
        existing_prices: Dict[str, int],
        base_token: Optional[str],
    ) -> Dict[str, int]:
        """
        Simple price calculation without networkx dependency.

        Fallback method for environments without networkx.
        """
        prices = existing_prices.copy()

        # Set base token price if not set
        if base_token and base_token.lower() not in prices:
            prices[base_token.lower()] = 10**18

        # Calculate prices from trades
        for trade in trades:
            sell_token = trade.sell_token.lower()
            buy_token = trade.buy_token.lower()

            sell_amount = int(trade.sell_amount)
            buy_amount = int(trade.buy_amount)

            if sell_amount > 0 and buy_amount > 0:
                # If we have price for one token, calculate the other
                if sell_token in prices and buy_token not in prices:
                    # Calculate buy token price
                    sell_price = prices[sell_token]
                    buy_price = (sell_price * sell_amount) // buy_amount
                    prices[buy_token] = buy_price
                elif buy_token in prices and sell_token not in prices:
                    # Calculate sell token price
                    buy_price = prices[buy_token]
                    sell_price = (buy_price * buy_amount) // sell_amount
                    prices[sell_token] = sell_price

        return prices

    def _normalize_prices(self, prices: Dict[str, int]) -> Dict[str, int]:
        """
        Normalize prices to ensure they're positive integers.

        Also handles very small or very large prices.
        """
        if not prices:
            return {}

        normalized = {}

        for token, price in prices.items():
            # Ensure price is positive
            if price <= 0:
                price = 1

            # Cap extremely large prices
            max_price = 10**30  # Maximum reasonable price
            if price > max_price:
                price = max_price

            normalized[token] = int(price)

        return normalized
