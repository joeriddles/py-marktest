import os
import tempfile

import pytest

from py_marktest import main, marktest


@pytest.fixture
def generate_tempfile():
    tf = tempfile.NamedTemporaryFile(
        "w",
        delete=False,
        delete_on_close=False,
    )
    tf.writelines(
        line + os.linesep
        for line in [
            "# Main",
            "",
            "This is a normal sentence.",
            "",
            "```python",
            'print("hello")',
            "```",
            "",
            "```python",
            "raise Exception() # raises Exception",
            "```",
        ]
    )
    tf.close()

    yield tf.name

    os.remove(tf.name)


def test_integration(generate_tempfile: str):
    main.main(generate_tempfile)

    with open("./_testfile.py") as testfile:
        actual = testfile.readlines()
        expected = [
            "### Code Block 1\n",
            'print("hello")\n',
            "\n",
            "### Code Block 2\n",
            "try:\n",
            "    raise Exception()\n",
            "except Exception:\n",
            "    pass\n",
            "\n",
        ]
        assert actual == expected


def test_examples():
    examples_dir = marktest.ROOT_PATH / "examples"
    for markdown_file in examples_dir.glob("*.md"):
        main.main(filename=str(markdown_file.absolute()))
