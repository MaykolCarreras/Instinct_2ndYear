from __future__ import annotations  #esto es pa que python trate todo esto como texto
from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING   #esto es pa quitar las subrayas rojas cuando escribo, xq me sacan de quicio.

if TYPE_CHECKING:
    from world.world import World
    from program import Program
    from world.creatures import Creature

Value = int | str

@dataclass
class EvalContext:
    #Lo que hace falta para evaluar las expresiones.
    creature: Creature            # la criatura que está ejecutando
    world: World                  # el mundo sobre el que actúa
    program: Program              # el programa que está ejecutando (para saltos)
    action_registry: dict         # nombre de acción -> instancia de Action
    function_registry: dict       # nombre de función -> callable(ctx, args)
    constants: dict               # nombre -> valor (NONE, GROUND, OBJECT, ALLY, ENEMY)

class ExecStatus(Enum): 
    """Lo que devuelve una instrucción al intérprete."""
    CONTINUE = "continue"           # sigue con la siguiente instrucción
    TURN_ENDED = "turn_ended"       # el turno termina aquí