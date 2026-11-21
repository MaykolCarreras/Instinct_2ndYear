import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Instinct.loaders.manager import load_all_data

if __name__ == "__main__":
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

    print (f"Buscando datos en: {BASE_DIR}")

    terrains, objects, maps, logs = load_all_data(base_path=BASE_DIR)

    print("\n--- LOGS DE CARGA ---")
    if not logs:
        print("No hubo errores de carga.")
    for log in logs:
        print (log)

    print("\n--- MAPAS CARGADOS ---")
    for name, world in maps.items():
        print(f"\nMapa: {name} ({world.width}x{world.height})")
        for y in range(world.height):
            row_str = ""
            for x in range(world.width):
                cell = world.cell_at(x, y)
                if cell.object:
                    row_str += cell.object.char
                else:
                    row_str += cell.terrain.char
            print(row_str)
