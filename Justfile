#!/usr/bin/env just --justfile

default: lock install format lint test build_ocaml example run_ocaml

lock:
    poetry lock --no-update

install:
    poetry install

format: ssort isort black fmt_ocaml

lint: flake8 pyright

test: pytest

ssort:
    poetry run python -m ssort wode

isort:
    poetry run python -m isort wode

black:
    poetry run python -m black wode

flake8:
    poetry run python -m flake8 wode

pyright:
    poetry run python -m pyright wode

pytest:
    poetry run python -m pytest -vv wode

coverage:
    poetry run python -m http.server --directory=htmlcov

example:
    poetry run python -m wode run example.wode

run_ocaml:
    opam exec dune exec wode

build_ocaml:
    opam exec dune build

fmt_ocaml:
    opam exec dune fmt -- --diff-command=delta
