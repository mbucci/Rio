from marshmallow import Schema, fields

from base import Base, Unicode


class WorldLookupSchema(Base):

	name = Unicode(required=True)
