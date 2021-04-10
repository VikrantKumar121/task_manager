from django.db import models
from mongoengine import Document, EmbeddedDocument, fields
# Create your models here.

class Organization(Document):
    """"""
    # id = fields.IntField(primary_key=True)
    name = fields.StringField(required=True)
    domain = fields.StringField(unique= True, null =True)
