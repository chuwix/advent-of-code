import contextlib
import dataclasses
from typing import Tuple, Iterable


@dataclasses.dataclass
class Device:
    label: str

    def __hash__(self) -> int:
        return hash(self.label)


@dataclasses.dataclass
class Edge:
    device: Device
    target: Device


def parse_inputs(file) -> Tuple[dict[str, Device], list[Edge], dict[Device, set[Device]], dict[Device, set[Device]]]:
    devices = {}
    edges = []
    edge_map = {}
    target_map = {}

    def get_or_add_device(label: str) -> Device:
        return devices.setdefault(label, Device(label))

    def add_device(device: Device, targets: Iterable[Device]) -> None:
        if any(t.label == "you" for t in targets): return
        for target in targets:
            edges.append(Edge(device, target))
            edge_map.setdefault(device, set()).add(target)
            target_map.setdefault(target, set()).add(device)

    with open(file) as f:
        for line in f:
            data = line.rstrip().split(":", maxsplit=1)
            add_device(get_or_add_device(data[0]), list(map(get_or_add_device, data[1].split())))

    return devices, edges, edge_map, target_map


@dataclasses.dataclass
class VisitedTracker:
    set: set[Device]

    def __contains__(self, device: Device) -> bool:
        return device in self.set

    @contextlib.contextmanager
    def push(self, device: Device):
        self.set.add(device)
        yield
        self.set.remove(device)


def get_path_count_to_out(devices: dict[str, Device], edges: list[Edge], edge_map: dict[Device, set[Device]], target_map: dict[Device, set[Device]]) -> int:
    def prune_unreachable():
        to_visit = set(d for d in devices.values() if d not in target_map if d.label != "you")
        while len(to_visit) > 0:
            unreachable = to_visit.pop()
            to_remove = edge_map.pop(unreachable, [])

            for target in to_remove:
                target_map[target].remove(unreachable)
                if len(target_map[target]) == 0:
                    del target_map[target]
                    to_visit.add(target)

    def get_path_count(device: Device, visited: VisitedTracker) -> int:
        if device.label == "you":
            return 1
        if device not in target_map:
            return 0
        with visited.push(device):
            return sum(get_path_count(d, visited) for d in target_map[device])

    prune_unreachable()
    return get_path_count(devices["out"], VisitedTracker(set()))
