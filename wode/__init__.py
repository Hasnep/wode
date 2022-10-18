from pathlib import Path

import typer

from wode.ast_to_s_expression import convert_to_s_expression
from wode.parser import Parser
from wode.scanner import Scanner

cli = typer.Typer(add_completion=False)


@cli.command()
def main(source_file_path: Path = typer.Argument(None, dir_okay=False)):
    # Read source from file
    with open(source_file_path, "r") as f:
        source = f.read()

    # Scan the source code into tokens
    tokens, scanning_errors = Scanner(source).scan()

    # If there were any scanning errors, raise them
    if len(scanning_errors) > 0:
        for error in scanning_errors:
            error_message = error.get_message()
            print(error_message)

    else:
        # Parse the tokens into an AST
        expressions, errors = Parser(tokens, source).parse_all()

        # If there were any parsing errors, raise them
        if len(errors) > 0:
            print("Parsing errors:")
            for error in errors:
                error_message = error.get_message()
                print(error_message)
        else:
            print("Parsed AST:")
            for expression in expressions:
                s_expression = convert_to_s_expression(expression)
                print(s_expression)
