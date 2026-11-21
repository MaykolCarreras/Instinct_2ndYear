from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Instinct.core.nodes.context import EvalContext

NONE = -1
GROUND = 0
OBJECT = 1
ALLY = 2
ENEMY = 3

def distance(x1: int, y1: int, x2: int, y2: int) -> int:
    return max(abs(x2 - x1), abs(y2 - y1))


CONSTANTS = {
    "NONE": NONE, "GROUND": GROUND, "OBJECT": OBJECT,
    "ALLY": ALLY, "ENEMY": ENEMY,
    }

def fn_see(context: EvalContext, args: list) -> int:
    x, y = args[0], args[1]
    creature = context.creature
    if not isinstance(x, int) or not isinstance(y, int):
        raise RuntimeError("see espera dos enteros")
    #esto es si está fuera de rango de vison
    if distance(creature.x, creature.y, x, y) > creature._vision:
        return NONE
    #si está fuera del mapa, lo que el bichito ve es un muro
    if not context.world.in_bounds(x, y):
        return OBJECT
    cell = context.world.cell_at(x, y)
    if cell.creature is not None:
        return ALLY if cell.creature.is_same_faction(creature) else ENEMY
    if cell.object is not None:
        return OBJECT
    return GROUND

def fn_name(context: EvalContext, args: list) -> str:
    x, y = args[0], args[1]
    creature = context.creature
    if not isinstance(x, int) or not isinstance(y, int):
        raise RuntimeError("name espera dos enteros")
    if distance(creature.x, creature.y, x, y) > creature._vision:
        return ""
    if not context.world.in_bounds(x, y):
        return ""
    cell= context.world.cell_at(x, y)
    if cell.creature is not None:
        return cell.creature._species
    if cell.object is not None:
        return cell.object.name
    return cell.terrain.name

FUNCTION_REGISTRY = {
    "see": fn_see,
    "name": fn_name,
}