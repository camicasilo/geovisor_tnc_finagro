import subprocess
import os

def generate_changelog():
    print("--- Generando historial de cambios (Changelog) ---")
    
    try:
        # Forzar UTF-8 para evitar errores con nombres como 'ORDOÑEZ'
        cmd = ["git", "log", "-n", "15", "--pretty=format:%h | %ad | %s", "--date=short"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
        
        if not result.stdout:
            print("--- No hay historial de Git disponible. ---")
            return

        changelog_content = "# Historial de Cambios - SIGAGRO\n\n"
        changelog_content += "| Hash | Fecha | Descripcion |\n"
        changelog_content += "|------|-------|-------------|\n"
        
        for line in result.stdout.split('\n'):
            if line.strip():
                parts = line.split(" | ")
                if len(parts) == 3:
                    changelog_content += f"| {parts[0]} | {parts[1]} | {parts[2]} |\n"
        
        with open("CHANGELOG.md", "w", encoding="utf-8") as f:
            f.write(changelog_content)
            
        print("--- CHANGELOG.md actualizado con exito. ---")
        
    except Exception as e:
        print(f"--- Error al generar changelog: {e} ---")

if __name__ == "__main__":
    generate_changelog()
