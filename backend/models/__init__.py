# Importar todos los modelos para que SQLAlchemy pueda resolver las relaciones
from database import db, bcrypt
from models.user import User
from models.post import Post

# Exportar todo
__all__ = ['User', 'Post', 'db', 'bcrypt']
