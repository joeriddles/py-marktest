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
