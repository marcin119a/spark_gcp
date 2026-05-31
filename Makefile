.PHONY: install conda-create conda-update run test lint format clean

VENV = .venv
PY   = $(VENV)/bin/python
PIP  = $(VENV)/bin/pip

# ── Virtualenv ─────────────────────────────────────────────────────────────────
install:
	python -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install -e .
	@echo "Run: source $(VENV)/bin/activate"

# ── Conda ──────────────────────────────────────────────────────────────────────
conda-create:
	conda env create -f environment.yml
	@echo "Run: conda activate us-accidents-etl"

conda-update:
	conda env update -f environment.yml --prune

# ── Run ────────────────────────────────────────────────────────────────────────
run:
	$(PY) main.py

# ── Tests ──────────────────────────────────────────────────────────────────────
test:
	$(VENV)/bin/pytest tests/ -v

test-cov:
	$(VENV)/bin/pytest tests/ -v --cov=src/us_accidents_etl --cov-report=term-missing

# ── Lint / Format ──────────────────────────────────────────────────────────────
lint:
	$(VENV)/bin/ruff check src/ tests/
	$(VENV)/bin/mypy src/

format:
	$(VENV)/bin/black src/ tests/
	$(VENV)/bin/ruff check --fix src/ tests/

# ── Clean ──────────────────────────────────────────────────────────────────────
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
