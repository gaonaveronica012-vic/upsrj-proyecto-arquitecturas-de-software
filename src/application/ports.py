from abc import ABC, abstractmethod
from typing import BinaryIO, Dict, Any, List, Optional


# ======================================================
# 📁 File Repository Port (interfaz para archivos binarios)
# ======================================================

class FileRepositoryPort(ABC):
    """
    Define las operaciones necesarias para el manejo de archivos binarios.
    Implementado por: src/infrastructure/file_repository.py
    """

    @abstractmethod
    def save(self, file: BinaryIO, file_id: str, signed: bool = False) -> str:
        """
        Guarda un archivo binario (firmado o no) y devuelve la ruta completa.

        Args:
            file (BinaryIO): Archivo a guardar.
            file_id (str): Identificador único del archivo.
            signed (bool): Indica si es un archivo firmado.

        Returns:
            str: Ruta completa del archivo guardado.
        """
        pass

    @abstractmethod
    def load(self, file_path: str) -> bytes:
        """Carga y devuelve el contenido binario de un archivo existente."""
        pass

    @abstractmethod
    def delete(self, file_path: str) -> None:
        """Elimina un archivo binario del sistema de archivos."""
        pass

    @abstractmethod
    def move_to_signed(self, original_path: str, signed_data: bytes) -> str:
        """
        Mueve un archivo a la carpeta de firmados y guarda los datos firmados.

        Returns:
            str: Nueva ruta del archivo firmado.
        """
        pass

    @abstractmethod
    def list_files(self, signed: bool = False) -> list:
        """Lista los nombres de los archivos almacenados."""
        pass


# ======================================================
# 📄 JSON Repository Port (interfaz para base de datos JSON)
# ======================================================

class JsonRepositoryPort(ABC):
    """
    Define las operaciones necesarias para manejar registros en una base JSON.
    Implementado por: src/infrastructure/json_repository.py
    """

    @abstractmethod
    def add_record(self, record: Dict[str, Any]) -> None:
        """Agrega un nuevo registro con marca de tiempo."""
        pass

    @abstractmethod
    def get_record(self, file_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene un registro específico por su ID."""
        pass

    @abstractmethod
    def update_record(self, file_id: str, updates: Dict[str, Any]) -> bool:
        """Actualiza los campos de un registro existente."""
        pass

    @abstractmethod
    def list_records(self) -> List[Dict[str, Any]]:
        """Lista todos los registros almacenados."""
        pass

    @abstractmethod
    def delete_record(self, file_id: str) -> bool:
        """Elimina un registro por su ID."""
        pass
