import importlib.metadata
from pathlib import Path

from wode.ast_to_s_expression import convert_to_s_expression
from wode.parser import ParserState, parse_all
from wode.scanner import scan_all_tokens
from wode.source import Source

__version__ = importlib.metadata.version("wode")


def show_version():
    print(__version__)


def main(source_file_path: Path | str):
    # Read the source code from the specified file
    with open(source_file_path, "r") as f:
        source = Source(Path(source_file_path), f.read())

    # Scan the source code into tokens
    tokens, scanner_errors = scan_all_tokens(source)

    # If there were any scanning errors, show them and stop execution
    if len(scanner_errors) > 0:
        print("Scanning errors:")
        for error in scanner_errors:
            print(error.get_message())
        return

    # Parse the tokens into an AST
    expressions, parsing_errors = parse_all(ParserState(tokens, source))

    # If there were any parsing errors, show them and stop execution
    if len(parsing_errors) > 0:
        print("Parsing errors:")
        for error in parsing_errors:
            print(error.get_message())
        return

    print("Parsed AST:")
    for expression in expressions:
        s_expression = convert_to_s_expression(expression)
        print(s_expression)
