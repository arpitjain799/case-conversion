# -*- coding: utf-8 -*-
"""Unit test for case-conversion
"""

from case_conversion import CaseConverter
from unittest import TestCase
from parameterized import parameterized

ACRONYMS = ['HTTP']
ACRONYMS_UNICODE = [u'HÉÉP']

CASES = [
    'camel',
    'pascal',
    'snake',
    'dash',
    'spinal',
    'dash',
    'const',
    'const',
    'dot',
]

CASES_PRESERVE = [
    'separate_words',
    'slash',
    'backslash',
]

VALUES = {
    'camel': 'fooBarString',
    'pascal': 'FooBarString',
    'snake': 'foo_bar_string',
    'dash': 'foo-bar-string',
    'spinal': 'foo-bar-string',
    'dash': 'foo-bar-string',
    'const': 'FOO_BAR_STRING',
    'const': 'FOO_BAR_STRING',
    'dot': 'foo.bar.string',
    'separate_words': 'foo bar string',
    'slash': 'foo/bar/string',
    'backslash': 'foo\\bar\\string',
}

VALUES_UNICODE = {
    'camel': u'fóoBarString',
    'pascal': u'FóoBarString',
    'snake': u'fóo_bar_string',
    'dash': u'fóo-bar-string',
    'spinal': u'fóo-bar-string',
    'dash': u'fóo-bar-string',
    'const': u'FÓO_BAR_STRING',
    'const': u'FÓO_BAR_STRING',
    'dot': u'fóo.bar.string',
    'separate_words': u'fóo bar string',
    'slash': u'fóo/bar/string',
    'backslash': u'fóo\\bar\\string',
}

VALUES_SINGLE = {
    'camel': 'foo',
    'pascal': 'Foo',
    'snake': 'foo',
    'dash': 'foo',
    'spinal': 'foo',
    'dash': 'foo',
    'const': 'FOO',
    'const': 'FOO',
    'dot': 'foo',
    'separate_words': 'foo',
    'slash': 'foo',
    'backslash': 'foo',
}

VALUES_SINGLE_UNICODE = {
    'camel': u'fóo',
    'pascal': u'Fóo',
    'snake': u'fóo',
    'dash': u'fóo',
    'spinal': u'fóo',
    'dash': u'fóo',
    'const': u'FÓO',
    'const': u'FÓO',
    'dot': u'fóo',
    'separate_words': u'fóo',
    'slash': u'fóo',
    'backslash': u'fóo',
}

VALUES_ACRONYM = {
    'camel': 'fooHTTPBarString',
    'pascal': 'FooHTTPBarString',
    'snake': 'foo_http_bar_string',
    'dash': 'foo-http-bar-string',
    'spinal': 'foo-http-bar-string',
    'dash': 'foo-http-bar-string',
    'const': 'FOO_HTTP_BAR_STRING',
    'const': 'FOO_HTTP_BAR_STRING',
    'dot': 'foo.http.bar.string',
    'separate_words': 'foo http bar string',
    'slash': 'foo/http/bar/string',
    'backslash': 'foo\\http\\bar\\string',
}

VALUES_ACRONYM_UNICODE = {
    'camel': u'fooHÉÉPBarString',
    'pascal': u'FooHÉÉPBarString',
    'snake': u'foo_héép_bar_string',
    'dash': u'foo-héép-bar-string',
    'spinal': u'foo-héép-bar-string',
    'dash': u'foo-héép-bar-string',
    'const': u'FOO_HÉÉP_BAR_STRING',
    'const': u'FOO_HÉÉP_BAR_STRING',
    'dot': u'foo.héép.bar.string',
    'separate_words': u'foo héép bar string',
    'slash': u'foo/héép/bar/string',
    'backslash': u'foo\\héép\\bar\\string',
}

PRESERVE_VALUES = {
    'separate_words': {'camel': 'foo Bar String',
                       'pascal': 'Foo Bar String',
                       'const': 'FOO BAR STRING',
                       'const': 'FOO BAR STRING',
                       'default': 'foo bar string'},
    'slash': {'camel': 'foo/Bar/String',
                  'pascal': 'Foo/Bar/String',
                  'const': 'FOO/BAR/STRING',
                  'const': 'FOO/BAR/STRING',
                  'default': 'foo/bar/string'},
    'backslash': {'camel': 'foo\\Bar\\String',
                      'pascal': 'Foo\\Bar\\String',
                      'const': 'FOO\\BAR\\STRING',
                      'const': 'FOO\\BAR\\STRING',
                      'default': 'foo\\bar\\string'},
}

