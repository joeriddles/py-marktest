"""
Name: marktest.py
Usage: python -m marktest README.md

Inspired from https://daniel.feldroy.com/posts/my-markdown-code-snippet-tester.
"""
import re
import subprocess
import typing


class Reader(typing.Protocol):
    def read(self, filename: str) -> list[str]:
        ...


class FileReader(Reader):
    def read(self, filename: str) -> list[str]:
        with open(filename) as f:
            lines = f.readlines()
        return lines


class Writer(typing.Protocol):
    def write(self, filename: str, lines: list[str]) -> None:
        ...


class FileWriter(Writer):
    def write(self, filename: str, lines: list[str]) -> None:
        with open(filename, mode="w") as f:
            f.writelines("".join(lines))


class Parser(typing.Protocol):
    def parse(self, lines: list[str]) -> list[str]:
        """Parse lines of text, returning some other text."""
        ...


class MarkdownPythonParser(Parser):
    """Parse Python code blocks from markdown, returning the lines of code."""

    OPEN_PATTERN = re.compile(r"\s*`{3}\s*python")
    CLOSE_PATTERN = re.compile(r"\s*`{3}")
    RAISES_ERROR_PATTERN = re.compile(r"\s*raises (\w*Error|Exception)")

    def parse(self, lines: list[str]) -> list[str]:
        in_python = False
        code: list[str] = []
        for line in lines:
            if re.match(self.OPEN_PATTERN, line) is not None:
                in_python = True
            elif in_python and re.match(self.CLOSE_PATTERN, line):
                in_python = False
            elif in_python:
                parsed_code = self._parse_code_line(line)
                code.extend(parsed_code)
        return code

    def _parse_code_line(self, line: str) -> list[str]:
        """Look for comments about raising errors.

        If a comment in the format "... # raises Error" is detected, wrap the code
        line in a try/except for that error and handle the error.
        """
        lines: list[str] = []
        has_comment = "#" in line
        if has_comment:
            code, comment = line.split("#")
            code = code.rstrip()
            comment = comment.strip()
            if match := self.RAISES_ERROR_PATTERN.match(comment):
                # note: does not handle matching indentation currently and assumes
                # 4-spaces for indentation
                error = match.groups()[0]
                lines.append("try:\n")
                lines.append(f"    {code}\n")
                lines.append(f"except {error}:\n")
                lines.append("    pass\n")
                return lines

        lines.append(line)
        return lines


class Runner(typing.Protocol):
    def run(self, cmd: list[str]) -> tuple[str, str]:
        """Run the command and return the stdout and stderr."""
        ...


class PythonRunner(Runner):
    def __init__(self, python_entrypoint: str = "python3"):
        self._python_entrypoint = python_entrypoint

    def run(self, cmd: list[str]) -> tuple[str, str]:
        cmd = [self._python_entrypoint] + cmd
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = proc.communicate()
        output = output.decode("utf-8")
        error = error.decode("utf-8")
        return output, error


def main(
    filename: str,
    python_entrypoint="python",
    test_filename="_testfile.py",
):
    reader: Reader = FileReader()
    lines = reader.read(filename)

    parser: Parser = MarkdownPythonParser()
    code = parser.parse(lines)

    writer: Writer = FileWriter()
    writer.write(test_filename, code)

    runner: Runner = PythonRunner(python_entrypoint)
    _, stderr = runner.run([test_filename])

    if stderr:
        print(stderr)
        return 1
    return 0
