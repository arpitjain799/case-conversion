import pytest

from case_conversion import Case, parse_case


@pytest.mark.parametrize(
    "string,acronyms,preserve_case,expected",
    (
        ("fooBarBaz", None, False, (["Foo", "Bar", "Baz"], Case.CAMEL, "")),
        ("fooBarBaz", None, True, (["foo", "Bar", "Baz"], Case.CAMEL, "")),
        ("fooBarBaz", ("BAR",), False, (["Foo", "BAR", "Baz"], Case.CAMEL, "")),
        ("fooBarBaz", ("BAR",), True, (["foo", "Bar", "Baz"], Case.CAMEL, "")),
    ),
)
def test_parse_case(string, acronyms, preserve_case, expected):
    assert parse_case(string, acronyms, preserve_case) == expected
