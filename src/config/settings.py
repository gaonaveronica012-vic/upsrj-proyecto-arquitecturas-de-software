# ============================================================
# Politécnica de Santa Rosa
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Alumna: Veronica Vicente Gaona
# Archivo: settings.py
# ============================================================
# Descripción:
# Maneja variables de entorno, rutas base, configuración de Flask,
# directorios de datos y parámetros generales de la aplicación.
# Centraliza ajustes que pueden cambiar según el entorno.
# ============================================================

import os
from dotenv import load_dotenv

# ======================================================
#  Load environment variables
# ======================================================
# Permite usar un archivo .env para definir variables de entorno
# (por ejemplo: DEBUG=True, FLASK_PORT=5000, etc.)
load_dotenv()

# ======================================================
# General Application Settings
# ======================================================

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Nombre de la aplicación (puede usarse en logs, UI, etc.)
APP_NAME = os.getenv("APP_NAME", "ProyectoArquitecturas")

# Entorno actual (development, production, testing)
ENV = os.getenv("ENV", "development")

# Modo debug de Flask
DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1", "yes")

# Host y puerto del servidor Flask
HOST = os.getenv("FLASK_HOST", "0.0.0.0")
PORT = int(os.getenv("FLASK_PORT", 5000))

# ======================================================
#  Repository Paths
# ======================================================

# Carpeta donde se almacenan los datos binarios
DATA_DIR = os.getenv("DATA_DIR", os.path.join(BASE_DIR, "data"))
BINARIES_DIR = os.path.join(DATA_DIR, "binaries")
SIGNED_DIR = os.path.join(DATA_DIR, "signed")

# Ruta del archivo JSON para el repositorio de metadatos
JSON_DB_PATH = os.getenv("JSON_DB_PATH", os.path.join(DATA_DIR, "database.json"))

# ======================================================
# Flask Template Config
# ======================================================

TEMPLATES_DIR = os.getenv("TEMPLATES_DIR", os.path.join(BASE_DIR, "src", "templates"))


# ======================================================
#  Security Settings
# ======================================================

# Clave de Flask (para sesiones, CSRF, etc.)
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")

# ======================================================
#  Helper: ensure folders exist
# ======================================================

def ensure_directories():
    """Crea las carpetas necesarias para el funcionamiento de la app."""
        for path in [DATA_DIR, BINARIES_DIR, SIGNED_DIR]:
                os.makedirs(path, exist_ok=True)

                ensure_directories()
