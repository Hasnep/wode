import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Optional

from koda import Err, Ok

from wode.ast_printer import AstPrinter
from wode.parser import Parser
from wode.scanner import Scanner


def get_file_path() -> Optional[Path]:
    parser = ArgumentParser()
    parser.add_argument(
        "file_path",
        type=Path,
        default=None,
        nargs="?",
    )
    args = parser.parse_args()
    file_path: Optional[Path] = args.file_path
    return file_path


def main():
    file_path = get_file_path()
    if file_path is None:
        source = sys.stdin.read()
    else:
        with open(file_path, "r") as f:
            source = f.read()

    tokens_result = Scanner(source).scan()
    match tokens_result:
        case Ok(tokens):
            expressions, errors = Parser(tokens, source).parse_all()
            if len(errors) > 0:
                print("Parsing errors:")
                for error in errors:
                    print(error.get_message())
            else:
                for expression in expressions:
                    rendered_expression = AstPrinter().convert_to_s_expression(
                        expression
                    )
                    print(rendered_expression)
        case Err(errors):
            for error in errors:
                print(error.get_message())
