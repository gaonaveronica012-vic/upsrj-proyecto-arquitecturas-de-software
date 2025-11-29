# ============================================================
# Politécnica de Santa Rosa
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Alumna: Veronica Vicente Gaona
# Archivo: vars.py
# ============================================================
# Descripción:
# Define rutas base del proyecto y constantes de formato
# para impresión en consola (colores ANSI y separadores).
# ============================================================

import os

# Rutas relevantes
BASE_DIR =os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Colores ANSI
GREEN = "\033[92m"
RED = "\033[91m"
LIGHT_RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"
BOLD = "\033[1m"
SEPARATOR = f"{BOLD}{'='*50}{RESET}"