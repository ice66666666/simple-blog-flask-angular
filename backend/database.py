from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# Crear instancias globales únicas
db = SQLAlchemy()
bcrypt = Bcrypt()
