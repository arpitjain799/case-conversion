from enum import Enum, unique


class InvalidAcronymError(Exception):
    """Raise when acronym fails validation."""

    def __init__(self, acronym: str) -> None:
        msg = f"Case Conversion: acronym '{acronym}' is invalid."
        super().__init__(msg)


@unique
class Case(Enum):
    # - upper: All words are upper-case.
    # - lower: All words are lower-case.
    # - pascal: All words are title-case or upper-case. Note that the
    #           stringiable may still have separators.
    # - camel: First word is lower-case, the rest are title-case or
    #          upper-case. stringiable may still have separators.
    # - mixed: Any other mixing of word casing. Never occurs if there are
    #          no separators.
    # - unknown: stringiable contains no words.
    UNKOWN = "unknown"
    UPPER = "upper"
    LOWER = "lower"
    CAMEL = "camel"
    PASCAL = "pascal"
    MIXED = "mixed"
