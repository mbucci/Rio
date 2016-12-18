from marshmallow import Schema, fields

class Base(Schema):
	id = fields.Integer()


class Unicode(fields.Field):
    def _serialize(self, value, attr, obj):
        if not value:
            return ''
        return value.decode('utf-8')

