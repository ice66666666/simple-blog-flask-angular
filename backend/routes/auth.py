from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from database import db
from models import User
from schemas.user_schema import UserRegistrationSchema, UserLoginSchema
from marshmallow import ValidationError

# Crear Blueprint para las rutas de autenticación
auth_bp = Blueprint('auth', __name__)

#Registro de nuevos usuarios
@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        # Validar datos con Marshmallow
        schema = UserRegistrationSchema()  # sirve para crear un validador
        data = schema.load(request.get_json())  # sirve para validar y limpiar los datos
        
        # Crear nuevo usuario
        user = User(
            username=data['username'],
            email=data['email']
        )
        
        # Encriptar contraseña
        user.set_password(data['password'])  # sirve para encriptar la contraseña antes de guardarla
        
        # Guardar en base de datos
        db.session.add(user)
        db.session.commit()
        
        # Generar token JWT
        token = user.generate_token()
        
        return jsonify({
            'message': 'Usuario registrado exitosamente',
            'token': token,
            'user': user.to_dict(),
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

#Login de usuarios existentes
@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        # Validar datos con Marshmallow
        schema = UserLoginSchema()
        data = schema.load(request.get_json())
        
        # Buscar usuario por email
        user = User.query.filter_by(email=data['email']).first()
        
        if not user:
            return jsonify({
                'message': 'Credenciales inválidas',
                'status': 'error'
            }), 401  # sirve para error de autenticación (credenciales inválidas)
        
        # Verificar contraseña
        if not user.check_password(data['password']):  # sirve para comparar contraseña encriptada con la ingresada
            return jsonify({
                'message': 'Credenciales inválidas',
                'status': 'error'
            }), 401  # sirve para error de autenticación (credenciales inválidas)
        
        # Generar token JWT
        token = user.generate_token()
        
        return jsonify({
            'message': 'Login exitoso',
            'token': token,
            'user': user.to_dict(),
            'status': 'success'
        }), 200
        
    except ValidationError as err:
        return jsonify({
            'errors': err.messages,
            'status': 'error'
        }), 400  # sirve para error de validación (datos malos del cliente)
        
    except Exception as e:
        return jsonify({
            'message': 'Error interno del servidor',
            'status': 'error'
        }), 500  # sirve para error interno del servidor (problema de BD o sistema)

#Obtener perfil del usuario autenticado
@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        # Obtener ID del usuario desde el token
        user_id = get_jwt_identity()
        
        # Buscar usuario
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'message': 'Usuario no encontrado',
                'status': 'error'
            }), 404  # sirve para error de recurso no encontrado (usuario no existe)
        
        return jsonify({
            'user': user.to_dict(),
            'status': 'success'
        }), 200
        
    except Exception as e:
        return jsonify({
            'message': 'Error interno del servidor',
            'status': 'error'
        }), 500  # sirve para error interno del servidor (problema de BD o sistema)    
