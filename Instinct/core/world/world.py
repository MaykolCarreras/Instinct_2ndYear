from __future__ import annotations
from typing import TYPE_CHECKING
from Instinct.core.world.creatures import Creature

if TYPE_CHECKING:
    from Instinct.core.world.cell import Cell

class World:
    def __init__(self, width: int, height: int, grid:list[list[Cell]]) -> None:
        self.width = width
        self.height = height
        self.grid = grid
        self.ticks = 0
        self.name = ""
        self.creatures: list[Creature] = []
        self.roars_previous_tick: list[tuple[int, int, str]] = []
        self. roars_this_tick: list[tuple[int, int, str]] = []
        self.log_messages: list[str] = []

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def cell_at(self, x: int, y: int) -> Cell:
        return self.grid[y][x]
    
    def creature_at(self, x: int, y: int) -> Creature|None:
        if not self.in_bounds(x, y):
            return None
        return self.grid[y][x].creature
    
    def can_move_to(self, x:int, y:int) -> bool:
        if not self.in_bounds(x, y):
            return False
        return self.grid[y][x].is_passable()
    
    def add_creature(self, creature: Creature, x: int, y: int) -> None:
        creature.x = x
        creature.y = y
        self.grid[y][x].creature = creature
        self.creatures.append(creature)
    
    def remove_creature(self, creature: Creature) -> None:
        if self.in_bounds(creature.x, creature.y):
            self.grid[creature.y][creature.x].creature = None
        if creature in self.creatures:
            self.creatures.remove(creature)

    def move_creature(self, creature: Creature, nx: int, ny:int) -> None:
        self.grid[creature.y][creature.x].creature = None
        creature.x, creature.y = nx, ny
        self.grid[ny][nx].creature = creature
    
    def damage_cell(self, x:int, y:int, amount:int) -> None:
        if not self.in_bounds(x,y):
            return
        cell = self.grid[y][x]
        if cell.object is not None:
            cell.object.take_damage(amount)
            if cell.object.is_destroyed():
                cell.object = None
        else:
            cell.terrain.take_damage(amount)

    def spawn_child_from(self, parent: Creature, x: int, y: int, health: int) -> Creature:
        child = Creature(
            parent._species,
            parent._faction,
            parent._health,
            parent._vision,
            parent._lifespan,
            parent.program,
            x, y)
        child.health = health
        self.add_creature(child, x, y)
        return child

    def log(self, message):
        self.log_messages.append(message)    
    