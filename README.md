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

## Install Requirements

1. Python 3.11+ (tested with Python 3.11.9)
2. Rust v1.60.0+ (for connecting to the driver)

```sh
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install additional dependencies for configuration system
pip install pydantic-settings httpx

# Verify installation
python -c "from src.infra.settings import settings; print('✅ Config OK:', settings.solver.chain_id)"
```

### Quick Test

```sh
# Test configuration system
python -m pytest src/tests/test_config.py -v

# Show current configuration
python -m src.infra.cli config
```

## Run Solver Server

### Multi-Engine Solver (Recommended)

The solver now supports multiple engines in a single FastAPI application with a clean, modular structure:

```shell
source venv/bin/activate
python -m src.infra.cli run --host 0.0.0.0 --port 8080
```

Or using uvicorn directly:
```shell
uvicorn src.api.app:app --host 0.0.0.0 --port 8080
```

Or using the entry point:
```shell
python -m src._server
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

### Solve an Auction with Default Engine
```shell
curl -X POST "http://127.0.0.1:8080/solve" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  --data "@data/small_example.json"
```

### Prometheus Metrics
```shell
curl http://localhost:8080/metrics
```

## Run Tests

The project includes a comprehensive test suite:

### Configuration Tests (Recommended)
```shell
# Test configuration system (9 tests)
python -m pytest src/tests/test_config.py -v

# Quick configuration test
python -c "from src.infra.settings import settings; print('✅ Config OK:', settings.solver.chain_id)"

# Show current configuration
python -m src.infra.cli config
```

### All Tests
```shell
# Run all tests
pytest src/tests/

# Run specific test categories
pytest src/tests/test_api_health_metrics.py
pytest src/tests/test_models_smoke.py
pytest src/tests/test_multi_engine.py

# Run with coverage
pytest src/tests/ --cov=src
```

### Test Commands Summary
```shell
# Basic tests
python -m pytest src/tests/test_config.py -v          # Configuration tests
python -m pytest src/tests/test_api_health_metrics.py -v  # API tests

# Manual tests
python -c "from src.infra.settings import settings; print(settings.solver.dict())"  # Show config
python -m src.infra.cli config                          # CLI config display
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

```
src/
├── _server.py              # Main server entry point
├── api/                    # API endpoints and routing
│   ├── app.py             # Main FastAPI application
│   ├── healthz.py         # Health check endpoint
│   ├── metrics.py         # Metrics collection
│   └── routers/           # API routers
│       ├── baseline.py    # Baseline solver router
│       └── mysolver.py    # MySolver router
├── domain/                # Domain models and business logic
│   ├── auction.py         # Auction model
│   ├── solution.py        # Solution model
│   ├── order.py           # Order model
│   ├── liquidity.py       # Liquidity model
│   └── common.py          # Common domain types
├── engines/               # Solver engine implementations
│   ├── base.py            # Base engine protocol
│   ├── baseline/          # Baseline solver engine
│   │   └── engine.py      # Baseline implementation
│   └── mysolver/          # Custom solver engine
│       └── engine.py      # MySolver implementation
├── infra/                 # Infrastructure and configuration
│   ├── settings.py        # Application settings
│   ├── logging.py         # Logging configuration
│   ├── metrics.py         # Metrics infrastructure
│   ├── di.py              # Dependency injection
│   └── cli.py             # Command line interface
├── utils/                 # Utility functions
│   ├── bytes_conv.py      # Bytes conversion utilities
│   ├── hexbytes.py       # Hex bytes utilities
│   ├── mathx.py          # Math utilities
│   ├── serialize.py      # Serialization utilities
│   └── u256.py           # U256 utilities
└── tests/                 # Test suite
    ├── test_api_health_metrics.py
    ├── test_api_solve_contract.py
    ├── test_models_smoke.py
    └── test_multi_engine.py

data/
├── small_example.json     # Example auction data
└── large_example.json     # Larger example auction data
```

## Implementation Guide

1. **Understand the Models**: Start by examining the domain models in `src/domain/` (auction.py, solution.py, order.py, etc.)
2. **Study Engine Architecture**: Check `src/engines/base.py` for the engine protocol and `src/engines/baseline/engine.py` for implementation patterns
3. **Implement Custom Solver**: Modify `src/engines/mysolver/engine.py` to implement your solver logic
4. **Add Pathfinding**: Implement algorithms to find optimal trading paths
5. **Handle AMMs**: Add support for different AMM protocols
6. **Optimize**: Implement price optimization and MEV protection
7. **Test**: Use the test suite in `src/tests/` to validate your implementation

## Architecture

The solver template now features a clean, modular architecture:

- **API Layer**: FastAPI application with separate routers for each engine
- **Domain Layer**: Business models and logic (auction, solution, order, etc.)
- **Engine Layer**: Pluggable solver implementations (baseline, custom)
- **Infrastructure Layer**: Configuration, logging, metrics, and dependency injection
- **Utils Layer**: Shared utilities for math, serialization, and data conversion
- **Test Layer**: Comprehensive test suite for all components

## Schema Compatibility

This template now uses the current CoW Protocol schema:
- **Input**: `Auction` model with proper field aliases
- **Output**: `Solutions` model matching the protocol specification
- **Field Names**: Uses Python snake_case with automatic camelCase JSON conversion

## References

- [CoW Protocol Solvers Tutorial](https://docs.cow.fi/cow-protocol/tutorials/solvers)
- [Settlement Contract](https://github.com/cowprotocol/contracts/blob/ff6fb7cad7787b8d43a6468809cacb799601a10e/src/contracts/GPv2Settlement.sol#L121-L143)
- [Interaction Model](https://github.com/cowprotocol/services/blob/cda5e36db34c55e7bf9eb4ea8b6e36ecb046f2b2/crates/shared/src/http_solver/model.rs#L125-L130)

## Contributing

This template is actively maintained. Please feel free to submit issues and pull requests to improve the template for the community.

## License

See LICENSE file for details.