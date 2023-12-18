"""
Name: marktest.py
Usage: python -m marktest README.md

Inspired from https://daniel.feldroy.com/posts/my-markdown-code-snippet-tester.
"""
import re
import subprocess

open_pattern = re.compile(r"\s*`{3}\s*python")
close_pattern = re.compile(r"\s*`{3}")
test_filename = "_testfile.py"

RAISES_ERROR_PATTERN = re.compile(r"\s*raises (\w*Error)")


def parse_code_line(line: str) -> list[str]:
    """Look for comments about raising errors.
    
    If a comment in the format "... # raises Error" is detected, wrap the code
    line in a try/except for that error and eat the error.
    """
    lines: list[str] = []
    has_comment = "#" in line
    if has_comment:
        code, comment = line.split("#")
        code = code.rstrip()
        comment = comment.strip()
        if match := RAISES_ERROR_PATTERN.match(comment):
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



def main(filename, python_cmd="python"):
    # Create an array of the Python code called "code"
    code: list[str] = []
    in_python = False
    with open(filename) as f:
        for line in f.readlines():
            if re.match(open_pattern, line) is not None:
                in_python = True
            elif in_python and re.match(close_pattern, line):
                in_python = False
            elif in_python:
                parsed_code = parse_code_line(line)
                code.extend(parsed_code)

    # # Debugging
    # for line in code:
    #     print(line.rstrip("\n"))

    # Save the code as a string to the testfile
    # `tempfile.NamedTempFile` fails here because the `write()` doesn't seem to occur
    # until the `with` statement is finished. I would love to be wrong in that, using
    # a tempfile is the cleaner approach. Please let me know a better approach.
    with open(test_filename, mode="w") as f:
        f.writelines("".join(code))

    # Run the code
    cmd = [python_cmd, test_filename]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = proc.communicate()

    # Display the results
    output = output.decode("utf-8")
    error = error.decode("utf-8")
    if error:
        print(error)

    # Cleanup
    # os.remove(test_filename)

    return proc.returncode
