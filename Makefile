.PHONY: test, cov, htmlcov

test:
	. .venv/bin/activate; python -m pytest \
		-vv \
		--cov-config=pyproject.toml \
		--cov=src \
		--cov-fail-under=80 \
		--cov-report=html \
		src && echo "pytest passed"

cov: test
	. .venv/bin/activate; python -m coverage report

htmlcov:
	cd htmlcov; python -m http.server 8000

setup:
	python3 -m venv .venv
	. .venv/bin/activate; pip install '.[dev]'
