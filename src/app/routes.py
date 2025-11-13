# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software.
# Profesor: Jesús Salvador López Ortega.
# Grupo: ISW28.
# Alumno: Veronica Vicente Gaona.
# Archivo:routes.py.
# Descripción: Define la ruta /upload para recibir archivos mediante 
# solicitudes POST. Usa el caso de uso UploadBinaryUseCase junto con 
# los repositorios FileRepository y JsonRepository para procesar y 
# almacenar los archivos binarios según el entorno especificado.
# ============================================================

from flask import request, jsonify, render_template
from src.application.use_cases import UploadBinaryUseCase, ListFilesUseCase
from src.infrastructure.file_repository import FileRepository
from src.infrastructure.json_repository import JsonRepository

def register_routes(app):
    """
    Register HTTP routes for the Flask application.

    This function attaches all routes related to file uploads to the given
    Flask application instance. It defines an endpoint that handles binary
    file uploads and delegates the logic to the UploadBinaryUseCase class.

    Args:
        app (Flask): The Flask application instance used to register routes.

    Routes:
        /upload (POST): 
            Receives a file and an optional environment variable. 
            Executes the upload use case to process the binary file and 
            returns the file ID and its upload status in JSON format.
    """
    @app.route("/")
    def home():
        repo = JsonRepository()
        use_case = ListFilesUseCase(repo)
        files = use_case.execute()
        return render_template("home.html", files=files)
    

    @app.route("/upload", methods=["POST"])
    def upload_file():
        # Retrieve file and environment from the request 
        file = request.files['file']
        environment = request.form.get('environment', 'dev')

        
        # Execute the use case with appropiate repositories
        use_case = UploadBinaryUseCase(FileRepository(), JsonRepository())
        binary = use_case.execute(file, environment)

      # Return JSON response with binary metadata
        return jsonify({
            'id': binary.id,
            'filename': binary.filename,
            'environment': binary.environment,
            'status': binary.status,
            'signature': getattr(binary, 'signature', None),
            'uploaded_at': getattr(binary, 'uploaded_at', None),
            'signed_path': getattr(binary, 'signed_path', None)
        }), 200
