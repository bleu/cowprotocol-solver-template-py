"""
Prometheus metrics collection for the solver service.
"""

from typing import Dict, Any
import time
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

# Metrics definitions
REQUEST_COUNT = Counter(
    'solver_requests_total',
    'Total number of solver requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'solver_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint']
)

ACTIVE_REQUESTS = Gauge(
    'solver_active_requests',
    'Number of active requests'
)

SOLVER_SOLUTIONS = Counter(
    'solver_solutions_total',
    'Total number of solutions generated',
    ['status']
)

SOLVER_ORDERS = Histogram(
    'solver_orders_per_auction',
    'Number of orders per auction',
    buckets=[1, 5, 10, 25, 50, 100, 250, 500, 1000]
)


class MetricsCollector:
    """Metrics collection helper."""
    
    def __init__(self):
        self.start_time = time.time()
    
    def record_request(self, method: str, endpoint: str, status: str, duration: float):
        """Record a request metric."""
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status).inc()
        REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(duration)
    
    def record_solution(self, status: str):
        """Record a solution generation metric."""
        SOLVER_SOLUTIONS.labels(status=status).inc()
    
    def record_auction_orders(self, order_count: int):
        """Record the number of orders in an auction."""
        SOLVER_ORDERS.observe(order_count)
    
    def set_active_requests(self, count: int):
        """Set the number of active requests."""
        ACTIVE_REQUESTS.set(count)
    
    def get_metrics(self) -> str:
        """Get Prometheus metrics in text format."""
        return generate_latest().decode('utf-8')
    
    def get_metrics_content_type(self) -> str:
        """Get the content type for metrics."""
        return CONTENT_TYPE_LATEST


# Global metrics collector
_metrics = MetricsCollector()


def get_metrics() -> str:
    """Get Prometheus metrics."""
    return _metrics.get_metrics()


def get_metrics_content_type() -> str:
    """Get metrics content type."""
    return _metrics.get_metrics_content_type()


def record_request(method: str, endpoint: str, status: str, duration: float):
    """Record a request metric."""
    _metrics.record_request(method, endpoint, status, duration)


def record_solution(status: str):
    """Record a solution generation metric."""
    _metrics.record_solution(status)


def record_auction_orders(order_count: int):
    """Record auction order count."""
    _metrics.record_auction_orders(order_count)


def set_active_requests(count: int):
    """Set active request count."""
    _metrics.set_active_requests(count)
