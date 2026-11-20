from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from core.nodes.context import EvalContext, ExecStatus
from core.nodes.utils import is_truthy

if TYPE_CHECKING:
    from core.nodes.expressions import Expr

class Instruction(ABC):
    def __init__(self, line):
        self.line = line
    @abstractmethod
    def execute(self, context:EvalContext)-> ExecStatus:
        ...

class Assign(Instruction):
    def __init__(self, name:str, value: Expr):
        self.name = name
        self.value = value

    def execute(self, context):
        context.creature.variables[self.name] = self.value.eval(context)
        context.creature.pc += 1
        return ExecStatus.CONTINUE
    
    def __repr__(self) -> str:
        return f"Assign({self.name!r}, {self.value!r})"
    
class Goto(Instruction):
    def __init__(self, label:str):
        self.label = label

    def execute(self, context):
        context.creature.pc = context.program.labels[self.label]
        return ExecStatus.CONTINUE
    
    def __repr__(self):
        return f"Goto({self.label!r})"
    
class If(Instruction):
    def __init__(self, condition: Expr, target: str):
        self.condition = condition
        self.target = target

    def execute(self, context):
        if is_truthy(self.condition.eval(context)):
            context.creature.pc = context.program.labels[self.target]
        else:
            context.creature.pc += 1
        return ExecStatus.CONTINUE    
    
    def __repr__(self):
        return f"If({self.condition!r}, {self.target!r})"
    
class ActionCall(Instruction):
    def __init__(self, name:str, args:list[Expr], line: int = 0):
        super().__init__(line)
        self.name = name
        self.args = args

    def execute(self, context):
        action=context.action_registry.get(self.name)
        if action is None:
            raise RuntimeError(f"Acción desconocida: {self.name}")
        try:
            args=[a.eval(context) for a in self.args]
        except Exception as e:
            raise RuntimeError(f"{e}") from e
        action.apply(context.world, context.creature, args)

        context.creature.pc += 1
        return ExecStatus.TURN_ENDED if action.consumes_turn else ExecStatus.CONTINUE