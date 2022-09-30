from pathlib import Path
from typing import Any, Dict, List, Tuple

from pydantic import BaseModel, validator
from ruamel.yaml import YAML as Yaml

from wode.errors import WodeErrorType
from wode.token import Token
from wode.token_type import TokenType


class AbstractTestCase(BaseModel):
    name: str
    source: str


class SuccessCase(AbstractTestCase):
    expected_tokens: List[Token]

    @validator("expected_tokens", each_item=True, pre=True)
    def parse_expected_tokens(cls, x: Dict[str, str]) -> Token:
        return Token(TokenType(x["token_type"]), x["lexeme"])


class FailureCase(AbstractTestCase):
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
