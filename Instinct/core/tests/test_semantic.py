from Instinct.core.nodes.program import Program
from Instinct.core.nodes.instructions import If, Goto, Assign, ActionCall
from Instinct.core.nodes.expressions import BinaryOp, Name, Literal, FunctionCall
from Instinct.core.semantic import SemanticAnalyzer

def probar_analizador():

    #Le faltan cosas al header
    header_malo = {
        "creature": "Bug",
        "faction": "Test",
        "health": 50
    }

    # 2. Instrucciones con errores a propósito
    instrucciones_malas = [
        # Intentar asignar valora percepcion 
        Assign("health", Literal(100)),
        
        #Hacaer Goto a una etiqueta inexistente
        Goto("volar"),
        
        #Llamar a una accion con menos argumentos de los que lleva
        ActionCall("move", [Literal(1), Literal(0)]),
        
        #llamar a una accion inexistente
        ActionCall("disparar_laser", [Literal(1)]),

        #Llamar  a una funcion inexistente
        If(BinaryOp("==", Name("enemy_dist"), FunctionCall("invisible", [])), "atacar"),
    ]

    programa_malo = Program(
        header=header_malo,
        instructions=instrucciones_malas,
        labels={"start": 0} # "atacar" no existe como label => debe dar un error
    )

    analyzer = SemanticAnalyzer()
    es_valido = analyzer.analyze(programa_malo)

    print("¿El programa es válido?", es_valido)
    print("\nErrores encontrados:")
    for err in analyzer.errors:
        print(f" - {err}")

if __name__ == "__main__":
    probar_analizador()