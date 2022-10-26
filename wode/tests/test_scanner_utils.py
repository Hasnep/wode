from typing import List

import pytest
from koda import Just, Nothing, nothing

from wode.constants import DIGITS, LETTERS
from wode.scanner import (
    ScannerOutput,
    ScannerState,
    get_any_scanner,
    get_delimited_scanner,
    get_literal_scanner,
    get_one_or_more_of_any_literal_scanner,
    get_repeat_scanner,
    get_sequence_scanner,
    get_while_or_zero_characters_scanner,
    get_zero_or_more_of_any_literal_scanner,
    is_digit,
    is_letter,
)


@pytest.mark.parametrize(
    ",".join(
        [
            "state",
            "bite_size",
            "expected_bite",
            "expected_remaining_source",
            "expected_position",
        ]
    ),
    [
        (ScannerState("my test source"), 2, "my", " test source", 2),
        (ScannerState("another example", 8), 3, "exa", "mple", 11),
    ],
)
def test_chomp(
    state: ScannerState,
    bite_size: int,
    expected_bite: str,
    expected_remaining_source: str,
    expected_position: int,
):
    output = state.chomp(bite_size)
    assert isinstance(output, Just)
    assert output.val[0] == expected_bite
    assert output.val[1].remaining_source == expected_remaining_source
    assert output.val[1].position == expected_position


def test_chomp_returns_nothing_when_it_reaches_eof():
    source = ScannerState("")
    assert source.chomp() == nothing


@pytest.mark.parametrize(
    ",".join(["source", "literal"]),
    [("This is my string.", "This"), (" hi ", " "), ("hello", "he")],
)
def test_get_literal_scanner(source: str, literal: str):
    scan_literal = get_literal_scanner(literal)
    output = scan_literal(ScannerState(source))
    assert isinstance(output, Just)
    assert output.val[0] == literal


def test_get_literal_scanner_returns_nothing_when_no_match_is_found():
    source = ScannerState("This is my string.")
    scan_literal = get_literal_scanner("hello")
    assert isinstance(scan_literal(source), Nothing)


def test_get_literal_scanner_returns_nothing_when_string_ends():
    source = ScannerState("")
    scan_literal = get_literal_scanner("hello")
    assert isinstance(scan_literal(source), Nothing)


def test_get_while_scanner():
    source = ScannerState("123xyz")
    scan_while_is_digit = get_while_or_zero_characters_scanner(is_digit)
    output = scan_while_is_digit(source)
    assert isinstance(output, Just)
    assert output.val[0] == "123"


@pytest.mark.parametrize(
    ",".join(
        [
            "source",
            "list_of_literals",
            "expected_output_token",
            "expected_remaining_source",
        ]
    ),
    [
        ("cabbages", ["a", "b", "c", "d", "e", "f", "g"], "cabbage", "s"),
        ("123456abc", DIGITS, "123456", "abc"),
        ("abc!123", LETTERS, "abc", "!123"),
        ("123.", DIGITS, "123", "."),
        ("!£$.", DIGITS, "", "!£$."),
        ("!£$.", DIGITS, "", "!£$."),
    ],
)
def test_get_while_is_any_literal_scanner(
    source: str,
    list_of_literals: List[str],
    expected_output_token: str,
    expected_remaining_source: str,
):
    scanner = get_zero_or_more_of_any_literal_scanner(list_of_literals)
    output = scanner(ScannerState(source))
    assert isinstance(output, Just)
    assert output.val[0] == expected_output_token
    assert output.val[1].remaining_source == expected_remaining_source


def test_get_sequence_scanner():
    source = ScannerState("123&abc!")
    scan_sequence = get_sequence_scanner(
        [
            get_while_or_zero_characters_scanner(is_digit),
            get_literal_scanner("&"),
            get_while_or_zero_characters_scanner(is_letter),
        ]
    )
    output = scan_sequence(source)
    assert isinstance(output, Just)
    assert output.val[0] == "123&abc"
    assert output.val[1].remaining_source == "!"


@pytest.mark.parametrize(
    ",".join(["left", "right", "source"]),
    [
        (left, right, left + "this is my thing" + right)
        for left in ["[", "<--", "left"]
        for right in ["]", "-->", "right"]
    ],
)
def test_get_delimited_scanner(left: str, right: str, source: str):
    output = get_delimited_scanner(
        get_literal_scanner(left),
        get_while_or_zero_characters_scanner(lambda c: c != right[0]),
        get_literal_scanner(right),
    )(ScannerState(source))
    assert isinstance(output, Just)
    assert output.val[0] == ("this is my thing")
    assert output.val[1].remaining_source == ""


def test_get_repeat_scanner():
    source = ScannerState(":):):):(:)")
    repeated_smiley_scanner = get_repeat_scanner(get_literal_scanner(":)"))
    output = repeated_smiley_scanner(source)
    assert isinstance(output, Just)
    assert output.val[0] == ":):):)"
    assert output.val[1].remaining_source == ":(:)"


@pytest.mark.parametrize("source", ["hi.", "123.", "!£$."])
def test_get_any_scanner(source: str):
    sub_scanner_1 = get_literal_scanner("hi")
    sub_scanner_2 = get_one_or_more_of_any_literal_scanner(DIGITS)
    sub_scanner_3 = get_one_or_more_of_any_literal_scanner(["!", "£", "$"])
    sub_scanners = [sub_scanner_1, sub_scanner_2, sub_scanner_3]
    scanner = get_any_scanner(sub_scanners)
    output = scanner(ScannerState(source))
    assert isinstance(output, Just)
    assert output.val[0] == source[:-1]
    assert output.val[1].remaining_source == "."
