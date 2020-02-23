import pytest

from case_conversion import CaseConverter, InvalidAcronymError

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


@pytest.mark.parametrize(
    "acronyms,expected",
    (
        (("http",), ["HTTP"]),
        (("HTTP",), ["HTTP"],),
        (("Http",), ["HTTP"],),
        (("httP",), ["HTTP"],),
        (("http", "Nasa"), ["HTTP", "NASA"]),
    )
)
def test_sanitize_acronyms(acronyms, expected):
    assert CaseConverter._sanitize_acronyms(acronyms) == expected


@pytest.mark.parametrize(
    "acronyms",
    (
        "HT-TP", "NA SA", "SU.GAR"
    )
)
def test_sanitize_acronyms_raises_on_invalid_acronyms(acronyms):
    with pytest.raises(InvalidAcronymError):
        CaseConverter._sanitize_acronyms(acronyms)


@pytest.mark.parametrize(
    "words,acronyms,expected",
    (
        (["foobar"], (), ["Foobar"]),
        (["fooBar"], (), ["Foobar"]),
        (["FooBar"], (), ["Foobar"]),
        (["Foo", "Bar"], ("BAR"), ["Foo", "BAR"]),
    )
)
def test_normalize_words(words, acronyms, expected):
    assert CaseConverter._normalize_words(words, acronyms) == expected


@pytest.mark.parametrize(
    "was_upper,words,string,expected",
    (
        (False, [], "", "unknown"),
        (True, [], "", "upper"),
        (False, [], "foobar", "lower"),
        (False, ["foo", "Bar"], "", "camel"),
        (False, ["Foo", "Bar"], "", "pascal"),
        (False, ["foo", "bar"], "", "mixed"),
    )
)
def test_determine_case(was_upper, words, string, expected):
    assert CaseConverter._determine_case(was_upper, words, string) == expected
