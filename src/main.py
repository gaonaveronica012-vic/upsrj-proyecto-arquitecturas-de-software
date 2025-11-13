# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software.
# Profesor: Jesús Salvador López Ortega.
# Grupo: ISW28.
# Alumno: Veronica Vicente Gaona.
# Archivo: main.py.
# Descripción: Archivo principal del proyecto.
# ============================================================
from cryptography.fernet import Fernet
from flask import Flask, render_template
from common.vars import TEMPLATES_DIR, Hosts



app =  Flask(__name__)

@app.route("/")
def home():

    # Put this somewhere safe!
    key = Fernet.generate_key()
    f = Fernet(key)
    token = f.encrypt(b"A really secret message. Not for prying eyes.")
    message = f.encrypt(token)

    return render_template("home.html", token=token, message=message)
if __name__== "__main__":
    host, port = Hosts().main
app.run(host=host, port=port)
    