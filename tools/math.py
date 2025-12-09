import math
import typing


def sign(x: typing.SupportsAbs) -> int:
    return int(math.copysign(1, x))
