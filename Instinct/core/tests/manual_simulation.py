import random
from core.nodes.expressions import Literal, Name, BinaryOp
from core.nodes.instructions import ActionCall, Goto, If
from core.nodes.program import Program
from core.world.terrain import Terrain
from core.world.cell import Cell
from core.world.creatures import Creature
from core.world.world import World
from core.simulation.engine import SimulationEngine

#Esto es pa testear que las cosas funcionan en consola antes de meterle mano a los cargadores, el analizador semantico y toda esa talla.

#El programa de prueba es un bichito que lo que hace es caminar hacia la derecha hasta llegar al borde, después, se queda quieto ahí hasta nuevo aviso.
# y el otro, si ve un enemigo, lo ataca y si no, camina pa la izquierda.

programa_caminante = Program(
    header={
        "creature": "Walker",
        "faction": "A", 
        "health": 50,
        "vision": 3, 
        "lifespan": 100
    },

    instructions=[
        ActionCall("move", [Literal(1), Literal(0), Literal(1)], line=3),
        Goto("start"),
    ],
    labels={"start": 0},   
)

progama_guerrero = Program(
    header={
        "creature": "Fighter",
        "faction": "B",
        "health": 60,
        "vision": 3,
        "lifespan": 100,
    },

    instructions=[
        #[0] if enemy_dist == 1 goto atacar
        If(
            BinaryOp("==", Name("enemy_dist"), Literal(1)),
            "atacar",
        ),
        #[1] move(-1, 0, 1)
        ActionCall("move", [Literal(-1), Literal(0), Literal(1)]),
        #[2] goto start
        Goto("start"),
        #[3] atacar: attack(enemy_dx, enemy_dy, 10)
        ActionCall(
            "attack",
            [Name("enemy_dx"), Name("enemy_dy"), Literal(10)],
        ),
        #[4] goto start
        Goto("start"),        
    ],
    labels={"start": 0, "atacar": 3},
)

grass = Terrain(name="Grass", char=".", resource_max=100, regen=2)
grid = [[Cell(Terrain("Grass", ".", 100, 2)) for _ in range(10)] for _ in range(1)]
world = World(width=10, height=1, grid=grid)

walker = Creature("Walker", "A", 50, 3, 100, programa_caminante, 0, 0)
fighter = Creature("Fighter", "B", 60, 3, 100, progama_guerrero, 9, 0)

world.add_creature(walker, 0, 0)
world.add_creature(fighter, 9, 0)

rng = random.Random(42)
engine = SimulationEngine(world, rng)

#Simular 15 ticks
print(f"Mundo inicial: {world.width}x{world.height}")
print(f"  Walker:  pos=({walker.x},{walker.y}) hp={walker.health} age={walker.age}")
print(f"  Fighter: pos=({fighter.x},{fighter.y}) hp={fighter.health} age={fighter.age}")
print("-" * 60)

for _ in range(15):
    engine.tick()

    w_estado = (
        f"Walker=({walker.x},{walker.y}) hp={walker.health} age={walker.age}"
        if walker.is_alive() else "Walker MUERTO"
    )
    f_estado = (
        f"Fighter=({fighter.x},{fighter.y}) hp={fighter.health} age={fighter.age}"
        if fighter.is_alive() else "Fighter MUERTO"
    )
    print(f"tick {world.ticks:2d} | {w_estado:30s} | {f_estado}")

    if not walker.is_alive() and not fighter.is_alive():
        print("Ambas criaturas muertas. Fin.")
        break

#Tirar todos los logs
print("-" * 60)
print("Logs:")
for linea in world.log_messages:
    print(f"  {linea}")

    