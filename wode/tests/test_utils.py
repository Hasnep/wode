import pytest

from wode.utils import is_digit, is_letter, is_whitespace, safe_slice, safe_substring


def test_is_letter():
    assert is_letter("a")
    assert is_letter("A")
    assert not is_letter("1")
    assert not is_letter("!")


def test_is_digit():
    assert is_digit("1")
    assert not is_digit("a")


def test_is_whitespace():
    assert is_whitespace(" ")
    assert is_whitespace("\t")
    assert is_whitespace("\n")
    assert not is_whitespace("a")


def test_safe_slice():
    assert safe_slice(["a", "b", "c"], begin=1, end=2) == ["b"]
    assert safe_slice(["a", "b", "c"], begin=1, length=1) == ["b"]
    with pytest.raises(IndexError):
        safe_slice(["a", "b", "c"], begin=2, end=10)
    with pytest.raises(IndexError):
        safe_slice(["a", "b", "c"], begin=2, length=10)
    with pytest.raises(ValueError):
        safe_slice(["a", "b", "c"], begin=2)
    with pytest.raises(ValueError):
        safe_slice(["a", "b", "c"], begin=2, length=1, end=3)


def test_safe_substring():
    assert safe_substring("abc", begin=1, end=2) == "b"
    assert safe_substring("abc", begin=1, length=1) == "b"
