from textwrap import dedent

import pytest

from wode.ast_to_s_expression import convert_to_s_expression
from wode.parser import ParserState, parse_all
from wode.scanner import scan_all_tokens
from wode.tests.conftest import WodeTestCase, test_cases_flattened
from wode.token_type import TokenType


@pytest.mark.parametrize(
    ",".join(["test_case_id", "test_case"]),
    test_cases_flattened.items(),
    ids=list(test_cases_flattened.keys()),
)
def test_scanner_and_parser(test_case_id: str, test_case: WodeTestCase):
    if test_case.broken:
        pytest.xfail()

    source = test_case.source
    expected_tokens = test_case.expected_tokens
    expected_scanner_error_types = test_case.expected_scanner_error_types
    expected_ast = test_case.expected_ast
    del test_case

    # Scan the source
    tokens, scanner_errors = scan_all_tokens(source)

    # Extract the error types that were returned
    scanner_error_types = [type(e) for e in scanner_errors]

    if len(expected_scanner_error_types) == 0:
        assert len(scanner_error_types) == 0, (
            f"Test case `{test_case_id}` unexpectedly raised scanner error types: "
            + ", ".join([str(e) for e in scanner_error_types])
        )

        # Test the tokens were scanned as expected
        tokens_simplified = [(token.token_type, token.lexeme) for token in tokens]
        expected_tokens_simplified = [
            (token.token_type, token.lexeme) for token in expected_tokens
        ] + [(TokenType.EOF, "")]
        assert (
            tokens_simplified == expected_tokens_simplified
        ), f"Test case `{test_case_id}` was not scanned correctly."
    else:
        # If we expected scanner errors to be returned, test that the right errors were returned
        assert scanner_error_types == expected_scanner_error_types, dedent(
            f"""
            Expected test case `{test_case_id}` to return errors:
            {', '.join([str(e) for e in expected_scanner_error_types])}
            but it returned:
            {', '.join([str(e) for e in  scanner_error_types])}
            """
        )

    # If the test case doesn't have a valid AST then don't bother parsing it
    if expected_ast is None:
        return

    # Parse the tokens
    expressions, parser_errors = parse_all(ParserState(tokens, source))

    # Convert the expressions to s-expressions
    parsed_ast = [convert_to_s_expression(e) for e in expressions]

    # If there were any parser errors, raise them
    assert len(parser_errors) == 0, "\n".join(
        [f"Parsing errors found in test case `{test_case_id}`:"]
        + [error.get_message() for error in parser_errors]
    )

    # Check the parser works as expected
    assert parsed_ast == expected_ast, dedent(
        f"""
        Expected test case `{test_case_id}` to be parsed as:
        {expected_ast}
        but it was parsed as:
        {parsed_ast}
        """
    )
