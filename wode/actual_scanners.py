from wode.constants import DIGITS, LETTERS
from wode.scanner import (
    ScannerOutput,
    Source,
    get_any_literal_scanner,
    get_delimited_scanner,
    get_literal_scanner,
    get_sequence_scanner,
    get_while_is_any_literal_scanner,
    get_while_is_not_any_literal_scanner,
)


def scan_string(source: Source) -> ScannerOutput:
    return get_delimited_scanner(
        get_literal_scanner('"'),
        get_while_is_not_any_literal_scanner({'"'}),
        get_literal_scanner('"'),
    )(source)


def scan_comment(source: Source) -> ScannerOutput:
    return get_delimited_scanner(
        get_literal_scanner("#"),
        get_while_is_not_any_literal_scanner({"\n"}),
        get_literal_scanner("\n"),
    )(source)


def scan_identifier(source: Source) -> ScannerOutput:
    return get_sequence_scanner(
        [
            get_any_literal_scanner(LETTERS + ["_"]),
            get_while_is_any_literal_scanner(LETTERS + DIGITS + ["_"]),
        ]
    )(source)
