import random
from uuid import uuid1
import pytest
from typing import Callable, TypeVar


T = TypeVar('T', str, int, float, bool, bytes)


@pytest.fixture
def generate_val() -> Callable[..., T]:
    """
    generates a random value of given types
    if type is not given, it generates any type
    """
    def _generator(*types: type) -> T:
        ttype = random.choice(types or T.__constraints__)
        uuid = uuid1(random.randint(0, 32))

        if ttype is str:
            return uuid.hex[:uuid.node]
        if ttype is bytes:
            return uuid.bytes[:uuid.node]
        if ttype is bool:
            return uuid.node >= 16
        return uuid.node + (ttype is float and random.random())
    return _generator


def not_implemented(funcs: Callable) -> bool:
    """
    Checks if ALL Callables are implemented or not by inspecting the bytecode; (soft check)
    Check "dis" builtin module for more details
    """
    if not funcs:
        return False
    func, *funcs = funcs
    bytes, consts = list(func.__code__.co_code), func.__code__.co_consts
    cmds = {cmd: val for cmd, val in zip(bytes[:-1:2], bytes[1::2])}

    return cmds.keys() ^ {151, 100, 83} in ({151}, set()) and consts[-1] is None or not_implemented(funcs)


def pytest_runtest_setup(item):
    for mark in item.iter_markers(name="requires"):
        if not_implemented(mark.args):
            pytest.skip("Not Implemented")
