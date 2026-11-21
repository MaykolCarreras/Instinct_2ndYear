from __future__ import annotations
from typing import TYPE_CHECKING
from Instinct.core.actions.base import Action
from Instinct.core.world.creatures import Creature
from Instinct.core.world.world import World

if TYPE_CHECKING:
    from Instinct.core.world.world import World
    from Instinct.core.world.creatures import Creature

class MoveAction(Action):
    def apply (self, world, creature, args):
        dx, dy, speed=args
        #Q: Para qué es esto? A: Para validar la acción.
        if dx not in (-1, 0, 1) or dy not in (-1, 0, 1):
            raise RuntimeError(f"dx/dy fuera de (-1, 0, 1): ({dx}, {dy})")
        if not isinstance(speed,int):
            raise RuntimeError("speed debe ser un entero")
        
        #Esto si ya es lo que hace la función, hace que la criatura se mueva 'speeed' pasos y para si tiene algo delante, dígase árbol,
        #cambolo o cualquier otro objeto o terreno no pisoteable. 
        for _ in range(speed):
            nx, ny = creature.x + dx, creature.y + dy
            if not world.can_move_to(nx,ny):
                break
            world.move_creature(creature, nx, ny)

class AttackAction(Action):
    def apply(self, world, creature, args):
        dx, dy, damage = args

        if dx not in (-1, 0, 1) or dy not in (-1, 0, 1):
            raise RuntimeError(f"dx/dy fuera de (-1, 0, 1): ({dx}, {dy})")
        if not isinstance(damage, int):
            raise RuntimeError("damage debe ser un error")
        
        target = world.creature_at(creature.x + dx, creature.y + dy)
        if target is not None:
            target.take_damage(damage)
            return
        world.damage_cell(creature.x +dx, creature.y + dy, damage)

class ConsumeAction(Action):
    def apply(self, world, creature, args):
        dx, dy, damage, heal = args

        if dx not in (-1, 0, 1) or dy not in (-1, 0, 1):
            raise RuntimeError(f"dx/dy fuera de (-1, 0, 1): ({dx}, {dy})")
        if not isinstance(damage, int) or not isinstance(heal, int):
            raise RuntimeError("damage y heal deben ser enteros")
        
        target = world.creature_at(creature.x + dx, creature.y + dy)
        if target is not None:
            target.take_damage(damage)
        else:
            world.damage_cell(creature.x + dx, creature.y + dy, damage)
        creature.heal(heal)

class ReproduceAction(Action):
    def apply(self, world, creature, args) -> None:
        dx, dy, health = args

        if dx not in (-1, 0, 1) or dy not in (-1, 0, 1):
            raise RuntimeError(f"dx/dy fuera de (-1, 0, 1): ({dx}, {dy})")
        if not isinstance(health, int):
            raise RuntimeError("health debe ser entero")
        if creature.health <= health:
            return #No le alcanza la vida al bichito pa reproducirse
        
        nx, ny = creature.x + dx, creature.y + dy
        if not world.can_move_to(nx, ny):
            return #No se puede procear por falta de espacio o la zona no está dentro del borde del mapa
        creature.take_damage(health)
        world.spawn_child_from(creature, nx, ny, health)

class RoarAction(Action):
    def apply(self, world: World, creature: Creature, args) -> None:
        text = args[0]

        if not isinstance(text, str):
            raise RuntimeError("roar espera un texto")
        world.roars_this_tick.append((creature.x, creature.y, text))
        world.log(f"{creature._species} ruge: {text}")


class SayAction(Action): 
    consumes_turn = False

    def apply(self, world, creature, args):
        text = args[0]
        if not isinstance (text,str):
            raise RuntimeError("La acción 'Say' espera un texto.")
        world.log(f"{creature._species} dice {text}")


class WaitAction(Action):
    def apply(self, world, creature, args):
        n = args[0]
        if not isinstance(n, int):
            raise RuntimeError("La acción 'Wait' espera un entero.")
        creature.wait_ticks = max(1, n) - 1


ACTION_REGISTRY: dict[str, Action] = {
    "wait": WaitAction(),
    "move": MoveAction(),
    "attack": AttackAction(),
    "consume": ConsumeAction(),
    "reproduce": ReproduceAction(),
    "roar": RoarAction(),
    "say": SayAction(),
}