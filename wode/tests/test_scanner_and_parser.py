from textwrap import dedent

import pytest

from wode.ast_to_s_expression import SExpression, convert_to_s_expression
from wode.errors import WodeError
from wode.parser import ParserState, parse_all
from wode.scanner import scan_all_tokens
from wode.source import Source
from wode.tests.conftest import SimplifiedToken, test_cases
from wode.types import List, Str, Type


@pytest.mark.parametrize(
    (
        "test_case_id",
        "source",
        "expected_tokens",
        "expected_scanner_error_types",
        "expected_s_expressions",
        "expected_parser_error_types",
    ),
    [
        pytest.param(
            tc.test_case_id,
            tc.source,
            tc.expected_tokens,
            tc.expected_scanner_error_types,
            tc.expected_s_expressions,
            tc.expected_parser_error_types,
            marks=[pytest.mark.xfail(tc.broken, reason="Test case is broken.")],
            id=tc.test_case_id,
        )
        for tc in test_cases
    ],
)
def test_test_cases(
    test_case_id: Str,
    source: Source,
    expected_tokens: List[SimplifiedToken],
    expected_scanner_error_types: List[Type[WodeError]],
    expected_s_expressions: List[SExpression],
    expected_parser_error_types: List[Type[WodeError]],
) -> None:
    # Scan the source
    tokens, scanner_errors = scan_all_tokens(source)

    # Test the tokens were scanned as expected
    tokens_simplified = [
        SimplifiedToken(token.token_type, token.lexeme) for token in tokens
    ]
    assert tokens_simplified == expected_tokens, dedent(
        f"""
        Test case `{test_case_id}` was expected to be scanned as these tokens:
        {[Str(t) for t in expected_tokens]}
        but it was scanned as:
        {[Str(t) for t in tokens_simplified]}
        """
    )

    # Extract the error types that were returned
    scanner_error_types = [type(e) for e in scanner_errors]
    # Test that the right errors were returned
    assert scanner_error_types == expected_scanner_error_types, dedent(
        f"""
        Expected test case `{test_case_id}` to return errors:
        {[Str(e) for e in expected_scanner_error_types]}
        but it returned:
        {[Str(e) for e in  scanner_error_types]}
        """
    )

    # Parse the tokens
    parsed_expressions, parser_errors = parse_all(ParserState(tokens, source))

    # Convert the expressions to s-expressions
    parsed_s_expressions = [convert_to_s_expression(e) for e in parsed_expressions]
    # Check the tokens were parsed as expected
    assert parsed_s_expressions == expected_s_expressions, dedent(
        f"""
        Expected test case `{test_case_id}` to be parsed as:
        {expected_s_expressions}
        but it was parsed as:
        {parsed_s_expressions}
        """
    )

    # Extract the error types that were returned
    parser_error_types = [type(e) for e in parser_errors]
    # Test that the right errors were returned
    assert parser_error_types == expected_parser_error_types, dedent(
        f"""
        Expected test case `{test_case_id}` to return errors:
        {[Str(e) for e in expected_parser_error_types]}
        but it returned:
        {[Str(e) for e in  parser_error_types]}
        """
    )
