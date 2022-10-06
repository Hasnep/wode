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
            parser = Parser(tokens)
            expressions = parser.parse()
            ast_printer = AstPrinter()
            for expression in expressions:
                rendered_expression = ast_printer.convert_to_s_expression(expression)
                print(rendered_expression)
                # match convert_ast(expression):
                #     case Ok(converted_expression):
                #         match unparse_go_expression(converted_expression):
                #             case Ok(unparsed_go_expression):
                #                 print(f"{unparsed_go_expression=}")
                #             case Err(message):
                #                 print(message)
                #     case Err(message):
                #         print(message)
        case Err(errors):
            for error in errors:
                print(error.message)
