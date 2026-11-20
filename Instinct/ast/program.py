from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from context import Value
    from instructions import Instruction

@dataclass
class Program:
    header: dict[str, Value] # type: ignore
    instructions: list[Instruction] = field(default_factory=list)
    labels: dict[str, int] = field(default_factory=dict)

    def entry_point(self) -> int:
        return self.labels["start"]