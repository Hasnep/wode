import pytest
from koda import Err, Ok

from wode.ast_printer import AstPrinter
from wode.parser import Parser
from wode.scanner import Scanner
from wode.tests.conftest import WodeTestCase, test_cases

success_cases = [x for x in test_cases if x.expected_ast is not None]
failure_cases = [x for x in test_cases if x.expected_ast is None]


@pytest.mark.parametrize(
    "success_case", success_cases, ids=[x.name for x in success_cases]
)
def test_parser(success_case: WodeTestCase):
    scanner = Scanner(success_case.source)
    match scanner.scan():
        case Ok(tokens):
            expressions, errors = Parser(tokens, success_case.source).parse_all()
            if len(errors) > 0:
                raise Exception(
                    "\n".join(
                        ["Parsing errors found:"]
                        + [error.get_message() for error in errors]
                    )
                )
            expected_ast = success_case.expected_ast
            if expected_ast is not None:
                assert [
                    AstPrinter().convert_to_s_expression(e) for e in expressions
                ] == [sexpr.strip() for sexpr in expected_ast]
        case Err(wode_errors):
            raise Exception(wode_errors)
