from typing import List, Optional, Tuple

from .alias import alias, aliased
from .utils import (
    segment_string,
    sanitize_acronyms,
    determine_case,
    normalize_words,
    advanced_acronym_detection,
    simple_acronym_detection,
    is_upper,
)
from .types import Case


@aliased
class CaseConverter:
    """Main Class."""

    @classmethod
    def parse_case(
        cls,
        string: str,
        acronyms: Optional[List[str]] = None,
        preserve_case: bool = False,
    ) -> Tuple[List[str], Case, str]:
        """
        Parse a stringiable into a list of words.

        Also returns the case type, which can be one of
        the following:
            - upper: All words are upper-case.
            - lower: All words are lower-case.
            - pascal: All words are title-case or upper-case. Note that the
                      stringiable may still have separators.
            - camel: First word is lower-case, the rest are title-case or
                     upper-case. stringiable may still have separators.
            - mixed: Any other mixing of word casing. Never occurs if there are
                     no separators.
            - unknown: stringiable contains no words.

        Also returns the first separator character,
        or False if there isn't one.
        """
        words_with_sep, separator, was_upper = segment_string(string)

        if acronyms:
            # Use advanced acronym detection with list
            acronyms = sanitize_acronyms(acronyms)
            check_acronym = advanced_acronym_detection  # type: ignore
        else:
            acronyms = []
            # Fallback to simple acronym detection.
            check_acronym = simple_acronym_detection  # type: ignore

        # Letter-run detector

        # Index of current word.
        i = 0
        # Index of first letter in run.
        s = None

        # Find runs of single upper-case letters.
        while i < len(words_with_sep):
            word = words_with_sep[i]
            if word is not None and is_upper(word):
                if s is None:
                    s = i
            elif s is not None:
                i = check_acronym(s, i, words_with_sep, acronyms) + 1  # type: ignore
                s = None
            i += 1

        # Separators are no longer needed, so they should be removed.
        words: List[str] = [w for w in words_with_sep if w is not None]

        # Determine case type.
        case_type = determine_case(was_upper, words, string)

        if preserve_case:
            if was_upper:
                words = [w.upper() for w in words]
        else:
            words = normalize_words(words, acronyms)

        return words, case_type, separator

    @classmethod
    def camel(cls, text: str, acronyms: Optional[List[str]] = None) -> str:
        """Return text in camelCase style.

        Args:
            text: input string to convert case
            detect_acronyms: should attempt to detect acronyms
            acronyms: a list of acronyms to detect

        >>> camelcase("hello world")
        'helloWorld'
        >>> camelcase("HELLO_HTML_WORLD", True, ["HTML"])
        'helloHTMLWorld'
        """
        words, _case, _sep = cls.parse_case(text, acronyms)
        if words:
            words[0] = words[0].lower()
        return "".join(words)

    @alias("mixed")
    @classmethod
    def pascal(cls, text: str, acronyms: Optional[List[str]] = None) -> str:
        """Return text in PascalCase style (aka MixedCase).

        Args:
            text: input string to convert case
            detect_acronyms: should attempt to detect acronyms
            acronyms: a list of acronyms to detect

        >>> pascalcase("hello world")
        'HelloWorld'
        >>> pascalcase("HELLO_HTML_WORLD", True, ["HTML"])
        'HelloHTMLWorld'
        """
        words, _case, _sep = cls.parse_case(text, acronyms)
        return "".join(words)

    @classmethod
    def snake(cls, text: str, acronyms: Optional[List[str]] = None) -> str:
        """Return text in snake_case style.

        Args:
            text: input string to convert case
            detect_acronyms: should attempt to detect acronyms
            acronyms: a list of acronyms to detect

        >>> snakecase("hello world")
        'hello_world'
        >>> snakecase("HelloHTMLWorld", True, ["HTML"])
        'hello_html_world'
        """
        words, _case, _sep = cls.parse_case(text, acronyms)
        return "_".join([w.lower() for w in words])

    @alias("kebap", "spinal", "slug")
    @classmethod
    def dash(cls, text: str, acronyms: Optional[List[str]] = None) -> str:
        """Return text in dash-case style (aka kebab-case, spinal-case).

        Args:
            text: input string to convert case
            detect_acronyms: should attempt to detect acronyms
            acronyms: a list of acronyms to detect

        >>> dashcase("hello world")
        'hello-world'
        >>> dashcase("HelloHTMLWorld", True, ["HTML"])
        'hello-html-world'
        """
        words, _case, _sep = cls.parse_case(text, acronyms)
        return "-".join([w.lower() for w in words])

    @alias("screaming")
    @classmethod
    def const(cls, text: str, acronyms: Optional[List[str]] = None) -> str:
        """Return text in CONST_CASE style (aka SCREAMING_SNAKE_CASE).

        Args:
            text: input string to convert case
            detect_acronyms: should attempt to detect acronyms
            acronyms: a list of acronyms to detect

        >>> constcase("hello world")
        'HELLO_WORLD'
        >>> constcase("helloHTMLWorld", True, ["HTML"])
        'HELLO_HTML_WORLD'
        """
        words, _case, _sep = cls.parse_case(text, acronyms)
        return "_".join([w.upper() for w in words])

    @classmethod
    def dot(cls, text: str, acronyms: Optional[List[str]] = None) -> str:
        """Return text in dot.case style.

        Args:
            text: input string to convert case
            detect_acronyms: should attempt to detect acronyms
            acronyms: a list of acronyms to detect

        >>> dotcase("hello world")
        'hello.world'
        >>> dotcase("helloHTMLWorld", True, ["HTML"])
        'hello.html.world'
        """
        words, _case, _sep = cls.parse_case(text, acronyms)
        return ".".join([w.lower() for w in words])

    @classmethod
    def separate_words(cls, text: str, acronyms: Optional[List[str]] = None) -> str:
        """Return text in "seperate words" style.

        Args:
            text: input string to convert case
            detect_acronyms: should attempt to detect acronyms
            acronyms: a list of acronyms to detect

        >>> separate_words("HELLO_WORLD")
        'HELLO WORLD'
        >>> separate_words("helloHTMLWorld", True, ["HTML"])
        'hello HTML World'
        """
        words, _case, _sep = cls.parse_case(text, acronyms, preserve_case=True)
        return " ".join(words)

    @classmethod
    def slash(cls, text: str, acronyms: Optional[List[str]] = None) -> str:
        """Return text in slash/case style.

        Args:
            text: input string to convert case
            detect_acronyms: should attempt to detect acronyms
            acronyms: a list of acronyms to detect

        >>> slashcase("HELLO_WORLD")
        'HELLO/WORLD'
        >>> slashcase("helloHTMLWorld", True, ["HTML"])
        'hello/HTML/World'
        """
        words, _case, _sep = cls.parse_case(text, acronyms, preserve_case=True)
        return "/".join(words)

    @classmethod
    def backslash(cls, text: str, acronyms: Optional[List[str]] = None) -> str:
        r"""Return text in backslash\case style.

        Args:
            text: input string to convert case
            detect_acronyms: should attempt to detect acronyms
            acronyms: a list of acronyms to detect

        >>> backslashcase("HELLO_WORLD") == r'HELLO\WORLD'
        True
        >>> backslashcase("helloHTMLWorld",
            True, ["HTML"]) == r'hello\HTML\World'
        True
        """
        words, _case, _sep = cls.parse_case(text, acronyms, preserve_case=True)
        return "\\".join(words)

    @alias("camel_snake")
    @classmethod
    def ada(cls, text: str, acronyms: Optional[List[str]] = None) -> str:
        """Return text in Ada_Case style."""
        words, _case, _sep = cls.parse_case(text, acronyms)
        return "_".join([w.capitalize() for w in words])

    @classmethod
    def title(cls, text: str, acronyms: Optional[List[str]] = None) -> str:
        """Return text in Title_case style."""
        return cls.snake(text, acronyms).capitalize()

    @classmethod
    def lower(cls, text: str, acronyms: Optional[List[str]] = None) -> str:
        """Return text in lowercase style."""
        return text.lower()

    @classmethod
    def upper(cls, text: str, acronyms: Optional[List[str]] = None) -> str:
        """Return text in UPPERCASE style."""
        return text.upper()

    @classmethod
    def capital(cls, text: str, acronyms: Optional[List[str]] = None) -> str:
        """Return text in UPPERCASE style."""
        return text.capitalize()

    @classmethod
    def http_header(cls, text: str, acronyms: Optional[List[str]] = None) -> str:
        """Return text in Http-Header-Case style."""
        words, _case, _sep = cls.parse_case(text, acronyms)
        return "-".join([w.capitalize() for w in words])
