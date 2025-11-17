from flask import Flask
from flask_cors import CORS
from routes.usuarios import usuarios_bp
from routes.reservas import reservas_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(usuarios_bp, url_prefix="/usuarios")
app.register_blueprint(reservas_bp, url_prefix="/reservas")

if __name__ == "__main__":
    app.run(port=5000, debug=True)