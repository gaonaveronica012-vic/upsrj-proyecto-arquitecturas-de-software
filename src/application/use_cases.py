# ============================================================
# Universidad Politécnica de Santa Rosa Jáuregui.
# Alumno: Veronica Vicente Gaona.
# Materia: Arquitecturas de Software.
# Profesor: Jesús Salvador López Ortega.
# Grupo: ISW28.
# Archivo: uses cases.py
# Descripción:  Este archivo implementa el caso de uso para la carga 
#              de archivos binarios. La clase UploadBinaryUseCase 
#              se encarga de gestionar el proceso de almacenamiento 
#              del archivo y el registro de sus metadatos en la base 
#              de datos, generando un identificador único y 
#              asignando su estado según el entorno (producción o 
#              desarrollo). Devuelve una instancia del modelo 
#              BinaryFile con la información del archivo cargado.
# ============================================================
# ============================================================
# Archivo: src/application/use_cases.py
# ============================================================
from datetime import datetime
from uuid import uuid4
from typing import List, Dict, Any, Optional

from src.domain.models import BinaryFile
from src.domain.services import SigningService

from src.infrastructure.json_repository import JsonRepository
from src.infrastructure.file_repository import FileRepository


# ============================================================
# Caso de uso: Subir binarios
# ============================================================
class UploadBinaryUseCase:
    def __init__(self, file_repo: FileRepository, db_repo: JsonRepository):
        self.file_repo = file_repo
        self.db_repo = db_repo

    def execute(self, file, environment: str) -> BinaryFile:
        """Guarda el archivo y registra su información en la base de datos JSON."""
        binary_id = str(uuid4())

        # Guarda físicamente el archivo
        self.file_repo.save(file, binary_id)

        # Crea el objeto de dominio BinaryFile
        binary = BinaryFile(
            file_id=binary_id,
            filename=file.filename,
            environment=environment,
            status='pending' if environment == 'prod' else 'signed',
            uploaded_at=datetime.now().isoformat(),
            signed_path=None,
            signature=None
        )

        # Guarda el registro en JSON
        self.db_repo.add_record(binary.to_dict())
        return binary


# ============================================================
# Caso de uso: Listar archivos subidos
# ============================================================
class ListFilesUseCase:
    def __init__(self, db_repo: JsonRepository):
        self.db_repo = db_repo

    def execute(self) -> List[Dict[str, Any]]:
        """Devuelve la lista de archivos registrados en la base JSON."""
        try:
            return self.db_repo.list_records()
        except Exception as e:
            print(f"[ListFilesUseCase] Error retrieving records: {e}")
            return []


# ============================================================
# Caso de uso: Firmar binarios
# ============================================================
class SignBinaryUseCase:
    def __init__(self, file_repo: FileRepository, json_repo: JsonRepository, signing_service: SigningService):
        self.file_repo = file_repo
        self.json_repo = json_repo
        self.signing_service = signing_service

    def execute(self, file_id: str) -> Optional[BinaryFile]:
        """Firma un archivo binario ya subido y actualiza su registro en JSON."""
        record = self.json_repo.get_record(file_id)

        if record is None:
            print(f"[SignBinaryUseCase] Record not found for file id: {file_id}")
            return None

        try:
            binary = BinaryFile.from_dict(record)

            # Ejecuta el servicio de firma
            signature, signed_path = self.signing_service.sign_file(binary)

            # Actualiza el estado
            binary.status = "signed"
            binary.signed_path = signed_path
            binary.signature = signature

            # Guarda los cambios
            self.json_repo.update_record(
                binary.id,
                {
                    "status": binary.status,
                    "signed_path": binary.signed_path,
                    "signature": binary.signature
                }
            )

            print(f"[SignBinaryUseCase] File '{binary.filename}' signed successfully.")
            return binary

        except Exception as e:
            print(f"[SignBinaryUseCase] Error while signing file '{file_id}': {e}")
            return None
