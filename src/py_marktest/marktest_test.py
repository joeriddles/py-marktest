import os
import tempfile

import pytest

from py_marktest.marktest import CodeBlock, MarkdownPythonParser, PythonRunner


@pytest.fixture
def temp_file():
    tf = tempfile.NamedTemporaryFile(
        delete=False,
        delete_on_close=False,
    )
    yield tf.name
    os.remove(tf.name)


def test_given_parse_code_line_when_a_code_line_then_adds_try_except():
    parser = MarkdownPythonParser()
    actual: list[CodeBlock] = parser.parse(
        [
            "```python",
            "... # raises Error",
            "```",
        ]
    )
    expected = [
        CodeBlock(
            [
                "try:\n",
                "    ...\n",
                "except Error:\n",
                "    pass\n",
            ]
        )
    ]
    assert actual == expected


def test_given_parse_code_line_when_no_comment_then_returns_line():
    parser = MarkdownPythonParser()
    actual: list[CodeBlock] = parser.parse(
        [
            "```python",
            "print('hello')",
            "```",
        ]
    )
    expected = [CodeBlock(["print('hello')"])]
    assert actual == expected


def test_run_with_basic_print(temp_file: str):
    runner = PythonRunner()
    with open(temp_file, "w") as tf:
        tf.write("print('hello')")
    stdout, stderr = runner.run([tf.name])
    assert stdout == "hello\n"
    assert stderr == ""


def test_with_raises_exception(temp_file: str):
    runner = PythonRunner()
    with open(temp_file, "w") as tf:
        tf.writelines(
            line + os.linesep
            for line in [
                "try:",
                "    raise Exception()",
                "except Exception:",
                "    pass",
            ]
        )
    stdout, stderr = runner.run([tf.name])
    assert stdout == ""
    assert stderr == ""
