import os
from dataclasses import dataclass
from typing import Tuple

# === Rutas base ===
# Calcula la ruta absoluta del directorio raíz del proyecto (uno arriba de /src)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directorios principales
SRC_DIR = os.path.join(BASE_DIR, "src")
DATA_DIR = os.path.join(BASE_DIR, "data")

# === Directorios de plantillas y datos ===
# 🔹 Aquí está el cambio importante: apunta a "src/app/templates"
TEMPLATES_DIR = os.path.join(SRC_DIR, "app", "templates")
SIGNED_DIR = os.path.join(DATA_DIR, "signed")

# === Configuración de servidor ===
@dataclass
class Hosts:
    """Configuración para el host y puerto principal."""
    main: Tuple[str, int] = ("0.0.0.0", 5000)

    