PRESERVE_VALUES_UNICODE = {
    'separate_words': {'camel': u'fóo Bar String',
                       'pascal': u'Fóo Bar String',
                       'const': u'FÓO BAR STRING',
                       'const': u'FÓO BAR STRING',
                       'default': u'fóo bar string'},
    'slash': {'camel': u'fóo/Bar/String',
                  'pascal': u'Fóo/Bar/String',
                  'const': u'FÓO/BAR/STRING',
                  'const': u'FÓO/BAR/STRING',
                  'default': u'fóo/bar/string'},
    'backslash': {'camel': u'fóo\\Bar\\String',
                      'pascal': u'Fóo\\Bar\\String',
                      'const': u'FÓO\\BAR\\STRING',
                      'const': u'FÓO\\BAR\\STRING',
                      'default': u'fóo\\bar\\string'},
}

PRESERVE_VALUES_SINGLE = {
    'separate_words': {'camel': 'foo',
                       'pascal': 'Foo',
                       'const': 'FOO',
                       'const': 'FOO',
                       'default': 'foo'},
    'slash': {'camel': 'foo',
                  'pascal': 'Foo',
                  'const': 'FOO',
                  'const': 'FOO',
                  'default': 'foo'},
    'backslash': {'camel': 'foo',
                      'pascal': 'Foo',
                      'const': 'FOO',
                      'const': 'FOO',
                      'default': 'foo'},
}

PRESERVE_VALUES_SINGLE_UNICODE = {
    'separate_words': {'camel': u'fóo',
                       'pascal': u'Fóo',
                       'const': u'FÓO',
                       'const': u'FÓO',
                       'default': u'fóo'},
    'slash': {'camel': u'fóo',
                  'pascal': u'Fóo',
                  'const': u'FÓO',
                  'const': u'FÓO',
                  'default': u'fóo'},
    'backslash': {'camel': u'fóo',
                      'pascal': u'Fóo',
                      'const': u'FÓO',
                      'const': u'FÓO',
                      'default': u'fóo'},
}

PRESERVE_VALUES_ACRONYM = {
    'separate_words': {'camel': 'foo HTTP Bar String',
                       'pascal': 'Foo HTTP Bar String',
                       'const': 'FOO HTTP BAR STRING',
                       'const': 'FOO HTTP BAR STRING',
                       'default': 'foo http bar string'},
    'slash': {'camel': 'foo/HTTP/Bar/String',
                  'pascal': 'Foo/HTTP/Bar/String',
                  'const': 'FOO/HTTP/BAR/STRING',
                  'const': 'FOO/HTTP/BAR/STRING',
                  'default': 'foo/http/bar/string'},
    'backslash': {'camel': 'foo\\HTTP\\Bar\\String',
                      'pascal': 'Foo\\HTTP\\Bar\\String',
                      'const': 'FOO\\HTTP\\BAR\\STRING',
                      'const': 'FOO\\HTTP\\BAR\\STRING',
                      'default': 'foo\\http\\bar\\string'},
}

PRESERVE_VALUES_ACRONYM_UNICODE = {
    'separate_words': {'camel': u'foo HÉÉP Bar String',
                       'pascal': u'Foo HÉÉP Bar String',
                       'const': u'FOO HÉÉP BAR STRING',
                       'const': u'FOO HÉÉP BAR STRING',
                       'default': u'foo héép bar string'},
    'slash': {'camel': u'foo/HÉÉP/Bar/String',
                  'pascal': u'Foo/HÉÉP/Bar/String',
                  'const': u'FOO/HÉÉP/BAR/STRING',
                  'const': u'FOO/HÉÉP/BAR/STRING',
                  'default': u'foo/héép/bar/string'},
    'backslash': {'camel': u'foo\\HÉÉP\\Bar\\String',
                      'pascal': u'Foo\\HÉÉP\\Bar\\String',
                      'const': u'FOO\\HÉÉP\\BAR\\STRING',
                      'const': u'FOO\\HÉÉP\\BAR\\STRING',
                      'default': u'foo\\héép\\bar\\string'},
}


PRESERVE_VALUES_ACRONYM_SINGLE = {
    'separate_words': {'camel': 'HTTP',
                       'pascal': 'HTTP',
                       'const': 'HTTP',
                       'const': 'HTTP',
                       'default': 'http'},
    'slash': {'camel': 'HTTP',
                  'pascal': 'HTTP',
                  'const': 'HTTP',
                  'const': 'HTTP',
                  'default': 'http'},
    'backslash': {'camel': 'HTTP',
                      'pascal': 'HTTP',
                      'const': 'HTTP',
                      'const': 'HTTP',
                      'default': 'http'},
}

CAPITAL_CASES = [
    'camel',
    'pascal',
    'const',
    'const',
]


def _expand_values(values):
    test_params = []
    for case in CASES:
        test_params.extend([
            (name + '2' + case,
             case,
             value,
             values[case]) for name, value in values.items()
        ])
        test_params.append((case + '_empty', case, '', ''))
    return test_params


def _expand_values_preserve(preserve_values, values):
    test_params = []
    for case in CASES_PRESERVE:
        test_params.extend([
            (name + '2' + case,
             case,
             value,
             preserve_values[case][name if name in CAPITAL_CASES else 'default'])  # nopep8
            for name, value in values.items()
        ])
        test_params.append((case + '_empty', case, '', ''))
    return test_params


