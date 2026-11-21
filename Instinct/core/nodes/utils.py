from typing import TYPE_CHECKING
from Instinct.core.nodes.context import Value

#Regla del lenguaje para valores verdaderos y falsos
def is_truthy(v: Value) -> bool:

    if isinstance(v, bool):
        return v
    
    #El 0 es falso
    if isinstance(v, int):
        return v!=0
    
    #La cadena vacia "" es falso
    if isinstance(v, str):
        return v!=""
    
    #Todo lo demas es verdadero
    return True