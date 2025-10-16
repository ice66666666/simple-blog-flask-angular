from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt  #sirve oara encriptar las contraseñas
from marshmallow import Schema, fields, ValidationError
from datetime import timedelta
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env si existe (solo en desarrollo local)
if os.path.exists('.env'):
    load_dotenv()

# Importar las instancias de los modelos
from database import db, bcrypt
from models import User, Post

# Inicializar otras extensiones
jwt = JWTManager()
migrate = Migrate()

def create_app():  #crea la app
    app = Flask(__name__)

    # Configuración básica de la app
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", 'dev_secret')
    # Configure database URI: prefer explicit DATABASE_URL, otherwise build from POSTGRES_* env vars, else fallback to sqlite
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        pg_user = os.environ.get('POSTGRES_USER')
        pg_pass = os.environ.get('POSTGRES_PASSWORD')
        pg_db = os.environ.get('POSTGRES_DB')
        if pg_user and pg_pass and pg_db:
            database_url = f'postgresql://{pg_user}:{pg_pass}@db:5432/{pg_db}'
        else:
            database_url = 'sqlite:///blog.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    #configuracion de JWT
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", 'dev_jwt_secret')
    # JWT_ACCESS_TOKEN_EXPIRES puede ser un entero en segundos
    try:
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    except ValueError:
        app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600
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
    
    # Registrar Blueprints
    from routes.auth import auth_bp
    from routes.posts import posts_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(posts_bp, url_prefix='/api/posts')
    
    return app

# Crear la aplicación
app = create_app()

if __name__ == '__main__':
    # Para inicializar la base de datos, usar `init_db.py` o migraciones.
    app.run(debug=True, host='0.0.0.0', port=5000)


