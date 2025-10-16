#!/usr/bin/env python3
"""
Script para inicializar la base de datos
"""

from app import create_app
from database import db
from models import User, Post

def init_db():
    """Inicializar la base de datos y crear tablas"""
    app = create_app()
    
    with app.app_context():
        # Crear todas las tablas
        db.create_all()
        print("✅ Tablas creadas correctamente")
        
        # Verificar que las tablas existen
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"📋 Tablas en la base de datos: {tables}")
        
        # Crear un usuario de prueba si no existe
        test_user = User.query.filter_by(email='test@example.com').first()
        if not test_user:
            test_user = User(
                username='testuser',
                email='test@example.com'
            )
            test_user.set_password('password123')
            db.session.add(test_user)
            db.session.commit()
            print("✅ Usuario de prueba creado")
        
        # Crear un post de prueba si no existe
        test_post = Post.query.first()
        if not test_post:
            test_post = Post(
                title='Bienvenido al Blog',
                content='Este es el primer post del blog. ¡Bienvenido!',
                author_id=test_user.id
            )
            db.session.add(test_post)
            db.session.commit()
            print("✅ Post de prueba creado")
        
        print("🎉 Base de datos inicializada correctamente")

if __name__ == '__main__':
    init_db()
