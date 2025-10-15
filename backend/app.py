from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt  #sirve oara encriptar las contraseñas
from marshmallow import Schema, fields, ValidationError
from datetime import timedelta
import os

# Inicializar extensiones
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()
bcrypt = Bcrypt()

def create_app():  #crea la app
    app = Flask(__name__)

    # Configuración básica de la app
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///blog.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #configuracion de JWT
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY") 
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    # Inicializar extensiones
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    CORS(app)


     # Ruta de prueba
    @app.route('/')
    def hello():
        return {"message": "Blog API is running!", "status": "success"}
    
    # Manejo de errores global
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return {"errors": error.messages, "status": "error"}, 400
    
    @app.errorhandler(404)
    def handle_not_found(error):
        return {"message": "Resource not found", "status": "error"}, 404
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        return {"message": "Internal server error", "status": "error"}, 500
    
    return app

# Crear la aplicación
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Crear tablas si no existen
        db.create_all()
    
    app.run(debug=True, host='0.0.0.0', port=5000)


