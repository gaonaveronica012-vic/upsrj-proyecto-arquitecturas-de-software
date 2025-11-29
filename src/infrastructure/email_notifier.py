# ============================================================
# Politécnica de Santa Rosa
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Alumna: Veronica Vicente Gaona
# Archivo: email_notifier.py
# ============================================================
# Descripción:
# Implementa un servicio real de notificaciones por correo
# usando Gmail SMTP. Envía mensajes para estados: PENDING,
# SIGNED y REJECTED.
# ============================================================

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from src.application.ports import INotifierService
from src.domain.models import BinaryFile


class EmailNotifier(INotifierService):

    def __init__(self, sender_email: str, sender_password: str, default_receiver: str = None):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.default_receiver = default_receiver


    # ============================================================
    # 1) Solicitud de aprobación (PENDING)
    # ============================================================
    def send_approval_request(self, binary: BinaryFile) -> None:

        subject = f"OTA Signer - Solicitud de aprobación | {binary.filename}"

        body = f"""
        <h2>Solicitud de Aprobación</h2>
        <p>Un archivo ha sido cargado y requiere revisión.</p>

        <b>Archivo:</b> {binary.filename}<br>
        <b>ID:</b> {binary.id}<br>
        <b>Estado actual:</b> PENDING<br><br>

        <p>Por favor revisa el panel de administración y aprueba para continuar con la firma digital.</p>
        """

        self._send_email_html(self.default_receiver, subject, body)


    # ============================================================
    # 2) Archivo firmado exitosamente (SIGNED)
    # ============================================================
    def send_signed_confirmation(self, binary: BinaryFile) -> None:

        subject = f"OTA Signer - Archivo firmado | {binary.filename}"

        body = f"""
        <h2>Archivo Firmado</h2>
        <p>El archivo ha sido firmado con éxito.</p>

        <b>Archivo:</b> {binary.filename}<br>
        <b>ID:</b> {binary.id}<br>
        <b>Ruta firmada:</b> {binary.signed_path}<br><br>

        <p>La firma ya está disponible.</p>
        """

        self._send_email_html(self.default_receiver, subject, body)


    # ============================================================
    # 3) Archivo RECHAZADO (REJECTED)
    # ============================================================
    def send_rejection_notification(self, binary: BinaryFile) -> None:

        subject = f"OTA Signer - Archivo Rechazado | {binary.filename}"

        body = f"""
        <h2>Archivo Rechazado</h2>

        <p>El archivo ha sido revisado pero NO fue aprobado.</p>

        <b>Archivo:</b> {binary.filename}<br>
        <b>ID:</b> {binary.id}<br>
        <b>Estado:</b> REJECTED<br><br>

        <p>Si es necesario, vuelve a cargar una nueva versión del archivo.</p>
        """

        self._send_email_html(self.default_receiver, subject, body)


    # ============================================================
    # MÉTODO CENTRAL DE ENVÍO (HTML)
    # ============================================================
    def _send_email_html(self, to_email: str, subject: str, body_html: str):

        msg = MIMEMultipart("alternative")
        msg["From"] = self.sender_email
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body_html, "html"))

        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, to_email, msg.as_string())
            server.quit()

            print(f"[EMAIL OK] → {to_email} | {subject}")

        except Exception as e:
            print("\n" + "="*60)
            print("ERROR EN ENVÍO DE CORREO")
            print(f"Destinatario: {to_email}")
            print(f"Asunto: {subject}")
            print(f"Error: {e}")
            print("="*60 + "\n")
