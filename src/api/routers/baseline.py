"""
Baseline solver router.
"""
from fastapi import APIRouter, Depends
from src.domain.auction import Auction
from src.domain.solution import Solutions
from src.engines.baseline.engine import BaselineEngine
from src.infra.di import baseline_engine

router = APIRouter(prefix="/baseline", tags=["baseline"])

@router.post("/solve")
async def solve_baseline(
    auction: Auction, 
    engine: BaselineEngine = Depends(baseline_engine)
) -> Solutions:
    """Solve auction using baseline engine."""
    return await engine.solve(auction)
