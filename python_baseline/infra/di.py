"""
Dependency injection for solver engines.
"""

from python_baseline.engines.baseline.engine import BaselineEngine
from python_baseline.engines.mysolver.engine import MySolverEngine
from python_baseline.engines.base import SolverEngine


def baseline_engine() -> SolverEngine:
    """Get baseline solver engine instance."""
    return BaselineEngine()


def mysolver_engine() -> SolverEngine:
    """Get MySolver engine instance."""
    return MySolverEngine()
