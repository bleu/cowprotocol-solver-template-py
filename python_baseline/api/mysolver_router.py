"""
MySolver router.
"""

from fastapi import APIRouter, Depends
from python_baseline.models.auction import Auction
from python_baseline.models.solution import Solutions
from python_baseline.engines.mysolver.engine import MySolverEngine
from python_baseline.infra.di import mysolver_engine

router = APIRouter(prefix="/mysolver", tags=["mysolver"])


@router.post("/solve", response_model=Solutions)
async def solve(auction: Auction, engine: MySolverEngine = Depends(mysolver_engine)):
    """
    Solve a CoW Protocol auction using the MySolver engine.
    
    Args:
        auction: The auction to solve
        engine: The MySolver engine
        
    Returns:
        Solutions object containing the solver's solutions
    """
    return await engine.solve(auction)
