from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Instinct.core.world.world import World
    from Instinct.core.world.creatures import Creature
    from Instinct.core.nodes.context import Value

def distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return max(abs(x2-x1), abs(y2-y1))

#Para las percepciones
def compute_perceptions(creature: Creature, world: World, rng) -> dict[str, Value]:
    p: dict[str, Value] = {}
    
    #las propias del bichito
    p["health"] = creature.health
    p["age"] = creature.age
    p["lifespan"] = creature._lifespan
    p["vision"] = creature._vision
    p["faction"] = creature._faction
    p["x"] = creature.x
    p["y"] = creature.y
    cell = world.cell_at(creature.x,creature.y)
    p["terrain_here"] = cell.terrain.name
    p["reserve_here"] = cell.terrain.reserve

    #las del mundo del bichito
    p["width"] = world.width
    p["height"] = world.height
    p["tick"] = world.ticks
    p["total_creatures"] = max(0, len(world.creatures) - 1) # es así pa que el bichito no se cuente a sí mismo
    p["total_allies"] = sum(
        1 for c in world.creatures
        if c is not creature and c.is_alive() and c.is_same_faction(creature)
    )
    p["total_enemies"] = sum(
        1 for c in world.creatures
        if c is not creature and c.is_alive() and not c.is_same_faction(creature)
    )
    p["random"] = rng.randint(0, 99)

    #las de los alrededores
    vision = creature._vision
    allies_near = enemies_near = objects_near = 0
    nearest_enemy: tuple[int, int, int] | None = None
    nearest_ally: tuple[int, int, int] | None = None
    nearest_object: tuple[int, int, int] | None = None

    #los demas bichitos del radio
    for other in world.creatures:
        if other is creature or not other.is_alive():
            continue
        d=distance(creature.x, creature.y, other.x, other.y)
        if d > vision or d == 0:
            continue
        same= other.is_same_faction(creature)
        if same:
            allies_near += 1
            if nearest_ally is None or d < nearest_ally[0]:
                nearest_ally = (d, other.x - creature.x, other.y - creature.y)
        else:
            enemies_near += 1
            if nearest_enemy is None or d < nearest_enemy[0]:
                nearest_enemy = (d, other.x - creature.x, other.y - creature.y)

    #los objetos del radio
    for dy in range(-vision, vision + 1):
        for dx in range(-vision, vision +1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = creature.x +  dx, creature.y + dy
            if not world.in_bounds(nx, ny):
                continue
            if world.cell_at(nx, ny).object is not None:
                objects_near += 1
                d = max(abs(dx), abs(dy))
                if nearest_object is None or d < nearest_object[0]:
                    nearest_object = (d, dx, dy)

    p["allies_near"] = allies_near
    p["enemies_near"] = enemies_near 
    p["objects_near"] = objects_near

    if nearest_ally:
        p["ally_dist"], p["ally_dx"], p["ally_dy"] = nearest_ally
    else:
        p["ally_dist"], p["ally_dx"], p["ally_dy"] = -1, 0, 0

    if nearest_enemy:
        p["enemy_dist"], p["enemy_dx"], p["enemy_dy"] = nearest_enemy
    else:
        p["enemy_dist"], p["enemy_dx"], p["enemy_dy"] = -1, 0, 0

    if nearest_object:
        p["object_dist"], p["object_dx"], p["object_dy"] = nearest_object
    else:
        p["object_dist"], p["object_dx"], p["object_dy"] = -1, 0, 0

    #los rugidos del tick anterior
    roars_in_range = [
        text for (rx, ry, text) in world.roars_previous_tick
        if distance(creature.x, creature.y, rx, ry) <= vision
    ]   
    p["roars_near"] = len(roars_in_range)
    p["last_roar"] = roars_in_range[-1] if roars_in_range else ""

    return p
