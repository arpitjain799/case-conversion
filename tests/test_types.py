from case_conversion import InvalidAcronymError


def test_invalid_acronym_error_message():
    acronym = "BadAcronym"
    msg = f"Case Conversion: acronym '{acronym}' is invalid."
    try:
        raise InvalidAcronymError(acronym)
    except InvalidAcronymError as e:
        assert msg in str(e)
