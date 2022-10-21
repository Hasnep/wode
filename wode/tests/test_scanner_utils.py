from koda import Just, Maybe, nothing

from wode.scanner import (
    Source,
    chomp,
    is_digit,
    scan_delimited,
    scan_literal,
    scan_while_callback,
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


def test_scan_literal():
    source = Source("This is my string.")
    literals = ["This", " ", "is"]
    for literal in literals:
        match scan_literal(source, literal):
            case Just((bite, remaining_source)):
                assert bite == literal
                source = remaining_source
            case _:
                raise ValueError(
                    f"Unexpected failure scanning for `{literal}` in `{source.text}`."
                )


def test_scan_while_callback():
    source = Source("123xyz")

    def are_all_digits(s: str) -> Maybe[bool]:
        if len(s) == 0:
            return nothing
        return Just(all(is_digit(c) for c in s))

    output = scan_while_callback(source, are_all_digits)

    assert isinstance(output, Just)
    assert output.val == ("123", Source("xyz", 3))


def test_scan_delimited():
    for left in ["[", "<--", "left"]:
        for right in ["]", "-->", "right"]:
            source = Source(left + "this is my thing" + right)
            output = scan_delimited(source, left, right)
            assert isinstance(output, Just)
            assert output.val == ("this is my thing", Source("", len(source.text)))
