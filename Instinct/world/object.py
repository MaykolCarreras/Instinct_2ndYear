from dataclasses import dataclass, field

@dataclass
class Object:
    name: str
    char: str
    resource_max: int
    reserve: int = field(init=False)

    def __post_init__(self):
        self.reserve = self.resource_max

    def take_damage(self, damage) -> None:
        self.reserve -= damage

    def is_destroyed(self) -> bool:
        return self.reserve <= 0