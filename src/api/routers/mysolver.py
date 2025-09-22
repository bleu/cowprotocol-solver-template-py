"""
MySolver router.
"""
from fastapi import APIRouter, Depends
from src.domain.auction import Auction
from src.domain.solution import Solutions
from src.engines.mysolver.engine import MySolverEngine
from src.infra.di import mysolver_engine

router = APIRouter(prefix="/mysolver", tags=["mysolver"])

@router.post("/solve")
async def solve_mysolver(
    auction: Auction,
    engine: MySolverEngine = Depends(mysolver_engine)
) -> Solutions:
    """Solve auction using custom solver engine."""
    return await engine.solve(auction)
