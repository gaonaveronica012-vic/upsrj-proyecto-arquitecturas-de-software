from datetime import datetime

class BinaryFile:
    """
    Domain entity representing a binary file record.
    """

    def __init__(self, id, filename, environment, status,
                 uploaded_at=None, signed_path=None, signature=None):
        self.id = id
        self.filename = filename
        self.environment = environment          # 'dev' or 'prod'
        self.status = status                     # 'pending', 'approved', etc.
        self.uploaded_at = uploaded_at or datetime.now().isoformat()
        self.signed_path = signed_path
        self.signature = signature

    def to_dict(self):
        """Return a dictionary representation of the BinaryFile."""
        return {
            "id":          self.id,
            "filename":    self.filename,
            "environment": self.environment,
            "status":      self.status,
            "uploaded_at": self.uploaded_at,
            "signed_path": self.signed_path,
            "signature":   self.signature
        }

    @classmethod
    def from_dict(cls, data):
        """Create a BinaryFile instance from a dictionary."""
        return cls(
            id=data.get("id"),
            filename=data.get("filename"),
            environment=data.get("environment"),
            status=data.get("status"),
            uploaded_at=data.get("uploaded_at"),
            signed_path=data.get("signed_path"),
            signature=data.get("signature")
        )
