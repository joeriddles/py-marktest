import os

import pytest

import marktest


def test_given_parse_code_line_when_a_code_line_then_adds_try_except():
    actual = marktest.parse_code_line("... # raises Error")
    expected = [
        "try:\n",
        "    ...\n",
        "except Error:\n",
        "    pass\n"
    ]
    assert actual == expected


def test_given_parse_code_line_when_no_comment_then_returns_line():
    actual = marktest.parse_code_line("print('hello')")
    expected = ["print('hello')"]
    assert actual == expected


@pytest.fixture
def setup_main():
    with open("test.md", "w") as fout:
        lines = """# Main

This is a normal sentence.

```python
print("hello")
```

```python
raise Exception() # raises Exception
```""".splitlines()
        fout.writelines([line + os.linesep for line in lines])
    yield
    os.remove("test.md")
    os.remove("_testfile.py")


def test_main(setup_main):
    assert marktest.main("test.md") == 0
    assert os.path.exists("./_testfile.py")
    with open("./_testfile.py") as testfile:
        actual = testfile.readlines()
        expected = [
            "print(\"hello\")\n",
            "try:\n",
            "    raise Exception()\n",
            "except Exception:\n",
            "    pass\n",
        ]
        assert actual == expected
