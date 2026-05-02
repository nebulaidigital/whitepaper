.PHONY: help install test baseline packages rdm rdm-large clean lint format

help:
	@echo "Available targets:"
	@echo "  install      Install dependencies in editable mode (pip)"
	@echo "  test         Run pytest test suite"
	@echo "  baseline     Run status-quo baseline simulation"
	@echo "  packages     Compare all 7 policy packages at 2036"
	@echo "  rdm          RDM sweep with 1000 scenarios per package"
	@echo "  rdm-large    RDM sweep with 5000 scenarios per package + CSV output"
	@echo "  lint         Run ruff lint"
	@echo "  format       Run ruff format"
	@echo "  clean        Remove results/ and __pycache__"

install:
	pip install -e ".[dev]"

test:
	python -m pytest

baseline:
	python scripts/run_baseline.py

packages:
	python scripts/run_packages.py

rdm:
	python scripts/run_rdm.py --scenarios 1000

rdm-large:
	mkdir -p results
	python scripts/run_rdm.py --scenarios 5000 --csv results/rdm_5000.csv

lint:
	ruff check src/ tests/ scripts/

format:
	ruff format src/ tests/ scripts/

clean:
	rm -rf results/ __pycache__/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
