import os

import pytest

from py_marktest import marktest


@pytest.fixture(scope="package", autouse=True)
def cleanup_testfile():
    """Delete the test file once at the end."""
    yield
    os.remove(marktest.ROOT_PATH / "_testfile.py")
