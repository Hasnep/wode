#!/usr/bin/env just --justfile

default: lock install format lint test dune_build example

lock:
    poetry lock --no-update

install:
    poetry install

format: format_python dune_fmt

format_python: ssort isort black

lint: flake8 pyright

test: pytest dune_test

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

dune_build:
    opam exec dune build

dune_fmt:
    -opam exec dune fmt

dune_test:
    opam exec dune test

example:
    opam exec dune exec wode -- ./example.wode
