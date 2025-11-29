# ============================================================
# Politécnica de Santa Rosa
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Alumna: Veronica Vicente Gaona
# Archivo: models.py
# ============================================================
# Descripción:
# Define la entidad de dominio BinaryFile, usada como modelo base
# para representar metadatos de archivos binarios, su estado,
# rutas, firma digital y tokens de aprobación/rechazo por correo.
# ============================================================

from datetime import datetime

class BinaryFile:
    """
    Domain entity representing a binary file record.
    """

    def __init__(
        self,
        id: str,
        filename: str,
        environment: str,
        status: str,
        uploaded_at: str = None,
        signed_path: str = None,
        signature: str = None,
        file_path: str = None,
        approval_token: str = None,
        reject_token: str = None,
    ):
        self.id = id
        self.filename = filename
        self.environment = environment      # 'dev' or 'prod'
        self.status = status                # 'pending', 'approved', 'signed', 'rejected'
        self.uploaded_at = uploaded_at or datetime.now().isoformat()
        self.signed_path = signed_path
        self.signature = signature
        self.file_path = file_path          # Ruta original para la firma

        # === Tokens para aprobar/rechazar vía correo ===
        self.approval_token = approval_token
        self.reject_token = reject_token

    def to_dict(self):
        """Return a dictionary representation of the BinaryFile."""
        return {
            "id": self.id,
            "filename": self.filename,
            "environment": self.environment,
            "status": self.status,
            "uploaded_at": self.uploaded_at,
            "signed_path": self.signed_path,
            "signature": self.signature,
            "file_path": self.file_path,
            "approval_token": self.approval_token,
            "reject_token": self.reject_token
        }

    @classmethod
    def from_dict(cls, data):
        """Create a BinaryFile instance from a dictionary."""
        if data is None:
            return None

        return cls(
            id=data.get("id"),
            filename=data.get("filename"),
            environment=data.get("environment"),
            status=data.get("status"),
            uploaded_at=data.get("uploaded_at"),
            signed_path=data.get("signed_path"),
            signature=data.get("signature"),
            file_path=data.get("file_path"),
            approval_token=data.get("approval_token"),
            reject_token=data.get("reject_token"),
        )
