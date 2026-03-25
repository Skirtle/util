from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Node:
    value: object
    connections: list[Node] = field(default_factory = list)

@dataclass
class Graph:
    nodes: list[Node] = field(default_factory = list)
    name: str = "untitled graph"

    def add(self, node: Node) -> None: self.nodes.append(node)

    def __str__(self) -> str:
        s = f"{self.name}\n"
        for i in self.nodes:
            s += f"\t{str(i.value).ljust(15, ' ')} -> {i.connections}\n"
        return s