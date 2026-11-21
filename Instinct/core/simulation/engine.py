from __future__ import annotations
from typing import TYPE_CHECKING
from Instinct.core.simulation.interpreter import run_creature_turn

if TYPE_CHECKING:
    from Instinct.core.world.world import World

class SimulationEngine:
    def __init__(self, world: World, rng):
        self.world = world
        self.rng = rng

    def tick(self) -> None:
        world = self.world

        #Orden aleatorio
        living = [c for c in world.creatures if c.is_alive()]
        self.rng.shuffle(living)

        #Turno de cada bichito
        for creature in living:
            if not creature.is_alive():
                continue
            run_creature_turn(creature, world, self.rng)

        self._end_of_tick()

        world.ticks += 1

    def _end_of_tick(self):
        world = self.world

        #Quitar vida y envejecer
        for creature in list(world.creatures):
            if not creature.is_alive():
                continue
            creature.health -= 1
            creature.age += 1

        #Los que la palmaron
        for creature in list(world.creatures):
            if not creature.is_alive() or creature.age >= creature._lifespan:
                world.remove_creature(creature)
                world.log(f"{creature._species} muere en ({creature.x},{creature.y})")
        
        #Regerando terrenos...
        for row in world.grid:
            for cell in row:
                cell.terrain.regenerate()

        #Objetos partidos al medio
        for row in world.grid:
            for cell in row:
                if cell.object is not None and cell.object.is_destroyed():
                    cell.object = None

        #Rugidos
        world.roars_previous_tick = world.roars_this_tick
        world.roars_this_tick = []