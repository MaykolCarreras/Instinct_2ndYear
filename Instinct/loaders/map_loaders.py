from Instinct.core.world.world import World
from Instinct.core.world.cell import Cell 
from Instinct.core.world.terrain import Terrain
from Instinct.core.world.object import Object

def load_map(filepath: str, terrains: dict[str, Terrain], objects: dict[str, Object]) -> tuple[World | None, list[str]]:

    errors = []

    try: 
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        return None, [f"Error al leer el mapa {filepath}: {e}"]
    
    lines = [line.rstrip("\n") for line in lines if line.strip()]

    if not lines:
        return None, [f"{filepath} - El mapa está vacío."]
    
    map_name = lines[0].strip()
    grid_lines = lines[1:]

    if not grid_lines:
        return None, [f"{filepath} - El mapa no tiene celdas."]
    
    width = len(grid_lines[0])
    height = len(grid_lines)

    grid = []

    default_terrain = list(terrains.values())[0] if terrains else None
    if not default_terrain:
        return None, [f"Error global: No hay terrenos cargados para poner debajo de los objetos."]
    
    for y, line in enumerate(grid_lines):
        if len(line) != width:
            errors.append(f"{filepath}:{y+2} - La fila no tiene el mismo el largo que las demás ({len(line)} vs {width}).")
            continue
        
        row_cells=[]
        for x, char in enumerate(line):
            if char in terrains:
                t_proto = terrains[char]
                cell = Cell(Terrain(t_proto.name, t_proto.char, t_proto.resource_max, t_proto.regen))
            elif char in objects:
                t_proto = default_terrain
                o_proto = objects[char]
                cell = Cell(Terrain(t_proto.name, t_proto.char, t_proto.resource_max, t_proto.regen))
                cell.object = Object(o_proto.name, o_proto.char, o_proto.resource_max)
            else:
                errors.append(f"{filepath}:{y+2} - Carácter desconocido '{char}' en la columna {x+1}.")
                cell = Cell(Terrain(default_terrain.name, default_terrain.char, default_terrain.resource_max, default_terrain.regen))

            row_cells.append(cell)
        
        grid.append(row_cells)
    
    if errors:
        return None, errors
    
    world = World(width=width, height=height, grid=grid)
    world.name = map_name
    return world, []