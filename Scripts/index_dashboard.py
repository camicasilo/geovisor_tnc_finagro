import re
import json
import os

def index_dashboard():
    html_path = "index.html"
    json_path = "Ayuda.json"
    
    if not os.path.exists(html_path):
        print(f"--- Error: {html_path} no encontrado. ---")
        return

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Buscar IDs en elementos interactivos comunes
    interactive_ids = re.findall(r'id=["\']([^"\']+)["\']', html_content)
    
    # Elementos con onmouseenter o logic en JS
    hover_ids = re.findall(r'updateConsole\(["\']([^"\']+)["\']\)', html_content)
    
    # Unificar y limpiar
    all_potential_ids = set(interactive_ids + hover_ids)
    
    # Cargar diccionario actual
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            existing_ids = {item["id"] for item in data["diccionario_geovisor"]}
    else:
        existing_ids = set()

    print(f"--- Analizando dashboard ---")
    print(f"--- Elementos potenciales encontrados en HTML: {len(all_potential_ids)}")
    print(f"--- Elementos ya indexados en Ayuda.json: {len(existing_ids)}")

    missing = []
    for pid in all_potential_ids:
        if pid not in existing_ids and pid.isupper():
            missing.append(pid)

    if missing:
        print(f"\n--- Faltan {len(missing)} elementos por indexar en Ayuda.json:")
        for m in sorted(missing):
            print(f"  - {m}")
    else:
        print("\n--- ¡Todo el dashboard parece estar correctamente indexado! ---")

if __name__ == "__main__":
    index_dashboard()
