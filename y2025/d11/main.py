import dataclasses
from functools import wraps, cache
from typing import Iterable, Callable

from tools.decorators import timeit  # type: ignore


@dataclasses.dataclass(frozen=True)
class Device:
    label: str


@dataclasses.dataclass(frozen=True)
class Edge:
    device: Device
    target: Device

    def __contains__(self, item: Device) -> bool:
        return item == self.device or item == self.target


@dataclasses.dataclass
class Rack:
    devices: dict[str, Device]
    edges: list[Edge]
    edge_map: dict[Device, set[Edge]]
    target_map: dict[Device, set[Edge]]

    def add_device(self, device: Device, targets: Iterable[Device]) -> None:
        for target in targets:
            edge = Edge(device, target)
            self.edges.append(edge)
            self.edge_map.setdefault(edge.device, set()).add(edge)
            self.target_map.setdefault(edge.target, set()).add(edge)


def parse_inputs(file) -> Rack:
    rack: Rack = Rack({}, [], {}, {})

    def get_or_add_device(label: str) -> Device:
        return rack.devices.setdefault(label, Device(label))

    with open(file) as f:
        for line in f:
            data = line.rstrip().split(":", maxsplit=1)
            rack.add_device(get_or_add_device(data[0]), list(map(get_or_add_device, data[1].split())))
    return rack


@dataclasses.dataclass
class VisitedTracker:
    path: list[Device]
    required_devices: dict[Device, bool]

    def __init__(self, required_devices: set[Device] = None) -> None:
        self.path = []
        self.required_devices = {d: False for d in required_devices} if required_devices else {}

    def __hash__(self) -> int:
        return hash(tuple(self.required_devices.values()))

    def __contains__(self, device: Device) -> bool:
        return device in self.path

    def _push_device(self, device: Device) -> None:
        self.path.append(device)
        if device in self.required_devices:
            self.required_devices[device] = True

    def _pop_device(self, device: Device) -> None:
        device = self.path.pop()
        if device in self.required_devices:
            self.required_devices[device] = False

    def is_valid_path(self):
        return all(self.required_devices.values())

    @staticmethod
    def push_device(arg_name: str = "device"):
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                from inspect import signature
                sig = signature(func)
                bound = sig.bind_partial(*args, **kwargs)
                bound.apply_defaults()

                device, visited = bound.arguments[arg_name], bound.arguments["visited"]
                visited._push_device(device)
                try:
                    return func(*args, **kwargs)
                finally:
                    visited._pop_device(device)

            return wrapper

        return decorator


def get_path_count(rack: Rack, start_device: Device, end_device: Device, required_devices: set[Device] = None) -> int:
    @cache
    @VisitedTracker.push_device()
    def get_path_count_inner(device: Device, visited: VisitedTracker) -> int:
        if device == start_device: return visited.is_valid_path()
        if device not in rack.target_map: return 0
        return sum(get_path_count_inner(d.device, visited) for d in rack.target_map[device])

    return get_path_count_inner(end_device, VisitedTracker(required_devices))
