"""
Dependency injection for solver engines.
"""

from src.engines.baseline.engine import BaselineEngine
from src.engines.mysolver.engine import MySolverEngine
from src.engines.base import SolverEngine


def baseline_engine() -> SolverEngine:
    """Get baseline solver engine instance."""
    return BaselineEngine()


def mysolver_engine() -> SolverEngine:
    """Get MySolver engine instance."""
    return MySolverEngine()
