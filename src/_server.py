"""
This is the project's Entry point.
"""
from __future__ import annotations

import argparse
import decimal
import logging

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from pydantic import BaseSettings

from src.models.cow_auction import CowAuction
from src.models.cow_solution import Solutions

# Set decimal precision.
decimal.getcontext().prec = 100

# Holds parameters passed on the command line when invoking the server.
# These will be merged with request solver parameters
SERVER_ARGS = None


# ++++ Interface definition ++++


# Server settings: Can be overridden by passing them as env vars or in a .env file.
# Example: PORT=8001 python -m src._server
class ServerSettings(BaseSettings):
    """Basic Server Settings"""

    host: str = "0.0.0.0"
    port: int = 8080


server_settings = ServerSettings()

# ++++ Endpoints: ++++


app = FastAPI(title="Batch auction solver")
app.add_middleware(GZipMiddleware)


@app.get("/health", status_code=200)
def health() -> bool:
    """Convenience endpoint to check if server is alive."""
    return True


@app.post("/notify", response_model=bool)
async def notify(request: Request) -> bool:
    """Print response from notify endpoint."""
    print(f"Notify request {await request.json()}")
    return True


@app.post("/solve", response_model=Solutions)
async def solve(problem: CowAuction, request: Request):  # type: ignore
    """API POST solve endpoint handler"""
    from datetime import datetime

    print("\n" + "=" * 80)
    print("🎯 RECEIVED NEW COW PROTOCOL AUCTION")
    print("=" * 80)
    print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📋 Auction ID: {problem.id}")
    print(f"⛽ Gas Price: {problem.effective_gas_price}")
    print(f"⏰ Deadline: {problem.deadline}")

    print(f"\n📊 AUCTION STATISTICS:")
    print(f"   - Total Orders: {len(problem.orders)}")
    print(f"   - Total Tokens: {len(problem.tokens)}")
    print(f"   - Total Liquidity: {len(problem.liquidity)}")

    # Print token details with addresses
    if problem.tokens:
        print(f"\n🪙 TOKENS ({len(problem.tokens)}):")
        for i, (address, token) in enumerate(problem.tokens.items()):
            if i < 5:  # Show first 5 tokens
                decimals = token.decimals if token.decimals else 'unknown'
                symbol = token.symbol if token.symbol else 'unknown'
                print(f"   {i+1}. {address[:10]}... (decimals: {decimals}, symbol: {symbol})")
            elif i == 5:
                print(f"   ... and {len(problem.tokens) - 5} more tokens")

    # Print order details
    if problem.orders:
        print(f"\n📝 ORDERS ({len(problem.orders)}):")
        for i, order in enumerate(problem.orders):
            if i < 3:  # Show first 3 orders
                order_type = "Sell" if order.kind == "sell" else "Buy"
                sell_token = order.sell_token[:10] if order.sell_token else 'unknown'
                buy_token = order.buy_token[:10] if order.buy_token else 'unknown'
                print(f"   {i+1}. {order_type} Order: {order.uid[:10]}...")
                print(f"      Sell Token: {sell_token}... -> Buy Token: {buy_token}...")
                print(f"      Sell Amount: {order.sell_amount}")
                print(f"      Buy Amount: {order.buy_amount}")
            elif i == 3:
                print(f"   ... and {len(problem.orders) - 3} more orders")

    # Print liquidity if present
    if problem.liquidity:
        print(f"\n💱 LIQUIDITY ({len(problem.liquidity)}):")
        for i, liquidity in enumerate(problem.liquidity):
            if i < 2:
                liquidity_type = "Unknown"
                if liquidity.constant_product:
                    liquidity_type = "Constant Product"
                elif liquidity.weighted_product:
                    liquidity_type = "Weighted Product"
                elif liquidity.stable:
                    liquidity_type = "Stable"
                elif liquidity.concentrated_liquidity:
                    liquidity_type = "Concentrated Liquidity"
                elif liquidity.limit_order:
                    liquidity_type = "Limit Order"
                print(f"   {i+1}. {liquidity_type}")
            elif i == 2:
                print(f"   ... and {len(problem.liquidity) - 2} more liquidity sources")

    print("=" * 80)

    # TODO: Implement actual solver logic here
    # For now, return an empty solution
    simple_solution = Solutions(
        solutions=[]
    )

    print("\n\n*************\n\nReturning empty solution (no trades)")
    return simple_solution


# ++++ Server setup: ++++


if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser(
        fromfile_prefix_chars="@",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    # TODO - enable flag to write files to persistent storage
    # parser.add_argument(
    #     "--write_auxiliary_files",
    #     type=bool,
    #     default=False,
    #     help="Write auxiliary instance and optimization files, or not.",
    # )

    parser.add_argument(
        "--log-level",
        type=str,
        default="info",
        help="Log level",
    )

    SERVER_ARGS = parser.parse_args()
    uvicorn.run(
        "__main__:app",
        host=server_settings.host,
        port=server_settings.port,
        log_level=SERVER_ARGS.log_level,
    )
