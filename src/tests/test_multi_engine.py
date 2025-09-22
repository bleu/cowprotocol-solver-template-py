"""
Tests for multi-engine solver endpoints.
"""

import pytest
from fastapi.testclient import TestClient
from src.api.app import app
from src.models.auction import Auction, Order, Token
from src.models.common import Address, U256


@pytest.fixture
def client():
    """Test client fixture."""
    return TestClient(app)


@pytest.fixture
def sample_auction():
    """Sample auction for testing."""
    return Auction(
        id="test-auction-1",
        tokens={
            "0x1234567890123456789012345678901234567890": Token(
                decimals=18,
                symbol="WETH",
                reference_price=U256(2000000000000000000),  # 2 ETH in wei
                reference_price_denominator=U256(1000000000000000000)  # 1 ETH in wei
            ),
            "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd": Token(
                decimals=6,
                symbol="USDC",
                reference_price=U256(2000000),  # 2 USDC
                reference_price_denominator=U256(1000000)  # 1 USDC
            )
        },
        orders=[
                Order(
                    uid="0xorder1234567890123456789012345678901234567890123456789012345678901234",
                    sell_token=Address("0x1234567890123456789012345678901234567890"),
                    buy_token=Address("0xabcdefabcdefabcdefabcdefabcdefabcdefabcd"),
                    sell_amount=U256(1000000000000000000),  # 1 ETH
                    buy_amount=U256(2000000),  # 2000 USDC
                    fee_amount=U256(0),
                    kind="sell",
                    partially_fillable=False,
                    **{"class": "market"},  # Use the alias
                    signature="0xsignature1234567890123456789012345678901234567890123456789012345678901234",
                    app_data="0xappdata1234567890123456789012345678901234567890123456789012345678901234"
                )
        ],
        liquidity=[],
        effective_gas_price=U256(20000000000),  # 20 gwei
        deadline="2024-12-31T23:59:59Z"
    )


def test_baseline_solve_endpoint(client, sample_auction):
    """Test baseline solve endpoint."""
    response = client.post("/baseline/solve", json=sample_auction.model_dump())
    
    if response.status_code != 200:
        print(f"Error response: {response.status_code} - {response.text}")
    
    assert response.status_code == 200
    data = response.json()
    assert "solutions" in data
    assert isinstance(data["solutions"], list)


def test_mysolver_solve_endpoint(client, sample_auction):
    """Test MySolver solve endpoint."""
    response = client.post("/mysolver/solve", json=sample_auction.model_dump())
    
    if response.status_code != 200:
        print(f"Error response: {response.status_code} - {response.text}")
    
    assert response.status_code == 200
    data = response.json()
    assert "solutions" in data
    assert isinstance(data["solutions"], list)


def test_default_solve_endpoint(client, sample_auction):
    """Test default solve endpoint (should use baseline by default)."""
    response = client.post("/solve", json=sample_auction.model_dump())
    
    if response.status_code != 200:
        print(f"Error response: {response.status_code} - {response.text}")
    
    assert response.status_code == 200
    data = response.json()
    assert "solutions" in data
    assert isinstance(data["solutions"], list)


def test_healthz_endpoint(client):
    """Test healthz endpoint."""
    response = client.get("/healthz")
    
    assert response.status_code == 200
    data = response.json()
    assert "status" in data


def test_metrics_endpoint(client):
    """Test metrics endpoint."""
    response = client.get("/metrics")
    
    assert response.status_code == 200
    # Should return Prometheus metrics format
    assert "solver_requests_total" in response.text or "solver_request_duration_seconds" in response.text


def test_root_endpoint(client):
    """Test root endpoint."""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "service" in data
    assert "engines" in data
    assert "default_engine" in data
    assert data["engines"] == ["baseline", "mysolver"]
    assert data["default_engine"] == "baseline"


def test_invalid_auction_baseline(client):
    """Test baseline endpoint with invalid auction."""
    invalid_auction = {"id": "invalid", "tokens": {}, "orders": []}
    
    response = client.post("/baseline/solve", json=invalid_auction)
    
    # Should return 422 for validation error
    assert response.status_code == 422


def test_invalid_auction_mysolver(client):
    """Test MySolver endpoint with invalid auction."""
    invalid_auction = {"id": "invalid", "tokens": {}, "orders": []}
    
    response = client.post("/mysolver/solve", json=invalid_auction)
    
    # Should return 422 for validation error
    assert response.status_code == 422
