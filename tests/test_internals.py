import pytest

from case_conversion import Case, CaseConverter, InvalidAcronymError
import case_conversion.utils as utils


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
    ),
)
def test_segment_string(string, expected):
    assert utils._segment_string(string) == expected


@pytest.mark.parametrize(
    "acronyms,expected",
    (
        (("http",), ["HTTP"]),
        (("HTTP",), ["HTTP"],),
        (("Http",), ["HTTP"],),
        (("httP",), ["HTTP"],),
        (("http", "Nasa"), ["HTTP", "NASA"]),
    ),
)
def test_sanitize_acronyms(acronyms, expected):
    assert utils._sanitize_acronyms(acronyms) == expected


@pytest.mark.parametrize(
    "s,i,words,expected",
    (
        # TODO: Add more cases
        (0, 1, ["FOO", "bar"], 0),
        (1, 2, ["foo", "BAR", "baz"], 1),
    ),
)
def test_simple_acronym_detection(s, i, words, expected):
    assert utils._simple_acronym_detection(s, i, words) == expected


@pytest.mark.parametrize(
    "s,i,words,acronyms,expected",
    (
        # TODO: Add more cases
        (0, 1, ["FOO", "bar"], ("FOO",), 0),
        (0, 1, ["FOO", "bar"], ("BAR",), 2),
    ),
)
def test_advanced_acronym_detection(s, i, words, acronyms, expected):
    assert utils._advanced_acronym_detection(s, i, words, acronyms) == expected


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
    assert CaseConverter.parse_case(string, acronyms, preserve_case) == expected


def test_invalid_acronym_error_message():
    acronym = "BadAcronym"
    msg = f"Case Conversion: acronym '{acronym}' is invalid."
    try:
        raise InvalidAcronymError(acronym)
    except InvalidAcronymError as e:
        assert msg in str(e)


@pytest.mark.parametrize("acronyms", ("HT-TP", "NA SA", "SU.GAR"))
def test_sanitize_acronyms_raises_on_invalid_acronyms(acronyms):
    with pytest.raises(InvalidAcronymError):
        utils._sanitize_acronyms(acronyms)


@pytest.mark.parametrize(
    "words,acronyms,expected",
    (
        (["foobar"], (), ["Foobar"]),
        (["fooBar"], (), ["Foobar"]),
        (["FooBar"], (), ["Foobar"]),
        (["Foo", "Bar"], ("BAR"), ["Foo", "BAR"]),
    ),
)
def test_normalize_words(words, acronyms, expected):
    assert utils._normalize_words(words, acronyms) == expected


@pytest.mark.parametrize(
    "was_upper,words,string,expected",
    (
        (False, [], "", Case.UNKOWN),
        (True, [], "", Case.UPPER),
        (False, [], "foobar", Case.LOWER),
        (False, ["foo", "Bar"], "", Case.CAMEL),
        (False, ["Foo", "Bar"], "", Case.PASCAL),
        (False, ["foo", "bar"], "", Case.MIXED),
    ),
)
def test_determine_case(was_upper, words, string, expected):
    assert utils._determine_case(was_upper, words, string) == expected
