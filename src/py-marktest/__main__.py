import doctest
import pathlib
import sys

ROOT = pathlib.Path(__name__).parent.parent

if __name__ == "__main__":
    filename = sys.argv[1]
    try:
        python_cmd = sys.argv[2]
    except IndexError:
        python_cmd = "python3"

    # Test all REPLs
    # https://docs.python.org/3/library/doctest.html
    doctest.testfile(filename, module_relative=False)

    from . import marktest
    returncode = marktest.main(filename, python_cmd)
    exit(returncode)
