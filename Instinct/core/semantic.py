from __future__ import annotations
from typing import TYPE_CHECKING
from Instinct.core.nodes.program import Program
from Instinct.core.nodes.instructions import If, Goto, Assign, ActionCall
from Instinct.core.nodes.expressions import BinaryOp, UnaryOp, FunctionCall, Name, Literal
from Instinct.core.actions.builtin import ACTION_REGISTRY
from Instinct.core.simulation.functions import FUNCTION_REGISTRY, CONSTANTS

if TYPE_CHECKING:
    from Instinct.core.nodes.instructions import Instruction
    from Instinct.core.nodes.expressions import Expr

#Lista con todas las percepciones del bichito
PERCEPTIONS = {
    "health", "age", "lifespan", "vision", "species", "faction", "x", "y",
    "terrain_here", "reserve_here", "width", "height", "tick",
    "total_creatures", "total_allies", "total_enemies", "random",
    "allies_near", "enemies_near", "objects_near",
    "enemy_dist", "enemy_dx", "enemy_dy",
    "ally_dist", "ally_dx", "ally_dy",
    "object_dist", "object_dx", "object_dy",
    "roars_near", "last_roar"
}

#Diccionario con la cantidad de argumentos de cada acción que tiene el bichito
ACTION_ARITY = {
    "move": 3, "attack": 3, "consume": 4, "reproduce": 3,
    "roar": 1, "say": 1, "wait": 1
}

#Diccionario con la cantidad de argumentos de las funciones see y name
FUNCTION_ARITY = {
    "see": 2, "name": 2
}


class SemanticAnalyzer:
    def __init__(self):
        self.errors: list[str] = []

    def error(self, msg: str, line: int | None = None):
        if line is not None:
            self.errors.append(f"Línea {line}: {msg}")
        else:
            self.errors.append(msg)

    def analyze(self, program: Program) -> bool:
        #Esta empieza a analizar el AST que manda el parser. Da True si no hubo errores y False si los hubo.
        self.errors = []
        self.visit(program)
        return len(self.errors) == 0

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.generic_visit)
        return method(node)

    def generic_visit(self, node):

        pass


    #Desde aquí se visita la estructra principal del programa
    def visit_Program(self, node: Program):
        self.current_program = node
        required_keys = {"creature", "faction", "health", "vision", "lifespan"}
        header_keys = set(node.header.keys())
        
        missing = required_keys - header_keys
        if missing:
            self.error(f"Faltan claves obligatorias en la cabecera: {', '.join(missing)}")
        
        if "health" in node.header and (not isinstance(node.header["health"], int) or node.header["health"] <= 0):
            self.error("El 'health' inicial debe ser un entero mayor que 0.")
        if "vision" in node.header and (not isinstance(node.header["vision"], int) or node.header["vision"] < 1):
            self.error("La 'vision' debe ser un entero mayor o igual que 1.")
        if "lifespan" in node.header and (not isinstance(node.header["lifespan"], int) or node.header["lifespan"] <= 0):
            self.error("El 'lifespan' debe ser un entero mayor que 0.")

        if "start" not in node.labels:
            self.error("Falta la etiqueta obligatoria 'start:'")

        for instr in node.instructions:
            self.visit(instr)

    #Aqui se visitan las instrucciones
    def visit_Goto(self, node: Goto):
        if node.label not in self.current_program.labels:
            self.error(f"Salto a etiqueta inexistente: '{node.label}'", getattr(node, 'line', None))

    def visit_If(self, node: If):
        self.visit(node.condition)
        if node.target not in self.current_program.labels:
            self.error(f"Salto a etiqueta inexistente: '{node.target}'", getattr(node, 'line', None))

    def visit_Assign(self, node: Assign):
        if node.name in PERCEPTIONS:
            self.error(f"No se puede asignar un valor a la percepción de solo lectura '{node.name}'", getattr(node, 'line', None))
        elif node.name in CONSTANTS:
            self.error(f"No se puede asignar un valor a la constante '{node.name}'", getattr(node, 'line', None))
        else:
            self.visit(node.value)

    def visit_ActionCall(self, node: ActionCall):
        if node.name not in ACTION_REGISTRY:
            self.error(f"Acción desconocida: '{node.name}'", getattr(node, 'line', None))
        else:
            expected = ACTION_ARITY.get(node.name)
            if expected is not None and len(node.args) != expected:
                self.error(f"La acción '{node.name}' espera {expected} argumentos, pero recibió {len(node.args)}", getattr(node, 'line', None))
        
        for arg in node.args:
            self.visit(arg)

    #Aqui se visitan las expresiones
    def visit_BinaryOp(self, node: BinaryOp):
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node: UnaryOp):
        self.visit(node.operand)

    def visit_FunctionCall(self, node: FunctionCall):
        if node.name not in FUNCTION_REGISTRY:
            self.error(f"Función desconocida: '{node.name}'")
        else:
            expected = FUNCTION_ARITY.get(node.name)
            if expected is not None and len(node.args) != expected:
                self.error(f"La función '{node.name}' espera {expected} argumentos, pero recibió {len(node.args)}")
        
        for arg in node.args:
            self.visit(arg)

    def visit_Name(self, node: Name):
        pass

    def visit_Literal(self, node: Literal):
        pass

