import os
from Instinct.loaders.terrain_loader import load_terrain
from Instinct.loaders.object_loader import load_object
from Instinct.loaders.map_loaders import load_map

def load_all_data(base_path="Instinct_2ndYear"):
    logs = []
    terrains = {}
    objects = {}
    maps = {}

    #Cargando terrenos...
    t_dir = os.path.join(base_path, "terrains")
    if os.path.exists(t_dir):
        for file in os.listdir(t_dir):
            if file.endswith(".te"):
                t, err = load_terrain(os.path.join(t_dir, file))
                if t:
                    terrains[t.char] = t
                logs.extend(err)
    
    #Cargando objetos...
    o_dir = os.path.join(base_path, "objects")
    if os.path.exists(o_dir):
        for file in os.listdir(o_dir):
            if file.endswith(".ob"):
                o, err = load_object(os.path.join(o_dir, file))
                if o:
                    objects[o.char] = o
                logs.extend(err)

    #Cargando mapas...
    m_dir = os.path.join(base_path, "maps")
    if os.path.exists(m_dir):
        for file in os.listdir(m_dir):
            if file.endswith(".map"):
                w, err = load_map(os.path.join(m_dir, file), terrains, objects)
                if w:
                    maps[w.name] = w
                logs.extend(err)
    
    return terrains, objects, maps, logs