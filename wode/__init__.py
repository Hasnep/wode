import importlib.metadata
from pathlib import Path

import typer

from wode.ast_to_s_expression import convert_to_s_expression
from wode.parser import Parser
from wode.scanner import scan_all_tokens

__version__ = importlib.metadata.version("wode")


cli = typer.Typer(add_completion=False)


@cli.command("version")
def show_version():
    print(__version__)


@cli.command("run")
def main(source_file_path: Path = typer.Argument(None, dir_okay=False)):
    # Read the source code from the specified file
    with open(source_file_path, "r") as f:
        source = f.read()

    # Scan the source code into tokens
    tokens, scanner_errors = scan_all_tokens(source)

    # If there were any scanning errors, show them and stop execution
    if len(scanner_errors) > 0:
        print("Scanning errors:")
        for error in scanner_errors:
            print(error.get_message())
        return

    # Parse the tokens into an AST
    expressions, parsing_errors = Parser(tokens, source).parse()

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
