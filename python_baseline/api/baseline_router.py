"""
Baseline solver router.
"""

from fastapi import APIRouter, Depends
from python_baseline.models.auction import Auction
from python_baseline.models.solution import Solutions
from python_baseline.engines.baseline.engine import BaselineEngine
from python_baseline.infra.di import baseline_engine

router = APIRouter(prefix="/baseline", tags=["baseline"])


@router.post("/solve", response_model=Solutions)
async def solve(auction: Auction, engine: BaselineEngine = Depends(baseline_engine)):
    """
    Solve a CoW Protocol auction using the baseline solver.
    
    Args:
        auction: The auction to solve
        engine: The baseline solver engine
        
    Returns:
        Solutions object containing the solver's solutions
    """
    return await engine.solve(auction)
