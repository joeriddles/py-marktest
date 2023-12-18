# !/usr/bin
PYTHON=python
if ! command -v $PYTHON &> /dev/null
then
    PYTHON=python3
fi

PYTHONPATH=$PYTHONPATH:./src $PYTHON -m py-marktest README.md $PYTHON && echo "marktest passed"
$PYTHON -m pytest --quiet src && echo "pytest passed"
