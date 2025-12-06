import dataclasses
import operator
from io import open
from itertools import filterfalse
from os import PathLike
from typing import Callable, Iterable, TypeVar

from more_itertools.more import peekable

from tools.file import read_last_line

T = TypeVar('T')
TVal = TypeVar('TVal')


@dataclasses.dataclass
class Op:
    func: Callable[[T, TVal], T]
    default: TVal | None
    idx: int = 0


empty_op = Op(lambda x, y: 0, 0)

ops_templates: dict[str, Op] = {
    '+': Op(operator.add, 0),
    '-': Op(operator.sub, 0),
    '*': Op(operator.mul, 1),
}


def parse_lists_and_ops(file: PathLike[str]) -> tuple[list[Op], Iterable[list[int]]]:
    def parse_ops(file: PathLike[str]) -> list[Op]:
        line = read_last_line(file)
        templates = map(lambda op: ops_templates[op], line.split())
        return [Op(op.func, op.default, i) for i, op in enumerate(templates)]

    def parse_inputs(file: PathLike[str]) -> Iterable[list[int]]:
        with (open(file) as input):
            for row in input:
                try:
                    yield list(map(int, row.split()))
                except ValueError:
                    pass

    ops = parse_ops(file)
    inputs = parse_inputs(file)
    return ops, inputs


def parse_lists_and_ops_columns(file: PathLike[str]) -> tuple[list[Op], list[int]]:
    def parse_ops_columns(file: PathLike[str]) -> list[Op | None]:
        line = read_last_line(file)
        parsed_ops: list[Op] = []
        op: Op | None = None
        op_idx = 0

        for i, c in enumerate(line):
            if c != " ":
                op_template = ops_templates[c]
                op = Op(op_template.func, op_template.default, op_idx)
                op_idx += 1

                if i > 0:
                    parsed_ops[i - 1] = None

            parsed_ops.append(op)

        return parsed_ops

    def parse_digits(row: str) -> Iterable[int | None]:
        for c in row:
            if c.isdigit():
                yield int(c)
            elif c == " ":
                yield None

    def parse_inputs_columns(file) -> Iterable[list[int | None]]:
        with (open(file) as input):
            for row in input:
                yield list(parse_digits(row))

    ops = parse_ops_columns(file)
    inputs = peekable(parse_inputs_columns(file))

    def add_digit(x, y):
        if x is None:
            x = 0
        if y is None:
            return x
        return x * 10 + y

    transpose_ops = [Op(add_digit, None, i) for i in range(len(inputs.peek()))]
    transposed_inputs = parallel_map_ops(transpose_ops, inputs)

    return ops, transposed_inputs


def parallel_map_ops(ops: list[Op | None], inputs: Iterable[list[TVal]]) -> list[TVal]:
    totals_count = max(ops, key=lambda op: -1 if op is None else op.idx).idx + 1
    totals = [None] * totals_count

    for input in inputs:
        for op, val in zip(ops, input):
            if op is None:
                continue
            if val is None:
                val = op.default
            if totals[op.idx] is None:
                totals[op.idx] = op.default
            totals[op.idx] = op.func(totals[op.idx], val)

    return totals


def compute_totals_sum(ops: list[Op | None], inputs: Iterable[list[int]]) -> int:
    return sum(parallel_map_ops(ops, inputs))
