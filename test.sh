# !/usr/bin
PYTHON=python
if ! command -v $PYTHON &> /dev/null
then
    PYTHON=python3
fi

PYTHONPATH=$PYTHONPATH:./src $PYTHON -m py-marktest README.md $PYTHON && echo "marktest passed"

$PYTHON -m pytest \
    --cov-config=pyproject.toml \
    --cov=src \
    --cov-fail-under=80 \
    --cov-report=html \
    src && echo "pytest passed"

$PYTHON -m coverage report
