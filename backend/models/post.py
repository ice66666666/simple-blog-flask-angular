from app import db
from datetime import datetime

class Post(db.Model):
    __tablaname__ = 'posts'

    #campos de las tablas
    id = db.Column(db.Interger, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    # Clave foránea - referencia al usuario que creó el post
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    #timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Post {self.title}>' #es para que se vea bonito en consola o logs.
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author_id': self.author_id,
            'author': self.author.username if self.author else None,  # Nombre del autor
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    def is_author(self, user_id):
        """Verifica si un usuario es el autor del post"""
        return self.author_id == user_id
     