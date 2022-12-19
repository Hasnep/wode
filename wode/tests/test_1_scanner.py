from typing import Tuple

import pytest

from wode.scanner import Scanner
from wode.tests.conftest import WodeTestCase, test_cases_flattened
from wode.token_type import TokenType

success_cases = [
    (test_case_name, test_case)
    for test_case_name, test_case in test_cases_flattened
    if len(test_case.expected_errors) == 0
]
failure_cases = [
    (test_case_name, test_case)
    for test_case_name, test_case in test_cases_flattened
    if len(test_case.expected_errors) > 0
]


@pytest.mark.parametrize(
    "success_case", success_cases, ids=[x[0] for x in success_cases]
)
def test_scanner_parses_test_cases(success_case: Tuple[str, WodeTestCase]):
    test_case_name = success_case[0]
    source = success_case[1].source
    expected_tokens = success_case[1].expected_tokens

    # Scan the source
    tokens, errors = Scanner(source).scan()

    # If there were any scanning errors, raise them
    if len(errors) > 0:
        raise Exception("\n".join([error.get_message() for error in errors]))

    # Test the tokens were scanned as expected
    tokens_simplified = [(token.token_type, token.lexeme) for token in tokens]
    expected_tokens_simplified = [
        (token.token_type, token.lexeme) for token in expected_tokens
    ] + [(TokenType.EOF, "")]
    assert (
        tokens_simplified == expected_tokens_simplified
    ), f"Test case `{test_case_name}` was not scanned correctly."

    if success_case[1].broken:
        pytest.xfail()


@pytest.mark.parametrize(
    "failure_case", failure_cases, ids=[x[0] for x in failure_cases]
)
def test_scanner_fails_on_failure_cases(failure_case: Tuple[str, WodeTestCase]):
    test_case_name = failure_case[0]
    source = failure_case[1].source
    expected_error_types = failure_case[1].expected_errors

    _tokens, errors = Scanner(source).scan()

    if len(errors) == 0:
        raise ValueError(
            f"Expected test case `{test_case_name}` to return a `{expected_error_types}` error."
        )
    if len(errors) > 1:
        raise Exception("Too many errors were raised.")

    assert (
        errors[0].error_type == expected_error_types[0]
    ), f"Test case `{test_case_name}` should have returned `{expected_error_types}` error."

    if failure_case[1].broken:
        pytest.xfail()
