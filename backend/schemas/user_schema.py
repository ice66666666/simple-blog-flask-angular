from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from app import db
from models.user import User


class UserSchema(Schema): #es para validar los datos que se envian al servidor de un usuario

    #campos para el registro
    username = fields.Str(
        required = True,
        validate =[
            validate.Length(min=3, max=20),
            validate.Regexp(r'^[a-zA-Z0-9_]+$', error='Username solo puede contener letras, números y guiones bajos')
        ]
    )

    email = fields.Email(required = True)

    password = fields.Str(
        required = True,
        validate = validate.Length(min=8, max=50)  #
    )
    # validate.Regexp(r'^[A-Z].*$', error='Password debe empezar con mayúscula')

    #Verifica que el email sea único
    @validates_schema
    def validate_email_unique(self, data, **kwargs):
        if 'email' in data:
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                raise ValidationError('Email ya está en uso', 'email')
    
    #Verifica que el username sea único
    @validates_schema
    def validate_username_unique(self, data, **kwargs):
        if 'username' in data:
            existing_user = User.query.filter_by(username=data['username']).first()
            if existing_user:
                raise ValidationError('Username ya está en uso', 'username')

    # Esquemas específicos para diferentes operaciones
    #Esquema para registro de usuarios
class UserRegistrationSchema(UserSchema): 
    pass

#Esquema para login de usuarios
class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)

#Esquema para actualizar usuario
class UserUpdateSchema(Schema):
    username = fields.Str(
        validate=[
            validate.Length(min=3, max=20),
            validate.Regexp(r'^[a-zA-Z0-9_]+$', error='Username solo puede contener letras, números y guiones bajos')
        ]
    )
    email = fields.Email()
    new_password = fields.Str(validate=validate.Length(min=6, max=100))
