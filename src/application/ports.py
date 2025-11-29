# ============================================================
# Politécnica de Santa Rosa
# Materia: Arquitecturas de Software.
# Profesor: Jesús Salvador López Ortega.
# Grupo: ISW28.
# Alumna: Veronica Vicente Gaona.
# Archivo: ports.py
# ============================================================
# Descripción:
# Este módulo define las interfaces (puertos) que conforman la
# capa de abstracción entre la aplicación y las implementaciones
# concretas de la infraestructura. Siguiendo los principios de
# Arquitectura Limpia, estas interfaces permiten desacoplar el
# dominio de:
#
#   - Repositorios de archivos
#   - Repositorio de base de datos (JSON)
#   - Servicio de firmado digital
#   - Servicio de notificaciones por correo
#
# Cualquier clase de infraestructura debe implementar estas
# interfaces para garantizar la intercambiabilidad, pruebas
# unitarias aisladas y una arquitectura flexible, escalable
# y totalmente modular.
# ============================================================

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from src.domain.models import BinaryFile


# ============================================================
#   REPOSITORIO DE ARCHIVOS
# ============================================================

class IFileRepository(ABC):

    @abstractmethod
    def save(self, file: Any, file_id: str, signed: bool = False) -> str:
        """
        Guarda un archivo binario (original o firmado) y devuelve la ruta.
        """
        pass

    @abstractmethod
    def load(self, file_path: str) -> bytes:
        """
        Carga un archivo binario desde disco y devuelve sus bytes.
        """
        pass

    @abstractmethod
    def move_to_signed(self, original_path: str, signed_data: bytes) -> str:
        """
        Guarda el archivo firmado en /data/signed/.
        """
        pass

    @abstractmethod
    def delete(self, file_path: str) -> None:
        """
        Elimina un archivo del sistema.
        """
        pass

    @abstractmethod
    def list_files(self, signed: bool = False) -> list:
        """
        Lista archivos normales o firmados.
        """
        pass


# ============================================================
#   REPOSITORIO DE BASE DE DATOS (JSON)
# ============================================================

class IDatabaseRepository(ABC):

    @abstractmethod
    def add_record(self, record: Any) -> None:
        pass

    @abstractmethod
    def get_record(self, file_id: str) -> Optional[BinaryFile]:
        pass

    @abstractmethod
    def list_records(self) -> List[BinaryFile]:
        pass

    @abstractmethod
    def update_record(self, file_id: str, updates: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def delete_record(self, file_id: str) -> bool:
        pass


# ============================================================
#   SERVICIO DE FIRMA DIGITAL
# ============================================================

class ISigningService(ABC):

    @abstractmethod
    def sign_file(self, binary: BinaryFile) -> (str, str):
        """
        Firma el archivo y devuelve:
        - signature_hex: firma en texto hex
        - signed_file_path: ruta del archivo firmado
        """
        pass


# ============================================================
#   🔥 NUEVO: SERVICIO DE NOTIFICACIÓN POR CORREO
# ============================================================

class INotifierService(ABC):
    """
    Interface para cualquier servicio que envíe correos
    (por SMTP, SendGrid, Amazon SES, etc.)
    """

    @abstractmethod
    def send_approval_request(self, binary: BinaryFile) -> None:
        """
        Envía correo cuando un archivo pasa a estado 'PENDING'.
        """
        pass

    @abstractmethod
    def send_signed_confirmation(self, binary: BinaryFile) -> None:
        """
        Envía correo cuando el archivo ya fue firmado (APPROVED).
        """
        pass
