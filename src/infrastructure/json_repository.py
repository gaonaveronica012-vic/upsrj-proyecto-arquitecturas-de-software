# ============================================================
# Politécnica de Santa Rosa
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Alumna: Veronica Vicente Gaona
# Archivo: json_repository.py
# ============================================================
# Descripción:
# Repositorio JSON robusto que almacena y gestiona registros
# de archivos binarios. Corrige estructuras dañadas, valida
# datos y proporciona operaciones CRUD y búsqueda por tokens.
# ============================================================

import os
import json
from typing import Dict, Any, List, Optional
from src.domain.models import BinaryFile
from src.application.ports import IDatabaseRepository


class JsonRepository(IDatabaseRepository):
    """
    Robust JSON Repository that auto-corrects malformed or legacy JSON structures.
    """

    def __init__(self, json_path: str = "data/database.json"):
        self.json_path = json_path
        self.__ensure_database()

    def __ensure_database(self):
        os.makedirs(os.path.dirname(self.json_path), exist_ok=True)

        # If file doesn't exist → create valid structure
        if not os.path.exists(self.json_path):
            with open(self.json_path, "w") as db:
                json.dump({"records": []}, db, indent=4)
            return

        # If exists → validate structure
        data = self.__read_raw()
        fixed = self.__validate_structure(data)

        # Rewrite if fixed
        with open(self.json_path, "w") as db:
            json.dump(fixed, db, indent=4)

    # --- Basic Safe Readers/Writers ------------------------

    def __read_raw(self):
        try:
            with open(self.json_path, "r") as db:
                return json.load(db)
        except:
            return {"records": []}

    def __read_db(self) -> Dict[str, Any]:
        data = self.__read_raw()
        return self.__validate_structure(data)

    def __write_db(self, content: Dict[str, Any]) -> None:
        with open(self.json_path, "w") as db:
            json.dump(content, db, indent=4)

    # --- Structure Fixer -----------------------------------

    def __validate_structure(self, data):
        """
        Ensures data ALWAYS has format:
            { "records": [ ... ] }
        Even if users break or clear database.json manually.
        """
        # If file is a list → wrap into dict
        if isinstance(data, list):
            return {"records": data}

        # If is dict but missing "records"
        if isinstance(data, dict) and "records" not in data:
            data["records"] = []

        return data

    # --- CRUD ------------------------------------------------

    def add_record(self, record: Any) -> None:
        data = self.__read_db()
        data["records"].append(record)
        self.__write_db(data)

    def get_record(self, file_id: str) -> Optional[BinaryFile]:
        data = self.__read_db()
        for r in data["records"]:
            if r["id"] == file_id:
                return BinaryFile.from_dict(r)
        return None

    def list_records(self) -> List[BinaryFile]:
        data = self.__read_db()
        return [BinaryFile.from_dict(r) for r in data["records"]]

    def update_record(self, file_id: str, updates: Dict[str, Any]) -> bool:
        data = self.__read_db()
        for r in data["records"]:
            if r["id"] == file_id:
                r.update(updates)
                self.__write_db(data)
                return True
        return False

    def delete_record(self, file_id: str) -> bool:
        data = self.__read_db()
        new_records = [r for r in data["records"] if r["id"] != file_id]

        if len(new_records) != len(data["records"]):
            data["records"] = new_records
            self.__write_db(data)
            return True

        return False

    # --- NEW: Find by approval/reject tokens ----------------

    def find_by_approval_token(self, token: str) -> Optional[BinaryFile]:
        """
        Returns BinaryFile linked to an approval token from email link.
        """
        data = self.__read_db()
        for r in data["records"]:
            if r.get("approval_token") == token:
                return BinaryFile.from_dict(r)
        return None

    def find_by_reject_token(self, token: str) -> Optional[BinaryFile]:
        """
        Returns BinaryFile linked to a reject token from email link.
        """
        data = self.__read_db()
        for r in data["records"]:
            if r.get("reject_token") == token:
                return BinaryFile.from_dict(r)
        return None
