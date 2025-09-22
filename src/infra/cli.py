"""
Command line interface for the baseline solver.

This module provides CLI functionality using typer.
"""

import typer
from typing import Optional
import uvicorn
from .settings import settings
from .logging import setup_logging, log_startup, log_shutdown


app = typer.Typer(
    name="cow-solver-baseline",
    help="CoW Protocol Baseline Solver",
    add_completion=False
)


@app.command()
def run(
    host: Optional[str] = typer.Option(None, "--host", "-h", help="Server host"),
    port: Optional[int] = typer.Option(None, "--port", "-p", help="Server port"),
    log_level: Optional[str] = typer.Option(None, "--log-level", "-l", help="Log level"),
    workers: int = typer.Option(1, "--workers", "-w", help="Number of worker processes"),
    reload: bool = typer.Option(False, "--reload", "-r", help="Enable auto-reload"),
    access_log: bool = typer.Option(True, "--access-log", help="Enable access logging")
):
    """
    Run the baseline solver server.
    """
    # Override settings with CLI arguments
    if host:
        settings.host = host
    if port:
        settings.port = port
    if log_level:
        settings.log_level = log_level
    
    # Setup logging
    setup_logging()
    
    # Log startup
    log_startup("CoW Protocol Solver", "1.0.0", settings.host, settings.port)
    
    try:
        # Run the server
        uvicorn.run(
            "src.api.app:app",
            host=settings.host,
            port=settings.port,
            workers=workers,
            reload=reload,
            access_log=access_log,
            log_level=settings.log_level.lower()
        )
    except KeyboardInterrupt:
        log_shutdown("CoW Protocol Solver")
    except Exception as e:
        typer.echo(f"Error starting server: {e}", err=True)
        raise typer.Exit(1)


@app.command()
def health():
    """
    Check the health of the solver service.
    """
    typer.echo("Health check not implemented yet")


@app.command()
def metrics():
    """
    Display solver metrics.
    """
    typer.echo("Metrics display not implemented yet")


@app.command()
def config():
    """
    Display current configuration.
    """
    typer.echo("Current configuration:")
    typer.echo(f"  Host: {settings.host}")
    typer.echo(f"  Port: {settings.port}")
    typer.echo(f"  Log Level: {settings.log_level}")
    typer.echo(f"  Metrics Enabled: {settings.metrics_enabled}")
    typer.echo(f"  Max Orders: {settings.max_orders_per_auction}")
    typer.echo(f"  Max Tokens: {settings.max_tokens_per_auction}")
    typer.echo(f"  Max Liquidity: {settings.max_liquidity_sources}")


@app.command()
def version():
    """
    Display solver version.
    """
    typer.echo(f"CoW Protocol Baseline Solver v{settings.solver_version}")


if __name__ == "__main__":
    app()
