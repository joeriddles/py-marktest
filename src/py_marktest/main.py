import doctest
import os

from py_marktest.marktest import (
    FileReader,
    FileWriter,
    MarkdownPythonParser,
    Parser,
    PythonRunner,
    Reader,
    Runner,
    Writer,
)


def main(
    filename: str,
    python_entrypoint: str = "python3",
    test_filename: str = "_testfile.py",
) -> int:
    # Test all REPLs
    # https://docs.python.org/3/library/doctest.html
    doctest.testfile(filename, module_relative=False)

    reader: Reader = FileReader()
    lines = reader.read(filename)

    parser: Parser = MarkdownPythonParser()
    code_blocks = parser.parse(lines)

    writer: Writer = FileWriter()
    runner: Runner = PythonRunner(python_entrypoint)

    all_lines = []

    for index, code_block in enumerate(code_blocks, start=1):
        all_lines.extend(
            [
                f"### Code Block {index}{os.linesep}",
                str(code_block),
                "\n",
            ]
        )
    writer.write(test_filename, all_lines)

    _, stderr = runner.run([test_filename])

    if stderr:
        print(stderr)
        return 1

    return 0
