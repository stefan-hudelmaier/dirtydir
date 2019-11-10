# -*- coding: utf-8 -*-

import pytest
from dirtydir.skeleton import fib

__author__ = "Stefan Hudelmaier"
__copyright__ = "Stefan Hudelmaier"
__license__ = "apache"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
