from typing import Iterable, Any


def filter_none(iterable: Iterable[Any]) -> Iterable[Any]:
    return filter(lambda item: item is not None, iterable)
