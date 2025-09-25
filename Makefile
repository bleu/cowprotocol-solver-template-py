# CoW Protocol Solver Template - Makefile
# Simple commands for development and testing

.PHONY: help run format test clean install

# Default target
help:
	@echo "CoW Protocol Solver Template - Available Commands:"
	@echo ""
	@echo "  make run      - Start the solver server"
	@echo "  make format   - Format code with black"
	@echo "  make test     - Run all tests"
	@echo "  make install  - Install dependencies"
	@echo "  make clean    - Clean up temporary files"
	@echo "  make help     - Show this help message"
	@echo ""
	@echo "Examples:"
	@echo "  make run      # Start server on http://localhost:8080"
	@echo "  make format   # Format all Python code"
	@echo "  make test     # Run test suite"

# Start the solver server
run:
	@echo "🚀 Starting CoW Protocol Solver..."
	@echo "Server will be available at: http://localhost:8080"
	@echo "Press Ctrl+C to stop"
	@echo ""
	source venv/bin/activate && python -m src.infra.cli run --host 0.0.0.0 --port 8080

# Format code with black
format:
	@echo "🎨 Formatting code with black..."
	source venv/bin/activate && python -m black src/ --line-length 88
	@echo "✅ Code formatting complete!"

# Run tests
test:
	@echo "🧪 Running test suite..."
	source venv/bin/activate && python -m pytest src/tests/ -v
	@echo "✅ Tests complete!"

# Install dependencies
install:
	@echo "📦 Installing dependencies..."
	python -m venv venv
	source venv/bin/activate && pip install -r requirements.txt
	@echo "✅ Installation complete!"
	@echo "Run 'source venv/bin/activate' to activate the virtual environment"

# Clean up temporary files
clean:
	@echo "🧹 Cleaning up temporary files..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf build/
	rm -rf dist/
	@echo "✅ Cleanup complete!"
