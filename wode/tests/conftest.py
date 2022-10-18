from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, validator
from ruamel.yaml import YAML as Yaml

from wode.ast_to_s_expression import SExpression
from wode.errors import WodeErrorType
from wode.token_type import TokenType

DATA_FOLDER = Path(".") / "data"

SimplifiedToken = Tuple[TokenType, str]


class WodeTestCase(BaseModel):
    name: str
    source: str
    expected_tokens: List[SimplifiedToken] = []
    expected_errors: List[WodeErrorType] = []
    expected_ast: Optional[List[SExpression]]

    @validator("expected_tokens", pre=True, each_item=True)
    def parse_expected_tokens(cls, x: Dict[str, str]) -> SimplifiedToken:
        return (TokenType(x["token_type"]), x["lexeme"])

    @validator("expected_errors", pre=True, each_item=True)
    def parse_expected_errors(cls, x: str) -> WodeErrorType:
        return WodeErrorType(x)


def get_test_cases() -> List[WodeTestCase]:
    def _read_test_case(file_path: Path) -> WodeTestCase:
        print(f"Loading `{file_path}`.")
        with open(file_path, "r") as f:
            test_case_dict: Dict[str, Any] = yaml.load(f)  # type: ignore
        test_case_name = file_path.stem
        return WodeTestCase(name=test_case_name, **test_case_dict)

    yaml = Yaml()  # type: ignore
    test_case_file_paths = DATA_FOLDER.glob("**/*.yaml")
    return [_read_test_case(p) for p in test_case_file_paths]


test_cases = get_test_cases()