class CaseConversionTest(TestCase):
    @parameterized.expand(_expand_values(VALUES))
    def test(self, _, case, value, expected):
        """
        Test conversions from all cases to all cases that don't preserve
        capital/lower case letters.
        """
        case_converter = getattr(CaseConverter, case)
        self.assertEqual(case_converter(value), expected)

    @parameterized.expand(_expand_values(VALUES_UNICODE))
    def test_unicode(self, _, case, value, expected):
        """
        Test conversions from all cases to all cases that don't preserve
        capital/lower case letters (with unicode characters).
        """
        case_converter = getattr(CaseConverter, case)
        self.assertEqual(case_converter(value), expected)

    @parameterized.expand(_expand_values(VALUES_SINGLE))
    def test_single(self, _, case, value, expected):
        """
        Test conversions of single words from all cases to all cases that
        don't preserve capital/lower case letters.
        """
        case_converter = getattr(CaseConverter, case)
        self.assertEqual(case_converter(value), expected)

    @parameterized.expand(_expand_values(VALUES_SINGLE_UNICODE))
    def test_single_unicode(self, _, case, value, expected):
        """
        Test conversions of single words from all cases to all cases that
        don't preserve capital/lower case letters (with unicode characters).
        """
        case_converter = getattr(CaseConverter, case)
        self.assertEqual(case_converter(value), expected)

    @parameterized.expand(_expand_values_preserve(PRESERVE_VALUES, VALUES))
    def test_preserve_case(self, _, case, value, expected):
        """
        Test conversions from all cases to all cases that do preserve
        capital/lower case letters.
        """
        case_converter = getattr(CaseConverter, case)
        self.assertEqual(case_converter(value), expected)

    @parameterized.expand(
        _expand_values_preserve(PRESERVE_VALUES_UNICODE, VALUES_UNICODE))
    def test_preserve_case_unicode(self, _, case, value, expected):
        """
        Test conversions from all cases to all cases that do preserve
        capital/lower case letters (with unicode characters).
        """
        case_converter = getattr(CaseConverter, case)
        self.assertEqual(case_converter(value), expected)

    @parameterized.expand(
        _expand_values_preserve(PRESERVE_VALUES_SINGLE, VALUES_SINGLE))
    def test_preserve_case_single(self, _, case, value, expected):
        """
        Test conversions of single words from all cases to all cases that do
        preserve capital/lower case letters.
        """
        case_converter = getattr(CaseConverter, case)
        self.assertEqual(case_converter(value), expected)

    @parameterized.expand(
        _expand_values_preserve(PRESERVE_VALUES_SINGLE_UNICODE,
                                VALUES_SINGLE_UNICODE))
    def test_preserve_case_single_unicode(self, _, case, value, expected):
        """
        Test conversions of single words from all cases to all cases that do
        preserve capital/lower case letters (with unicode characters).
        """
        case_converter = getattr(CaseConverter, case)
        self.assertEqual(case_converter(value), expected)

    @parameterized.expand(_expand_values(VALUES_ACRONYM))
    def test_acronyms(self, _, case, value, expected):
        """
        Test conversions from all cases to all cases that don't preserve
        capital/lower case letters (with acronym detection).
        """
        case_converter = getattr(CaseConverter, case)
        result = case_converter(value, acronyms=ACRONYMS)
        self.assertEqual(result, expected)

    @parameterized.expand(_expand_values(VALUES_ACRONYM_UNICODE))
    def test_acronyms_unicode(self, _, case, value, expected):
        """
        Test conversions from all cases to all cases that don't preserve
        capital/lower case letters (with acronym detection and unicode
        characters).
        """
        case_converter = getattr(CaseConverter, case)
        result = case_converter(value, acronyms=ACRONYMS_UNICODE)
        self.assertEqual(result, expected)

    @parameterized.expand(
        _expand_values_preserve(PRESERVE_VALUES_ACRONYM, VALUES_ACRONYM))
    def test_acronyms_preserve_case(self, _, case, value, expected):
        """
        Test conversions from all cases to all cases that do preserve
        capital/lower case letters (with acronym detection).
        """
        case_converter = getattr(CaseConverter, case)
        result = case_converter(value, acronyms=ACRONYMS)
        self.assertEqual(result, expected)

    @parameterized.expand(
        _expand_values_preserve(PRESERVE_VALUES_ACRONYM_UNICODE,
                                VALUES_ACRONYM_UNICODE))
    def test_acronyms_preserve_case_unicode(self, _, case, value, expected):
        """
        Test conversions from all cases to all cases that do preserve
        capital/lower case letters (with acronym detection and unicode
        characters).
        """
        case_converter = getattr(CaseConverter, case)
        result = case_converter(value, acronyms=ACRONYMS_UNICODE)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    from unittest import main

    main()
