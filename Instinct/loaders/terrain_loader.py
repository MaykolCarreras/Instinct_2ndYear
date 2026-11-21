from Instinct.core.world.terrain import Terrain

def load_terrain(filepath: str) -> tuple[Terrain | None, list[str]]:

    errors = []
    data = {}

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
            errors.append(f"{filepath}:{num_line} - Formato inválido. Se esperaban 2 palabras.")
            continue

        key, value = parts
        data[key] = value

    required_keys = ["terrain", "char", "resource_max", "regen"]
    for key in required_keys:
        if key not in data:
            errors.append(f"{filepath} - Falta la clave obligatoria: '{key}'")

    if errors:
        return None, errors
        
    try:
        resource_max = int(data["resource_max"])
        regen = int(data["regen"])
    except ValueError:
        return None, [f"{filepath} - 'resource_max' y 'regen' deben ser números enteros."]
        
    if len(data["char"]) != 1:
        return None, [f"{filepath} - El 'char' debe ser exactamente un carácter."]
        
    terrain = Terrain(
        name=data["terrain"],
        char=data["char"],
        resource_max=resource_max,
        regen=regen
    )

    return terrain, []