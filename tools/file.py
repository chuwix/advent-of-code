import os
from os import PathLike
from typing import Iterable


def read_last_lines(filename: PathLike, n: int = 1) -> Iterable[str]:
    """Returns the nth before last line of a file (n=1 gives last line)"""
    num_newlines = 0
    with open(filename, 'rb') as f:
        try:
            f.seek(-2, os.SEEK_END)
            while num_newlines < n:
                f.seek(-2, os.SEEK_CUR)
                if f.read(1) == b'\n':
                    num_newlines += 1
        except OSError:
            f.seek(0)

        for line in f:
            yield line.decode()


def read_last_line(filename: PathLike) -> str | None:
    for line in read_last_lines(filename):
        return line
    return None