from Instinct.core.world.object import Object

def load_object(filepath: str) -> tuple[Object | None, list[str]]:
    errors = []
    data ={}

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        return None, [f"Error al leer el archivo {filepath}: {e}"]
    
    for num_line, line in enumerate(lines, start=1):
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        if len(parts) != 2:
            errors.append(f"{filepath}: {num_line} - Formato inválido.")
            continue

        key, value = parts
        data[key] = value

    required_keys = ["object", "char", "resource_max"]
    for key in required_keys:
        if key not in data:
            errors.append(f"{filepath} - Falta la clave obligatoria: '{key}'")

    if errors:
        return None, errors
    
    try:
        resource_max = int(data["resource_max"])
    except ValueError:
        return None, [f"{filepath} - 'resource_max' debe ser un número entero."]
    
    if len(data["char"]) != 1:
        return None, [f"{filepath} - El 'char' debe ser exactamente un carácter."]
    
    obj = Object(
        name=data["object"],
        char=data["char"],
        resource_max=resource_max
    )

    return obj, []