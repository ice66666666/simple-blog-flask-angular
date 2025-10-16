from database import db, bcrypt
from datetime import datetime
from flask_jwt_extended import create_access_token

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100),unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # Timestamps  es para registrar el tiempo de creacion y actualizacion cuando , donde  y quien lo modifico
    created_at = db.Column(db.DateTime, default=datetime.utcnow) #utcnow es para la hora actual
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    #onupdate actualiza automáticamente el campo cada vez que se edite.

    #relacion con post(un usuario puede tener muchos posts) - temporalmente comentada
    # posts = db.relationship('Post', backref='author', lazy=True, cascade='all, delete-orphan') #lazy=True hace que las publicaciones se carguen solo cuando se necesiten.

    def __repr__(self): #Se usa para definir cómo se verá tu objeto cuando lo imprimas o lo veas en consola.
        return f"<User {self.username}>" #Solo sirve para mostrarlo bonito en consola o logs.

    #metodo  de seguridad para encriptar y verificar las contraseñas
    def set_password(self, password): #Encripta y guarda la contraseña
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password): #Verifica si la contraseña es correcta
        return bcrypt.check_password_hash(self.password_hash, password)

    def generate_token(self):
        """Genera un token de acceso JWT usando el id del usuario."""
        return create_access_token(identity=self.id)

    def to_dict(self):
        """Convierte el usuario a diccionario (sin contraseña)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

        

