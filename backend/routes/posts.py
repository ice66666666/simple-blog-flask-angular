from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import Post, User
from schemas.post_schema import PostSchema
from marshmallow import ValidationError

# Crear Blueprint para las rutas de posts
posts_bp = Blueprint('posts', __name__)

#Obtener todos los posts
@posts_bp.route('/', methods=['GET'])
def get_all_posts():
    try:
        # Obtener todos los posts con información del autor
        posts = Post.query.join(User).all()  # sirve para traer posts Y datos del autor en una sola consulta
        
        posts_data = []
        for post in posts:
            post_dict = post.to_dict()
            posts_data.append(post_dict)
        
        return jsonify({
            'posts': posts_data,
            'count': len(posts_data),
            'status': 'success'
        }), 200
        
    except Exception as e:
        return jsonify({
            'message': 'Error interno del servidor',
            'status': 'error'
        }), 500  # sirve para error interno del servidor (problema de BD o sistema)

#Obtener un post específico por ID
@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    try:
        post = Post.query.get(post_id)
        
        if not post:
            return jsonify({
                'message': 'Post no encontrado',
                'status': 'error'
            }), 404  # sirve para error de recurso no encontrado (post no existe)
        
        return jsonify({
            'post': post.to_dict(),
            'status': 'success'
        }), 200
        
    except Exception as e:
        return jsonify({
            'message': 'Error interno del servidor',
            'status': 'error'
        }), 500  # sirve para error interno del servidor (problema de BD o sistema)

#Crear un nuevo post (solo usuarios autenticados)
@posts_bp.route('/', methods=['POST'])
@jwt_required()
def create_post():
    try:
        # Validar datos con Marshmallow
        schema = PostSchema()
        data = schema.load(request.get_json())
        
        # Obtener ID del usuario desde el token
        user_id = get_jwt_identity()
        
        # Crear nuevo post
        post = Post(
            title=data['title'],
            content=data['content'],
            author_id=user_id
        )
        
        # Guardar en base de datos
        db.session.add(post)  # sirve para agregar el post a la sesión de BD
        db.session.commit()    # sirve para guardar permanentemente en la BD
        
        return jsonify({
            'message': 'Post creado exitosamente',
            'post': post.to_dict(),
            'status': 'success'
        }), 201
        
    except ValidationError as err:
        return jsonify({
            'errors': err.messages,
            'status': 'error'
        }), 400  # sirve para error de validación (datos malos del cliente)
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Error interno del servidor',
            'status': 'error'
        }), 500  # sirve para error interno del servidor (problema de BD o sistema)

#Actualizar un post (solo el autor)
@posts_bp.route('/<int:post_id>', methods=['PUT'])
@jwt_required()
def update_post(post_id):
    try:
        # Validar datos con Marshmallow
        schema = PostSchema()
        data = schema.load(request.get_json())
        
        # Obtener ID del usuario desde el token
        user_id = get_jwt_identity()
        
        # Buscar el post
        post = Post.query.get(post_id)
        
        if not post:
            return jsonify({
                'message': 'Post no encontrado',
                'status': 'error'
            }), 404  # sirve para error de recurso no encontrado (post no existe)
        
        # Verificar que el usuario sea el autor
        if post.author_id != user_id:  # sirve para verificar que solo el autor puede editar/eliminar
            return jsonify({
                'message': 'No tienes permisos para editar este post',
                'status': 'error'
            }), 403  # sirve para error de permisos (usuario no es el autor)
        
        # Actualizar el post
        post.title = data['title']
        post.content = data['content']
        
        # Guardar cambios
        db.session.commit()
        
        return jsonify({
            'message': 'Post actualizado exitosamente',
            'post': post.to_dict(),
            'status': 'success'
        }), 200
        
    except ValidationError as err:
        return jsonify({
            'errors': err.messages,
            'status': 'error'
        }), 400  # sirve para error de validación (datos malos del cliente)
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Error interno del servidor',
            'status': 'error'
        }), 500  # sirve para error interno del servidor (problema de BD o sistema)

#Eliminar un post (solo el autor)
@posts_bp.route('/<int:post_id>', methods=['DELETE'])
@jwt_required()
def delete_post(post_id):
    try:
        # Obtener ID del usuario desde el token
        user_id = get_jwt_identity()
        
        # Buscar el post
        post = Post.query.get(post_id)
        
        if not post:
            return jsonify({
                'message': 'Post no encontrado',
                'status': 'error'
            }), 404  # sirve para error de recurso no encontrado (post no existe)
        
        # Verificar que el usuario sea el autor
        if post.author_id != user_id:
            return jsonify({
                'message': 'No tienes permisos para eliminar este post',
                'status': 'error'
            }), 403  # sirve para error de permisos (usuario no es el autor)
        
        # Eliminar el post
        db.session.delete(post)
        db.session.commit()
        
        return jsonify({
            'message': 'Post eliminado exitosamente',
            'status': 'success'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'message': 'Error interno del servidor',
            'status': 'error'
        }), 500  # sirve para error interno del servidor (problema de BD o sistema)

