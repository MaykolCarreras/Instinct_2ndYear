from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Instinct.core.nodes.program import Program
    from Instinct.core.nodes.context import Value

@dataclass
class Creature:
    #Las cinco líneas del .ins
    _species: str 
    _faction: str 
    _health: int 
    _vision: int 
    _lifespan: int
    program: Program
    #Posición del bichito en el mapa
    x: int
    y: int
    #El estado del bichito
    health: int = field(init=False)
    age: int = 0
    variables: dict[str, Value] = field(default_factory=dict)
    perceptions: dict[str, Value] = field(default_factory=dict)
    pc: int = 0
    wait_ticks: int = 0

    def __post_init__ (self):
        self.health = self._health
        self.pc = self.program.entry_point() 

    def take_damage(self, damage):
        self.health = max((self.health - damage), 0)

    def heal(self, healing):
        self.health = min(self._health, self.health + healing)

    def is_alive(self) -> bool:
        return self.health > 0
    
    def is_waiting(self) -> bool:
        return self.wait_ticks > 0

    def stop_wait_one_turn(self) -> None:
        if self.wait_ticks > 0:
            self.wait_ticks -= 1       

    def is_same_faction(self, other: Creature) -> bool:
        return self._faction == other._faction
    