"""
Baseline solver router.
"""

import logging
from fastapi import APIRouter, Depends
from src.domain.auction import Auction
from src.domain.solution import Solutions
from src.engines.baseline.engine import BaselineEngine
from src.infra.di import baseline_engine

router = APIRouter(prefix="/baseline", tags=["baseline"])
logger = logging.getLogger(__name__)


@router.post("/solve")
async def solve_baseline(
    auction: Auction, engine: BaselineEngine = Depends(baseline_engine)
) -> Solutions:
    """Solve auction using baseline engine."""

    result = await engine.solve(auction)

    logger.info(f"BASELINE SOLVER - SOLUTION:")
    logger.info(f" -> AUCTION ID: {auction.id}")
    logger.info(f" -> SOLUTIONS: {len(result.solutions)}")
    logger.info(f"===================================")

    return result


@router.post("/notify")
async def notify_baseline(
    notification: dict,
) -> dict:
    """Handle solver notifications."""
    logger.info(f"BASELINE NOTIFY:\n {notification}")
    logger.info(f"===================================")
    # For now, just acknowledge the notification
    # In a real implementation, this might trigger something
    return {"status": "acknowledged"}
