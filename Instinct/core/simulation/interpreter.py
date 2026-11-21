from __future__ import annotations
from typing import TYPE_CHECKING
from Instinct.core.nodes.context import EvalContext, ExecStatus
from Instinct.core.actions.builtin import ACTION_REGISTRY
from Instinct.core.simulation.perceptions import compute_perceptions
from Instinct.core.simulation.functions import CONSTANTS, FUNCTION_REGISTRY

if TYPE_CHECKING:
    from Instinct.core.world.world import World
    from Instinct.core.world.creatures import Creature

MAX_LINES_PER_TURN = 100

def run_creature_turn(creature: Creature, world:World, rng) -> None:
    if not creature.is_alive():
        return
    
    if creature.is_waiting():
        creature.stop_wait_one_turn()
        return
    
    #Cargar las percepciones
    creature.perceptions = compute_perceptions(creature, world, rng)

    #Contexto durante la ejecución
    context = EvalContext(
        creature=creature,
        world=world,
        program=creature.program,
        action_registry=ACTION_REGISTRY,
        function_registry=FUNCTION_REGISTRY,
        constants=CONSTANTS,
        )
    
    #Toca ejecutar las instrucciones
    lines = 0
    current_instr = None
    try:
        while lines < MAX_LINES_PER_TURN:
            current_instr = creature.program.instructions[creature.pc]
            status = current_instr.execute(context)
            if status == ExecStatus.TURN_ENDED:
                return
            lines += 1

            creature.wait_ticks = 0
    except Exception as e:
        #Se murio el bichito porque le dio un ictus (error de runtime)
        linea = getattr(current_instr, "line", "desconocida")
        world.log(f"Error de runtime en {creature._species}: {e}")
        creature.health = 0