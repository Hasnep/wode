import pytest

from wode.parser import Parser
from wode.scanner import Scanner
from wode.tests.conftest import WodeTestCase, test_cases
from wode.transpiler import transpile_expression

success_cases = [x for x in test_cases if x.expected_output is not None]
failure_cases = [x for x in test_cases if x.expected_output is None]


@pytest.mark.parametrize(
    "success_case", success_cases, ids=[x.name for x in success_cases]
)
def test_transpiler(success_case: WodeTestCase):
    # Scan the source
    tokens, scanner_errors = Scanner(success_case.source).scan()

    # If there were any scanner errors, raise them
    if len(scanner_errors) > 0:
        raise Exception("Scanning errors were found in unit test for parser.")

    # Parse the tokens
    expressions, parser_errors = Parser(tokens, success_case.source).parse_all()

    # If there were any parser errors, raise them
    if len(parser_errors) > 0:
        raise Exception(
            "\n".join(
                ["Parsing errors found:"]
                + [error.get_message() for error in parser_errors]
            )
        )

    # # Check the transpiler works as expected
    # _transpiled_expressions = [
    #     transpile_expression(expression) for expression in expressions
    # ]
