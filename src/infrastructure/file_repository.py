# ============================================================
# Politécnica de Santa Rosa
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Alumna: Veronica Vicente Gaona
# Archivo: file_repository.py
# ============================================================
# Descripción:
# Implementa un repositorio de archivos encargado de guardar,
# cargar, mover, listar y eliminar binarios en el sistema de
# archivos, tanto originales como firmados.
# ============================================================

import os
from datetime import datetime
from typing import BinaryIO, Any
from src.application.ports import IFileRepository


class FileRepository(IFileRepository):
    """
    Handles all file-system operations such as storing files
    and retrieving their content.
    """

    def __init__(self, base_path: str = "data"):
        self.base_path = base_path
        self.binary_dir = os.path.join(base_path, "binaries")
        self.signed_dir = os.path.join(base_path, "signed")
        self.__ensure_directories()

    def __ensure_directories(self):
        os.makedirs(self.binary_dir, exist_ok=True)
        os.makedirs(self.signed_dir, exist_ok=True)

    def save(self, file: Any, file_id: str, signed: bool = False) -> str:
        """
        Save file data to appropriate directory.
        """
        directory = self.signed_dir if signed else self.binary_dir
        file_path = os.path.join(directory, file_id)

        try:
            data = file.read() if not isinstance(file, bytes) else file
            with open(file_path, "wb") as f:
                f.write(data)
            return file_path
        except Exception as e:
            print(f"[FileRepository] Error saving file: {e}")
            return ""

    def load(self, file_path: str) -> bytes:
        """
        Read a file from disk and return its raw bytes.
        """
        try:
            with open(file_path, "rb") as f:
                return f.read()
        except Exception as e:
            print(f"[FileRepository] Error loading file: {e}")
            return b""

    def move_to_signed(self, original_path: str, signed_data: bytes) -> str:
        """
        Save signed data in signed folder.
        """
        filename = os.path.basename(original_path)
        signed_path = os.path.join(self.signed_dir, f"signed_{filename}")

        try:
            with open(signed_path, "wb") as f:
                f.write(signed_data)
            return signed_path
        except Exception as e:
            print(f"[FileRepository] Error moving signed file: {e}")
            return ""

    def delete(self, file_path: str) -> None:
        """
        Delete file from disk.
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"[FileRepository] Error deleting file: {e}")

    def list_files(self, signed: bool = False) -> list:
        """
        List stored files in the selected directory.
        """
        directory = self.signed_dir if signed else self.binary_dir

        try:
            return os.listdir(directory)
        except Exception as e:
            print(f"[FileRepository] Error listing files: {e}")
            return []
