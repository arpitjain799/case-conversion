import pytest

from case_conversion import CaseConverter

@pytest.mark.parametrize(
    "string,expected",
    (
        ("fooBarString", (["foo", "Bar", "String"], "", False)),
        ("FooBarString", (["Foo", "Bar", "String"], "", False)),
        ("foo_bar_string", (["foo", None, "bar", None, "string"], "_", False)),
        ("foo-bar-string", (["foo", None, "bar", None, "string"], "-", False)),
        ("FOO_BAR_STRING", (["foo", None, "bar", None, "string"], "_", True)),
        ("foo.bar.string", (["foo", None, "bar", None, "string"], ".", False)),
        ("foo bar string", (["foo", None, "bar", None, "string"], " ", False)),
        ("foo/bar/string", (["foo", None, "bar", None, "string"], "/", False)),
        ("foo\\bar\\string", (["foo", None, "bar", None, "string"], "\\", False)),
        ("foobarstring", (["foobarstring"], "", False)),
        ("FOOBARSTRING", (["foobarstring"], "", True)),
    )
)
def test_segment_string(string, expected):
    assert CaseConverter._segment_string(string) == expected
