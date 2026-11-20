from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from world.world import World
    from world.creatures import Creature

#Clase abstracta Action. Su función en la vida: existir, ser bonita y dejar que las demás acciones hereden de ella el 'contrato' apply.
class Action (ABC):
    consumes_turn: bool = True
    
    @abstractmethod
    def apply (self, world: World, creature: Creature, args) -> None:
        ...
    