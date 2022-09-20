#!/usr/bin/env just --justfile

default: lock install format lint test example

lock:
    poetry lock --no-update

install:
    poetry install

format: ssort isort black

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
    poetry run python -m pytest wode

example:
    poetry run python -m wode ./example.wode
