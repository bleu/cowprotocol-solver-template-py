> [!WARNING]  
> This repository is outdated and does not currently function as a basis for implementing a solver.

# CoW Protocol Solver Template (Python)

A Python template for implementing CoW Protocol solvers. This template provides a basic structure and examples for building solvers that can participate in CoW Protocol auctions.

## Setup Project

Clone this repository

```sh
git clone git@github.com:cowprotocol/solver-template-py.git
cd solver-template-py
```

## Poetry Setup

This project uses Poetry for dependency management. Install Poetry first by following the [official Poetry documentation](https://python-poetry.org/docs/).

## Install Requirements

1. Python 3.11+ (tested with Python 3.11.9)
2. Poetry (for dependency management)
3. Rust v1.60.0+ (for connecting to the driver)

```sh
# Install dependencies with Poetry
poetry install


# Verify installation
poetry run python -c "from src.infra.settings import settings; print('✅ Config OK:', settings.solver.chain_id)"
```


### Quick Test

```sh
# Test configuration system
poetry run python -m pytest src/tests/test_config.py -v

# Show current configuration
poetry run python -m src.infra.cli config
```

## Run Solver Server

The solver supports multiple engines in a single FastAPI application with a clean, modular structure:

```shell
# Using Makefile (Recommended)
make run

# Or manually
poetry run python -m src.infra.cli run

# Alternative methods
poetry run python -m src._server
poetry run uvicorn src.api.app:app --host 0.0.0.0 --port 8080
```

The solver will start on `http://localhost:8080` with the following endpoints:
- `GET /` - Root endpoint with service information
- `GET /healthz` - Health check
- `GET /metrics` - Prometheus metrics
- `POST /baseline/solve` - Baseline solver engine
- `POST /mysolver/solve` - MySolver engine (stub implementation)
- `POST /solve` - Default solver (configurable via DEFAULT_SOLVER_ROUTE)

## Test the Solver

### Health Check
```shell
curl http://localhost:8080/healthz
```

### Solve an Auction with Baseline Engine
```shell
curl -X POST "http://127.0.0.1:8080/baseline/solve" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  --data "@data/small_example.json"
```

### Solve an Auction with MySolver Engine
```shell
curl -X POST "http://127.0.0.1:8080/mysolver/solve" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  --data "@data/small_example.json"
```

### Prometheus Metrics
```shell
curl http://localhost:8080/metrics
```

## Development Commands

The project includes a Makefile with convenient development commands:

```shell
# Show all available commands
make help

# Start the solver server
make run

# Format code with black
make format

# Run all tests
make test

# Install dependencies
make install

# Clean up temporary files
make clean
```

### Manual Commands

If you prefer to run commands manually:

```shell
# Start server
poetry run python -m src.infra.cli run --host 0.0.0.0 --port 8080

# Format code
poetry run black src/ --line-length 88

# Run tests
poetry run pytest src/tests/ -v

# Show configuration
poetry run python -m src.infra.cli config
```

## Run Tests

The project includes a comprehensive test suite:

### Configuration Tests (Recommended)
```shell
# Test configuration system (9 tests)
poetry run python -m pytest src/tests/test_config.py -v

# Quick configuration test
poetry run python -c "from src.infra.settings import settings; print('✅ Config OK:', settings.solver.chain_id)"

# Show current configuration
poetry run python -m src.infra.cli config
```

### All Tests
```shell
# Run all tests
poetry run pytest src/tests/

# Run specific test categories
poetry run pytest src/tests/test_api_health_metrics.py
poetry run pytest src/tests/test_baseline_engine.py
poetry run pytest src/tests/test_config.py

# Run with coverage
poetry run pytest src/tests/ --cov=src
```

### Test Commands Summary
```shell
# Basic tests
poetry run python -m pytest src/tests/test_config.py -v          # Configuration tests
poetry run python -m pytest src/tests/test_api_health_metrics.py -v  # API tests

# Manual tests
poetry run python -c "from src.infra.settings import settings; print(settings.solver.dict())"  # Show config
poetry run python -m src.infra.cli config                          # CLI config display
```

## Connect to the Orderbook

To connect your solver to the CoW Protocol orderbook, you need to run the driver (auction dispatcher) in DryRun mode. This will read from the staging environment on Gnosis Chain.

### Prerequisites
1. Clone the services repository:
```shell
git clone https://github.com/cowprotocol/services.git
cd services
```

2. Make sure your solver is running on `http://127.0.0.1:11088`

### Run the Driver
```shell
cargo run -p driver -- \
    --orderbook-url https://barn.api.cow.fi/xdai/api \
    --base-tokens 0xDDAfbb505ad214D7b80b1f830fcCc89B60fb7A83 \
    --node-url "https://rpc.gnosischain.com" \
    --cow-dex-ag-solver-url "http://127.0.0.1:11088" \
    --solver-account 0x7942a2b3540d1ec40b2740896f87aecb2a588731 \
    --solvers CowDexAg \
    --transaction-strategy DryRun \
    --log-filter=info,solver=debug
```

The driver will connect to the staging orderbook on Gnosis Chain (very low traffic) so you can work with your own orders.

### Autopilot Configuration

You can configure autopilot to use different solver engines by pointing to different endpoints:

```shell
# Use baseline solver
--cow-dex-ag-solver-url "http://127.0.0.1:11088/baseline/solve"

# Use MySolver engine
--cow-dex-ag-solver-url "http://127.0.0.1:11088/mysolver/solve"

# Use default solver (configurable via DEFAULT_SOLVER_ROUTE)
--cow-dex-ag-solver-url "http://127.0.0.1:11088/solve"
```

## Place an Order

Navigate to [barn.cow.fi/](https://barn.cow.fi/) and place a tiny (real) order. You should see your driver pick it up and include it in the next auction being sent to your solver.

> **Note**: The driver and barn integration steps above have not been tested yet. They are included based on the original documentation and should be verified before use.

## Project Structure

The solver follows a clean, modular architecture:

- **`src/domain/`** - Business models (auction, order, solution, liquidity)
- **`src/engines/`** - Solver implementations (baseline, custom)
- **`src/api/`** - FastAPI endpoints and routing
- **`src/infra/`** - Configuration, logging, metrics
- **`src/utils/`** - Shared utilities (math, serialization)
- **`src/tests/`** - Test suite

## Non-Production Ready Parts

This template contains areas marked with `TODO:` comments that indicate non-production ready implementations. These are simplified or stub implementations that need to be replaced with proper production code.

## Implementation Guide

1. **Understand the Models**: Start by examining the domain models in `src/domain/` (auction.py, solution.py, order.py, etc.)
2. **Study Engine Architecture**: Check `src/engines/base.py` for the engine protocol and `src/engines/baseline/engine.py` for implementation patterns
3. **Implement Custom Solver**: Modify `src/engines/mysolver/engine.py` to implement your solver logic
4. **Add Pathfinding**: Implement algorithms to find optimal trading paths
5. **Handle AMMs**: Add support for different AMM protocols
6. **Optimize**: Implement price optimization and MEV protection
7. **Test**: Use the test suite in `src/tests/` to validate your implementation

## Architecture

The solver template features a clean, modular architecture:

- **API Layer**: FastAPI application with separate routers for each engine
- **Domain Layer**: Business models and logic (auction, solution, order, etc.)
- **Engine Layer**: Pluggable solver implementations (baseline, custom)
- **Infrastructure Layer**: Configuration, logging, metrics, and dependency injection
- **Utils Layer**: Shared utilities for math, serialization, and data conversion
- **Test Layer**: Comprehensive test suite for all components

## Schema Compatibility

This template uses the schema:
- **Input**: `Auction` model with proper field aliases
- **Output**: `Solutions` model matching the protocol specification
- **Field Names**: Uses Python snake_case with automatic camelCase JSON conversion

## References

- [CoW Protocol Solvers Tutorial](https://docs.cow.fi/cow-protocol/tutorials/solvers)
- [Settlement Contract](https://github.com/cowprotocol/contracts/blob/ff6fb7cad7787b8d43a6468809cacb799601a10e/src/contracts/GPv2Settlement.sol#L121-L143)
- [Interaction Model](https://github.com/cowprotocol/services/blob/cda5e36db34c55e7bf9eb4ea8b6e36ecb046f2b2/crates/shared/src/http_solver/model.rs#L125-L130)

## Contributing

Please feel free to submit issues and pull requests to improve the template for the community.
