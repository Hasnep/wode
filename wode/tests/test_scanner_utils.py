import pytest
from koda import Just, Maybe, Nothing, nothing

from wode.scanner import (
    Source,
    chomp,
    get_literal_scanner,
    get_sequence_scanner,
    get_while_is_any_literal_scanner,
    get_while_is_not_any_literal_scanner,
    get_while_scanner,
    is_digit,
    is_letter,
)


def test_chomp():
    example_source = Source("my test source")
    output = chomp(example_source, 2)
    expected_output = ("my", Source(" test source", 2))
    assert isinstance(output, Just)
    assert output.val == expected_output


def test_chomp_returns_nothing_when_it_reaches_eof():
    source = Source("")
    assert chomp(source) == nothing


@pytest.mark.parametrize(
    ",".join(["source", "literal"]),
    [("This is my string.", "This"), (" hi ", " "), ("hello", "he")],
)
def test_get_literal_scanner(source: str, literal: str):
    scan_literal = get_literal_scanner(literal)
    output = scan_literal(Source(source))
    assert isinstance(output, Just)
    assert output.val[0] == literal


def test_get_literal_scanner_returns_nothing_when_no_match_is_found():
    source = Source("This is my string.")
    scan_literal = get_literal_scanner("hello")
    assert isinstance(scan_literal(source), Nothing)


def test_get_literal_scanner_returns_nothing_when_string_ends():
    source = Source("")
    scan_literal = get_literal_scanner("hello")
    assert isinstance(scan_literal(source), Nothing)


def test_get_while_scanner():
    source = Source("123xyz")
    scan_while_is_digit = get_while_scanner(lambda c: Just(is_digit(c)))
    output = scan_while_is_digit(source)
    assert isinstance(output, Just)
    assert output.val == ("123", Source("xyz", 3))


def test_get_while_is_any_literal_scanner():
    source = Source("cabbages")
    scan_abcdefg = get_while_is_any_literal_scanner(["a", "b", "c", "d", "e", "f", "g"])
    output = scan_abcdefg(source)
    assert isinstance(output, Just)
    assert output.val == ("cabbage", Source("s", 7))


def test_get_while_is_not_any_literal_scanner():
    source = Source("some words")
    scan_non_whitespace = get_while_is_not_any_literal_scanner({" ", "\t", "\n"})
    output = scan_non_whitespace(source)
    assert isinstance(output, Just)
    assert output.val == ("some", Source(" words", 4))


def test_get_sequence_scanner():
    source = Source("123&abc!")
    scan_sequence = get_sequence_scanner(
        [
            get_while_scanner(lambda c: Just(is_digit(c))),
            get_literal_scanner("&"),
            get_while_scanner(lambda c: Just(is_letter(c))),
        ]
    )
    output = scan_sequence(source)
    assert isinstance(output, Just)
    assert output.val == ("123&abc", Source("!", 7))


# def test_scan_delimited():
#     for left in ["[", "<--", "left"]:
#         for right in ["]", "-->", "right"]:
#             source = Source(left + "this is my thing" + right)
#             output = get_delimited_scanner(source, left, right)
#             assert isinstance(output, Just)
#             assert output.val == ("this is my thing", Source("", len(source.text)))
