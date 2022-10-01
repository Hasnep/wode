import pytest
from koda import Err, Ok

from wode.scanner import Scanner
from wode.tests.conftest import WodeTestCase, test_cases
from wode.token import Token
from wode.token_type import TokenType

success_cases = [x for x in test_cases if len(x.expected_errors) == 0]
failure_cases = [x for x in test_cases if len(x.expected_errors) > 0]


@pytest.mark.parametrize(
    "success_case", success_cases, ids=[x.name for x in success_cases]
)
def test_scanner_parses_test_cases(success_case: WodeTestCase):
    test_case_name = success_case.name
    source = success_case.source
    expected_tokens = success_case.expected_tokens

    tokens_result = Scanner(source).scan()
    match tokens_result:
        case Ok(tokens):
            assert tokens == (
                expected_tokens + [Token(TokenType.EOF, "")]
            ), f"Test case `{test_case_name}` was not scanned correctly."
        case Err(wode_errors):
            for e in wode_errors:
                raise Exception(e.message)


@pytest.mark.parametrize(
    "failure_case", failure_cases, ids=[x.name for x in failure_cases]
)
def test_scanner_fails_on_failure_cases(failure_case: WodeTestCase):
    test_case_name = failure_case.name
    source = failure_case.source
    expected_error_types = failure_case.expected_errors

    tokens_result = Scanner(source).scan()
    match tokens_result:
        case Ok(_):
            raise ValueError(
                f"Expected test case `{test_case_name}` to return a `{expected_error_types}` error."
            )
        case Err(wode_errors):
            if len(wode_errors) > 1:
                raise Exception("Too many errors were raised.")
            assert (
                wode_errors[0].error_type == expected_error_types[0]
            ), f"Test case `{test_case_name}` should have returned `{expected_error_types}` error."
