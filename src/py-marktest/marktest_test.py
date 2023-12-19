import functools
import os
import tempfile
import unittest

import marktest
import pytest
from marktest import MarkdownPythonParser, PythonRunner

create_temp = functools.partial(tempfile.NamedTemporaryFile, delete_on_close=False)


class MarkdownPythonParserTests(unittest.TestCase):
    def test_given_parse_code_line_when_a_code_line_then_adds_try_except(self):
        parser = MarkdownPythonParser()
        actual = parser.parse(
            [
                "```python",
                "... # raises Error",
                "```",
            ]
        )
        expected = [
            "try:\n",
            "    ...\n",
            "except Error:\n",
            "    pass\n",
        ]
        assert actual == expected

    def test_given_parse_code_line_when_no_comment_then_returns_line(self):
        parser = MarkdownPythonParser()
        actual = parser.parse(
            [
                "```python",
                "print('hello')",
                "```",
            ]
        )
        expected = ["print('hello')"]
        assert actual == expected


class PythonRunnerTests(unittest.TestCase):
    def test_run_with_basic_print(self):
        runner = PythonRunner()
        with create_temp("w") as tf:
            tf.write("print('hello')")
            stdout, stderr = runner.run([tf.name])
        assert stdout == ""
        assert stderr == ""

    def test_with_raises_exception(self):
        runner = PythonRunner()
        with create_temp("w") as tf:
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


@pytest.fixture
def generate_tempfile():
    tf = create_temp("w", delete=False)
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
    os.remove("./_testfile.py")


def test_integration(generate_tempfile: str):
    marktest.main(generate_tempfile)

    with open("./_testfile.py") as testfile:
        actual = testfile.readlines()
        expected = [
            'print("hello")\n',
            "try:\n",
            "    raise Exception()\n",
            "except Exception:\n",
            "    pass\n",
        ]
        assert actual == expected
