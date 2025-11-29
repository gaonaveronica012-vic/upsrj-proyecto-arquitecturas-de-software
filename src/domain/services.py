# ============================================================
# Politécnica de Santa Rosa
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Alumna: Veronica Vicente Gaona
# Archivo: services.py
# ============================================================
# Descripción:
# Implementa el servicio de firma digital.
from src.domain.models import BinaryFile
from typing import Optional

from src.infrastructure.file_repository import FileRepository
from src.infrastructure.json_repository import JsonRepository

import hashlib


class SigningService:

    def __init__(self, file_repo: FileRepository):
        self.file_repo = file_repo

    def sign_file(self, binary: BinaryFile):
        """
        Returns:
            tuple[str, str]: (signature_hex, signed_file_path)
        """

        # Cargar archivo desde file_repo
        data = self.file_repo.load(binary.file_path)

        # Crear firma SHA-256
        sha256_hash = hashlib.sha256()
        sha256_hash.update(data)
        signature = sha256_hash.hexdigest()

        # Guardar archivo firmado usando el repositorio
        signed_path = self.file_repo.move_to_signed(
            binary.file_path,
            data + b"\n\n# SIGNATURE: " + signature.encode("utf-8")
        )

        return signature, signed_path


class SignBinaryUseCase:

    def __init__(
        self,
        file_repo: FileRepository,
        json_repo: JsonRepository,
        signing_service: SigningService,
    ):
        self.file_repo = file_repo
        self.json_repo = json_repo
        self.signing_service = signing_service

    def execute(self, file_id: str) -> Optional[BinaryFile]:

        binary = self.json_repo.get_record(file_id)

        if binary is None:
            print(f"[SignBinaryUseCase] File id not found: {file_id}")
            return None

        # Firmar archivo
        signature, signed_path = self.signing_service.sign_file(binary)

        # Actualizar modelo
        binary.status = "signed"
        binary.signature = signature
        binary.signed_path = signed_path

        # Guardar cambios
        self.json_repo.update_record(
            file_id,
            {
                "status": binary.status,
                "signature": signature,
                "signed_path": signed_path,
            },
        )

        print(f"[SignBinaryUseCase] File '{binary.filename}' signed successfully.")
        return binary
