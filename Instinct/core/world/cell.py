from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Instinct.core.world.terrain import Terrain
    from Instinct.core.world.object import Object
    from Instinct.core.world.creatures import Creature

class Cell:
    def __init__(self, terrain: Terrain) -> None:
        self.terrain = terrain
        self.object: Object | None = None
        self.creature: Creature | None = None

    def is_passable(self) -> bool:
        return self.creature is None and self.object is None