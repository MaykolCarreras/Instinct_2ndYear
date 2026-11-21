from dataclasses import dataclass, field

@dataclass
class Terrain:
    name: str
    char: str 
    resource_max: int
    regen: int
    reserve: int = field(init = False)

    def __post_init__(self):
        self.reserve = self.resource_max

    def regenerate(self) -> None:
        self.reserve = min(self.resource_max, self.reserve + self.regen)

    def take_damage(self, damage: int) -> None:
        self.reserve -= damage