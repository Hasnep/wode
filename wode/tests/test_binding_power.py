import pytest

from wode.binding_power import get_infix_binding_power, get_prefix_binding_power
from wode.token_type import TokenType
from wode.types import Float


def test_get_infix_binding_power_gets_binding_power():
    left, right = get_infix_binding_power(TokenType.PLUS)
    assert isinstance(left, Float)
    assert isinstance(right, Float)


def test_get_infix_binding_power_errors_for_invalid_tokens():
    with pytest.raises(ValueError):
        get_infix_binding_power(TokenType.COMMENT)


def test_get_prefix_binding_power_gets_binding_power():
    left, right = get_prefix_binding_power(TokenType.PLUS)
    assert left is None
    assert isinstance(right, Float)


def test_get_prefix_binding_power_errors_for_invalid_tokens():
    with pytest.raises(ValueError):
        get_prefix_binding_power(TokenType.COMMENT)
