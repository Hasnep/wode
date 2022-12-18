import pytest

from wode.ast_to_s_expression import convert_to_s_expression
from wode.parser import Parser
from wode.scanner import Scanner
from wode.tests.conftest import WodeTestCase, test_cases

success_cases = [x for x in test_cases if x.expected_ast is not None]
failure_cases = [x for x in test_cases if x.expected_ast is None]


@pytest.mark.parametrize(
    "success_case", success_cases, ids=[x.name for x in success_cases]
)
def test_parser(success_case: WodeTestCase):
    # Scan the source
    tokens, scanner_errors = Scanner(success_case.source).scan()

    # If there were any scanner errors, raise them
    if len(scanner_errors) > 0:
        raise Exception("Scanning errors were found in unit test for parser.")

    # Parse the tokens
    expressions, parser_errors = Parser(tokens, success_case.source).parse()

    # If there were any parser errors, raise them
    if len(parser_errors) > 0:
        raise Exception(
            "\n".join(
                ["Parsing errors found:"]
                + [error.get_message() for error in parser_errors]
            )
        )

    # Check the parser works as expected
    expected_ast = success_case.expected_ast
    if expected_ast is not None:
        assert [convert_to_s_expression(e) for e in expressions] == expected_ast

    if success_case.broken:
        pytest.xfail()
