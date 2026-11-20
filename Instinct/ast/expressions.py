from __future__ import annotations
from abc import ABC, abstractmethod
from context import EvalContext, Value

class Expr(ABC):
    @abstractmethod
    def eval(self, context: EvalContext) -> Value:
        ...

class Literal(Expr):
    def __init__(self, value:Value):
        self.value = value

    def eval(self, context):
        return self.value    
    
    def __repr__(self) -> str:
        return f"Literal ({self.value!r})"
    
class Name(Expr):
    def __init__ (self, name : str):
        self.name = name

    def eval(self, context):
        #si es variable propia de la criatura
        if self.name in context.creature.variables:
            return context.creature.variables[self.name]
        #si es percepcion de la criatura
        if self.name in context.creature.perceptions:
            return context.creature.variables[self.name]
        #si es una constante (NONE, GROUND, ALLY, ENEMY)
        if self.name in context.constants:
            return context.constants[self.name]
        raise RuntimeError(f"Nombre no definido: {self.name}")
    
    def __repr__(self):
        return f"Name({self.name!r})"
    
class UnaryOp(Expr):
    def __init__ (self, op:str, operand:Expr):
        self.op = op
        self.operand = operand

    def eval(self, context):
        v = self.operand.eval(context)
        if self.op == "-":
            if not isinstance(v, int):
                raise RuntimeError(f"Menos unario espera un entero, recibio {type(v).__name__}")
            return -v
        if self.op == "not":
            return 0 if _truthy(v) else 1
        raise RuntimeError(f"Operador unario desconocido: {self.op}")
    
class BinaryOp(Expr):
    def __init__(self, op:str, left:Expr, right:Expr):
        self.op = op
        self.left = left
        self.right = right

    def eval(self, context):
        if self.op == "and":
            if not _truthy(self.left.eval(context)):
                return 0
            return 1 if _truthy(self.right.eval(context)) else 0
        
        if self.op == "or":
            if _truthy(self.left.eval(context)):
                return 0
            return 1 if _truthy(self.right.eval(context)) else 0
        
        l=self.left.eval(context)
        r=self.right.eval(context)
        return self._apply(l,r)
    
    def _apply(self, l:Value, r:Value):
        if type(l) is not type(r):
            raise RuntimeError(f"Tipos incompatibles en '{self.op}':"  
                               f"{type(l).__name__} y {type(r).__name__}")
        
        op=self.op
        
        if isinstance(l, str):
            if op == "==": return 1 if l==r else 0
            if op == "!=": return 1 if l!=r else 0
            raise RuntimeError(f"Operador {op} no permitido para texto.")

        if op == "+": return l+r # type: ignore
        if op == "-": return l-r # type: ignore
        if op == "*": return l*r
        if op == "/":
            if r == 0: raise RuntimeError("Division por cero no está definido.")
            return l//r # type: ignore
        if op == "%":
            if r == 0: raise RuntimeError("Módulo por cero no está definido.")
            return l%r # type: ignore
        if op == "<": return 1 if l<r else 0 # type: ignore
        if op == "<=": return 1 if l<=r else 0 # type: ignore
        if op == ">": return 1 if l>r else 0 # type: ignore
        if op == ">=": return 1 if l>=r else 0 # type: ignore
        raise RuntimeError(f"Operador binario desconocido: {op}")
    
    def __repr__(self):
        return f"BinaryOp({self.op!r}, {self.left!r}, {self.right!r})"

class FunctionCall(Expr):
    def __init__(self, name:str, args: list[Expr]):
        self.name = name
        self.args = args

    def eval(self, context):
        fn = context.function_registry.get(self.name)
        if fn is None:
            raise RuntimeError(f"Función desconocida: {self.name}")
        args = [a.eval(context) for a in self.args]
        return fn(context,args) 
    
    def _repr__(self):
        return f"FunctionCall({self.name!r}, {self.args!r})"


def _truthy(v: Value) -> bool:
    if isinstance(v, bool):
        return v
    if isinstance(v, int):
        return v!=0
    if isinstance(v, str):
        return v!=""
    return True