from typing import Tuple

import pytest

from wode.ast_to_s_expression import convert_to_s_expression
from wode.parser import Parser
from wode.scanner import Scanner
from wode.tests.conftest import WodeTestCase, test_cases_flattened

success_cases = [
    (test_case_name, test_case)
    for test_case_name, test_case in test_cases_flattened
    if test_case.expected_ast is not None
]
failure_cases = [
    (test_case_name, test_case)
    for test_case_name, test_case in test_cases_flattened
    if test_case.expected_ast is None
]


@pytest.mark.parametrize(
    "success_case", success_cases, ids=[x[0] for x in success_cases]
)
def test_parser(success_case: Tuple[str, WodeTestCase]):
    if success_case[1].broken:
        pytest.xfail()

    test_case_name = success_case[0]
    source = success_case[1].source
    # Scan the source
    tokens, scanner_errors = Scanner(source).scan()

    # If there were any scanner errors, raise them
    if len(scanner_errors) > 0:
        raise Exception(
            f"Scanning errors were found in unit test `{test_case_name}` for parser."
        )

    # Parse the tokens
    expressions, parser_errors = Parser(tokens, source).parse()

    # If there were any parser errors, raise them
    if len(parser_errors) > 0:
        raise Exception(
            "\n".join(
                [f"Parsing errors found in test case `{test_case_name}`:"]
                + [error.get_message() for error in parser_errors]
            )
        )

    # Check the parser works as expected
    expected_ast = success_case[1].expected_ast
    if expected_ast is not None:
        assert [convert_to_s_expression(e) for e in expressions] == expected_ast
