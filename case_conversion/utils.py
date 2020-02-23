import unicodedata
from typing import cast, Any, Iterator, List, Optional, Tuple, Union

from .types import Case, InvalidAcronymError


def _get_rubstring_ranges(a_str: str, sub: str) -> Iterator[Tuple[int, int]]:
    start = 0
    sub_len = len(sub)
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield (start, start + sub_len)
        start += 1


def _char_is_sep(a_char: str) -> bool:
    return not (
        _char_is_upper(a_char) or _char_is_lower(a_char) or _char_is_decimal(a_char)
    )


def _char_is_decimal(a_char: str) -> bool:
    return unicodedata.category(a_char) == "Nd"


def _char_is_lower(a_char: str) -> bool:
    return unicodedata.category(a_char) == "Ll"


def _char_is_upper(a_char: str) -> bool:
    return unicodedata.category(a_char) == "Lu"


def _is_upper(a_string: str) -> bool:
    return len(a_string) == 1 and _char_is_upper(a_string)


def _is_valid_acronym(a_string: str) -> bool:
    if len(a_string) == 0:
        return False

    for a_char in a_string:
        if _char_is_sep(a_char):
            return False

    return True


def _determine_case(was_upper: bool, words: List[str], string: str) -> Case:
    """
    Determine case type of string.

    Arguments:
        was_upper {[type]} -- [description]
        words {[type]} -- [description]
        string {[type]} -- [description]

    Returns:
        - upper: All words are upper-case.
        - lower: All words are lower-case.
        - pascal: All words are title-case or upper-case. Note that the
                  stringiable may still have separators.
        - camel: First word is lower-case, the rest are title-case or
                 upper-case. stringiable may still have separators.
        - mixed: Any other mixing of word casing. Never occurs if there are
                 no separators.
        - unknown: stringiable contains no words.

    """
    case_type = Case.UNKOWN
    if was_upper:
        case_type = Case.UPPER
    elif string.islower():
        case_type = Case.LOWER
    elif words:
        camel_case = words[0].islower()
        pascal_case = words[0].istitle() or words[0].isupper()

        if camel_case or pascal_case:
            for word in words[1:]:
                c = word.istitle() or word.isupper()
                camel_case &= c
                pascal_case &= c
                if not c:
                    break

        if camel_case:
            case_type = Case.CAMEL
        elif pascal_case:
            case_type = Case.PASCAL
        else:
            case_type = Case.MIXED

    return case_type


def _advanced_acronym_detection(
    s: int, i: int, words: List[str], acronyms: List[str]
) -> int:
    """Detect acronyms by checking against a list of acronyms.

    Check a run of words represented by the range [s, i].
    Return last index of new word groups.
    """
    # Combine each letter into single string.
    acstr = "".join(words[s:i])

    # List of ranges representing found acronyms.
    range_list: List[Tuple[int, int]] = []
    # Set of remaining letters.
    not_range = set(range(len(acstr)))

    # Search for each acronym in acstr.
    for acronym in acronyms:
        for (a, b) in _get_rubstring_ranges(acstr, acronym):
            # Make sure found acronym doesn't overlap with others.
            ok = True
            for r in range_list:
                if a < r[1] and b > r[0]:
                    ok = False
                    break

            if ok:
                range_list.append((a, b))
                for j in range(a, b):
                    not_range.remove(j)

    # Add remaining letters as ranges.
    for nr in not_range:
        range_list.append((nr, nr + 1))

    # No ranges will overlap, so it's safe to sort by lower bound,
    # which sort() will do by default.
    range_list.sort()

    # Remove original letters in word list.
    for _ in range(s, i):
        del words[s]

    # Replace them with new word grouping.
    for j in range(len(range_list)):
        r = range_list[j]
        words.insert(s + j, acstr[r[0] : r[1]])

    return s + len(range_list) - 1


def _simple_acronym_detection(s: int, i: int, words: List[str], *args) -> int:
    """Detect acronyms based on runs of upper-case letters."""
    # Combine each letter into a single string.
    acstr = "".join(words[s:i])

    # Remove original letters in word list.
    for _ in range(s, i):
        del words[s]

    # Replace them with new word grouping.
    words.insert(s, "".join(acstr))

    return s


def _sanitize_acronyms(
    unsafe_acronyms: Union[List[str], Tuple[str], Tuple[str, str], str]
) -> List[str]:
    """Normalize valid acronyms to upper-case.

    If an invalid acronym is encountered (contains separators)
    raise InvalidAcronymError.
    """
    acronyms = []
    for a in unsafe_acronyms:
        if _is_valid_acronym(a):
            acronyms.append(a.upper())
        else:
            raise InvalidAcronymError(a)
    return acronyms


def _normalize_words(words: List[str], acronyms: Union[List[str], str]) -> List[str]:
    """Normalize case of each word to PascalCase."""
    for i, _ in enumerate(words):  # TODO: Rewrite loop without enumerate
        # if detect_acronyms:
        if words[i].upper() in acronyms:
            # Convert known acronyms to upper-case.
            words[i] = words[i].upper()
        else:
            # Fallback behavior: Preserve case on upper-case words.
            if not words[i].isupper():
                words[i] = words[i].capitalize()
    return words


def _segment_string(string: str) -> Tuple[List[Optional[str]], str, bool]:
    """Segment string on separator into list of words.

    Arguments:
        string -- the string we want to process
    Returns:
        words -- list of words the string got minced to
        separator -- the separator char intersecting words
        was_upper -- whether string happened to be upper-case
    """
    words: List[Optional[str]] = []
    separator = ""

    # curr_index of current character. Initially 1 because we don't
    # want to check if the 0th character is a boundary.
    curr_i = 1
    # Index of first character in a sequence
    seq_i = 0
    # Previous character.
    prev_i = string[0:1]

    # Treat an all-caps stringiable as lower-case, to prevent its
    # letters to be counted as boundaries
    was_upper = False
    if string.isupper():
        string = string.lower()
        was_upper = True

    # Iterate over each character, checking for boundaries, or places
    # where the stringiable should divided.
    while curr_i <= len(string):
        char = string[curr_i : curr_i + 1]
        split = False
        if curr_i < len(string):
            # Detect upper-case letter as boundary.
            if _char_is_upper(char):
                split = True
            # Detect transition from separator to not separator.
            elif not _char_is_sep(char) and _char_is_sep(prev_i):
                split = True
            # Detect transition not separator to separator.
            elif _char_is_sep(char) and not _char_is_sep(prev_i):
                split = True
        else:
            # The looprev_igoes one extra iteration so that it can
            # handle the remaining text after the last boundary.
            split = True

        if split:
            if not _char_is_sep(prev_i):
                words.append(string[seq_i:curr_i])
            else:
                # stringiable contains at least one separator.
                # Use the first one as the stringiable's primary separator.
                if not separator:
                    separator = string[seq_i : seq_i + 1]

                # Use None to indicate a separator in the word list.
                words.append(None)
                # If separators weren't included in the list, then breaks
                # between upper-case sequences ("AAA_BBB") would be
                # disregarded; the letter-run detector would count them
                # as a single sequence ("AAABBB").
            seq_i = curr_i

        curr_i += 1
        prev_i = char

    return words, separator, was_upper
