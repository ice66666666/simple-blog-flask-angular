from marshmallow import Schema, fields, validate

class PostSchema(Schema):
    title = fields.Str(
        required = True,
        validate = [
            validate.Length(min=1, max=200),
            validate.Regexp(r'^.+$', error='Título no puede estar vacío')
        ]
    )

    content = fields.Str(
        required = True,
        validate =[
            validate.Length(min=1, max=5000),
            validate.Regexp(r'^.+$', error='Contenido no puede estar vacío')
        ]
    )
