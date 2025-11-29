# ============================================================
# Politécnica de Santa Rosa
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Alumna: Veronica Vicente Gaona
# Archivo: crypto_adapter.py
# ============================================================
# Descripción:
# Adaptador criptográfico que implementa la firma SHA-256 para
# archivos binarios siguiendo la interfaz ISigningService.
# ============================================================

import hashlib
from src.application.ports import ISigningService, IFileRepository
from src.domain.models import BinaryFile


class CryptoAdapter(ISigningService):
    """
    Handles cryptographic signing of files.
    """

    def __init__(self, file_repo: IFileRepository):
        self.file_repo = file_repo

    def sign_file(self, binary: BinaryFile):
        data = self.file_repo.load(binary.file_path)
        sha256_hash = hashlib.sha256()
        sha256_hash.update(data)
        signature = sha256_hash.hexdigest()

        signed_data = data + b"\n\n# SIGNATURE: " + signature.encode("utf-8")
        signed_path = self.file_repo.move_to_signed(binary.file_path, signed_data)

        return signature, signed_path
