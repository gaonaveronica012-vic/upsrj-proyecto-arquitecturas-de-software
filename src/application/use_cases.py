# ============================================================
# Politécnica de Santa Rosa
# Materia: Arquitecturas de Software.
# Profesor: Jesús Salvador López Ortega.
# Grupo: ISW28.
# Alumna: Veronica Vicente Gaona.
# Archivo: use_cases.py
# ============================================================
# Descripción:
# Contiene los casos de uso de la aplicación, responsables de
# coordinar la carga, aprobación, firma, rechazo y listado de
# archivos, así como las notificaciones asociadas.
# Implementa la lógica principal siguiendo Arquitectura Limpia.
# ============================================================

from datetime import datetime
from uuid import uuid4
from typing import List, Dict, Any, Optional

from src.domain.models import BinaryFile
from src.application.ports import (
    IFileRepository,
    IDatabaseRepository,
    ISigningService,
    INotifierService,
)


class UploadBinaryUseCase:
    """
    Upload: si environment == 'prod' -> sign automático (y notificar signed).
    Si environment != 'prod' -> dejar pending, notificar approval request.
    """

    def __init__(
        self,
        file_repo: IFileRepository,
        db_repo: IDatabaseRepository,
        signing_service: ISigningService,
        notifier: Optional[INotifierService] = None,
    ):
        self.file_repo = file_repo
        self.db_repo = db_repo
        self.signing_service = signing_service
        self.notifier = notifier

    def execute(self, file, environment: str) -> BinaryFile:
        binary_id = str(uuid4())
        saved_path = self.file_repo.save(file, binary_id)

        # crear entidad y persistir initial
        binary = BinaryFile(
            id=binary_id,
            filename=getattr(file, "filename", "unknown.bin"),
            environment=environment,
            status="pending",
            uploaded_at=datetime.now().isoformat(),
            signed_path=None,
            signature=None,
            file_path=saved_path,
        )

        self.db_repo.add_record(binary.to_dict())

        # Si es producción: firmar automáticamente y notificar signed
        if environment == "prod":
            try:
                signature, signed_path = self.signing_service.sign_file(binary)
                binary.status = "signed"
                binary.signature = signature
                binary.signed_path = signed_path

                self.db_repo.update_record(
                    binary.id,
                    {"status": binary.status, "signed_path": binary.signed_path, "signature": binary.signature},
                )

                if self.notifier:
                    try:
                        self.notifier.send_signed_confirmation(binary)
                    except Exception as e:
                        print(f"[UploadBinaryUseCase] Notifier failed (signed): {e}")

            except Exception as e:
                print(f"[UploadBinaryUseCase] Signing failed for prod: {e}")
        else:
            # No es prod -> enviar solicitud de aprobación (PENDING)
            if self.notifier:
                try:
                    self.notifier.send_approval_request(binary)
                except Exception as e:
                    print(f"[UploadBinaryUseCase] Notifier failed (approval request): {e}")

        return binary


class ListFilesUseCase:
    def __init__(self, db_repo: IDatabaseRepository):
        self.db_repo = db_repo

    def execute(self) -> List[Dict[str, Any]]:
        try:
            records = self.db_repo.list_records()
            return [r.to_dict() for r in records]
        except Exception as e:
            print(f"[ListFilesUseCase] Error retrieving records: {e}")
            return []


class SignBinaryUseCase:
    """
    Firma solo archivos que ya están 'approved'.
    """

    def __init__(self, db_repo: IDatabaseRepository, signing_service: ISigningService, notifier: Optional[INotifierService] = None):
        self.db_repo = db_repo
        self.signing_service = signing_service
        self.notifier = notifier

    def execute(self, file_id: str) -> Optional[BinaryFile]:
        record = self.db_repo.get_record(file_id)
        if record is None:
            print(f"[SignBinaryUseCase] Record not found for file id: {file_id}")
            return None

        if record.status != "approved":
            print(f"[SignBinaryUseCase] Cannot sign file {file_id} with status '{record.status}'")
            return None

        try:
            signature, signed_path = self.signing_service.sign_file(record)

            record.status = "signed"
            record.signature = signature
            record.signed_path = signed_path

            self.db_repo.update_record(
                record.id,
                {"status": record.status, "signed_path": record.signed_path, "signature": record.signature},
            )

            if self.notifier:
                try:
                    self.notifier.send_signed_confirmation(record)
                except Exception as e:
                    print(f"[SignBinaryUseCase] Notifier failed (signed): {e}")

            return record
        except Exception as e:
            print(f"[SignBinaryUseCase] Error signing file {file_id}: {e}")
            return None


class ApproveBinaryUseCase:
    """
    Aprueba un archivo pending -> lo marca approved y luego dispara la firma.
    """

    def __init__(self, db_repo: IDatabaseRepository, signing_service: ISigningService, notifier: Optional[INotifierService] = None):
        self.db_repo = db_repo
        self.signing_service = signing_service
        self.notifier = notifier

    def execute(self, file_id: str) -> Optional[BinaryFile]:
        record = self.db_repo.get_record(file_id)
        if record is None:
            print(f"[ApproveBinaryUseCase] Record not found: {file_id}")
            return None

        # Solo podemos aprobar si está pending
        if record.status != "pending":
            print(f"[ApproveBinaryUseCase] Cannot approve file with status '{record.status}'")
            return None

        # Marcar approved
        record.status = "approved"
        self.db_repo.update_record(file_id, {"status": "approved"})

        # Firmar inmediatamente
        try:
            signature, signed_path = self.signing_service.sign_file(record)
            record.status = "signed"
            record.signature = signature
            record.signed_path = signed_path

            self.db_repo.update_record(
                file_id,
                {"status": record.status, "signed_path": record.signed_path, "signature": record.signature},
            )

            if self.notifier:
                try:
                    self.notifier.send_signed_confirmation(record)
                except Exception as e:
                    print(f"[ApproveBinaryUseCase] Notifier failed (signed): {e}")

            return record

        except Exception as e:
            print(f"[ApproveBinaryUseCase] Error signing after approve: {e}")
            return None


class RejectBinaryUseCase:
    """
    Rechaza un archivo (pending -> rejected) y notifica.
    """

    def __init__(self, db_repo: IDatabaseRepository, notifier: Optional[INotifierService] = None):
        self.db_repo = db_repo
        self.notifier = notifier

    def execute(self, file_id: str) -> Optional[BinaryFile]:
        record = self.db_repo.get_record(file_id)
        if record is None:
            print(f"[RejectBinaryUseCase] Record not found: {file_id}")
            return None

        # Solo rechazar si está pending
        if record.status != "pending":
            print(f"[RejectBinaryUseCase] Cannot reject file with status '{record.status}'")
            return None

        record.status = "rejected"
        self.db_repo.update_record(file_id, {"status": "rejected"})

        if self.notifier:
            try:
                self.notifier.send_rejection_notification(record)
            except Exception as e:
                print(f"[RejectBinaryUseCase] Notifier failed (rejection): {e}")

        return record
