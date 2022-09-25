from pathlib import Path
from typing import Any, Dict, List, Tuple

import pytest
from koda import Err, Ok
from pydantic import BaseModel, validator
from ruamel.yaml import YAML as Yaml

from wode.errors import WodeErrorType
from wode.scanner import Scanner
from wode.token import Token
from wode.token_type import TokenType


class TestCase(BaseModel):
    name: str
    source: str


class SuccessCase(TestCase):
    expected_tokens: List[Token]

    @validator("expected_tokens", each_item=True, pre=True)
    def parse_expected_tokens(cls, x: Dict[str, str]) -> Token:
        return Token(TokenType(x["token_type"]), x["lexeme"])


class FailureCase(TestCase):
    expected_errors: List[WodeErrorType]

    @validator("expected_errors", each_item=True, pre=True)
    def parse_expected_errors(cls, x: str) -> WodeErrorType:
        return WodeErrorType(x)


def get_test_cases() -> Tuple[List[SuccessCase], List[FailureCase]]:
    yaml = Yaml()  # type: ignore
    with open(Path(".") / "data" / "test_cases.yaml", "r") as f:
        test_cases_dict: Dict[str, Any] = yaml.load(f)  # type: ignore
    test_cases = [{"name": name, **data} for name, data in test_cases_dict.items()]
    return (
        [
            SuccessCase(**test_case)  # type: ignore
            for test_case in test_cases
            if "expected_tokens" in test_case
        ],
        [
            FailureCase(**test_case)  # type: ignore
            for test_case in test_cases
            if "expected_errors" in test_case
        ],
    )


success_cases, failure_cases = get_test_cases()


@pytest.mark.parametrize(
    "success_case", success_cases, ids=[x.name for x in success_cases]
)
def test_scanner_parses_test_cases(success_case: SuccessCase):
    test_case_name = success_case.name
    source = success_case.source
    expected_tokens = success_case.expected_tokens

    tokens_result = Scanner(source).scan()
    match tokens_result:
        case Ok(tokens):
            assert tokens == [
                *expected_tokens,
                Token(TokenType.EOF, ""),
            ], f"Test case `{test_case_name}` was not scanned correctly."
        case Err(wode_errors):
            for e in wode_errors:
                raise Exception(e.message)


@pytest.mark.parametrize(
    "failure_case", failure_cases, ids=[x.name for x in failure_cases]
)
def test_scanner_fails_on_failure_cases(failure_case: FailureCase):
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
