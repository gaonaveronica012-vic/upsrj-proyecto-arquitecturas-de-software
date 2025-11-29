# ============================================================
# Politécnica de Santa Rosa.
# Materia: Arquitecturas de Software.
# Profesor: Jesús Salvador López Ortega.
# Grupo: ISW28.
# Alumna: Veronica Vicente Gaona.
# Archivo: routes.py
# ============================================================
# Descripción:
# Este archivo define todas las rutas principales de la aplicación
# OTA Signer utilizando el framework Flask. Aquí se gestiona el
# flujo completo del sistema de firmado digital, incluyendo:
#
#   - Carga de binarios
#   - Aprobación y rechazo desde el panel
#   - Envío de notificaciones por correo
#   - Firmado automático para producción
#   - Tokens de aprobación/rechazo vía correo
#
# Las rutas funcionan como capa de presentación, conectando las
# solicitudes del usuario con los casos de uso del dominio, y
# construyendo dinámicamente la infraestructura necesaria en cada
# operación, siguiendo una arquitectura limpia y modular.
# ============================================================
# src/app/routes.py
from flask import request, jsonify, render_template, redirect, url_for
import os

from src.application.use_cases import (
    UploadBinaryUseCase,
    ListFilesUseCase,
    SignBinaryUseCase,
    ApproveBinaryUseCase,
    RejectBinaryUseCase,
)

from src.infrastructure.file_repository import FileRepository
from src.infrastructure.json_repository import JsonRepository
from src.infrastructure.crypto_adapter import CryptoAdapter
from src.infrastructure.email_notifier import EmailNotifier


def register_routes(app):

    # HOME
    @app.route("/")
    def home():
        repo = JsonRepository()
        use_case = ListFilesUseCase(repo)
        files = use_case.execute()
        return render_template("home.html", files=files)


    # Shared infrastructure
    def _build_infra():
        file_repo = FileRepository()
        json_repo = JsonRepository()
        crypto = CryptoAdapter(file_repo)

        # 🔥 Configuración fija de correo (sin .env)
        notifier = EmailNotifier(
            sender_email="vicentever427@gmail.com",
            sender_password="qwiw ljey ahnp uuxt",
            default_receiver="gavicov29@gmail.com"
        )

        return file_repo, json_repo, crypto, notifier




    # ============================================
    # UPLOAD
    # ============================================
    @app.route("/upload", methods=["POST"])
    def upload_file():
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        environment = request.form.get("environment", "dev")

        file_repo, json_repo, crypto, notifier = _build_infra()
        use_case = UploadBinaryUseCase(file_repo, json_repo, crypto, notifier)
        binary = use_case.execute(file, environment)

        return jsonify(binary.to_dict()), 200


    # ============================================
    # APPROVE FROM PANEL (by file_id)
    # ============================================
    @app.route("/approve/<file_id>", methods=["POST"])
    def approve_file(file_id):
        file_repo, json_repo, crypto, notifier = _build_infra()
        use_case = ApproveBinaryUseCase(json_repo, crypto, notifier)
        result = use_case.execute(file_id)

        if result is None:
            return jsonify({"error": "File not found or cannot be approved"}), 404

        return redirect(url_for("home"))


    # ============================================
    # REJECT FROM PANEL (by file_id)
    # ============================================
    @app.route("/reject/<file_id>", methods=["POST"])
    def reject_file(file_id):
        file_repo, json_repo, crypto, notifier = _build_infra()
        use_case = RejectBinaryUseCase(json_repo, notifier)
        result = use_case.execute(file_id)

        if result is None:
            return jsonify({"error": "File not found or cannot be rejected"}), 404

        return redirect(url_for("home"))


    # ============================================
    # SIGN (manual via AJAX request)
    # ============================================
    @app.route("/signing", methods=["POST"])
    def sign_file():
        data = request.json or request.form or request.args
        file_id = data.get("file_id")
        if not file_id:
            return jsonify({"error": "file_id is required"}), 400

        file_repo, json_repo, crypto, notifier = _build_infra()
        use_case = SignBinaryUseCase(json_repo, crypto, notifier)
        binary = use_case.execute(file_id)

        if binary is None:
            return jsonify({"error": "Cannot sign file (not found or wrong status)"}), 400

        return jsonify({"message": "File signed successfully", **binary.to_dict()}), 200


    # =====================================================
    # EMAIL APPROVAL via TOKEN
    # =====================================================
    @app.route("/email/approve/<token>", methods=["GET"])
    def approve_via_email(token):
        file_repo, json_repo, crypto, notifier = _build_infra()
        binary = json_repo.find_by_approval_token(token)

        if not binary:
            return "Token inválido o archivo no encontrado", 404

        # Ejecuta el caso de uso normal
        approve_usecase = ApproveBinaryUseCase(json_repo, crypto, notifier)
        result = approve_usecase.execute(binary.id)

        if result is None:
            return "El archivo no pudo ser aprobado", 400

        return render_template("email_action_success.html", message="Archivo aprobado y firmado con éxito")


    # =====================================================
    # EMAIL REJECTION via TOKEN
    # =====================================================
    @app.route("/email/reject/<token>", methods=["GET"])
    def reject_via_email(token):
        file_repo, json_repo, crypto, notifier = _build_infra()
        binary = json_repo.find_by_reject_token(token)

        if not binary:
            return "Token inválido o archivo no encontrado", 404

        reject_usecase = RejectBinaryUseCase(json_repo, notifier)
        result = reject_usecase.execute(binary.id)

        if result is None:
            return "El archivo no pudo ser rechazado", 400

        return render_template("email_action_success.html", message="Archivo rechazado correctamente")
