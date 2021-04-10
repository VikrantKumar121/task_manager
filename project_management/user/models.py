from django.db import models
from mongoengine import Document, EmbeddedDocument, fields
import mongoengine
from organization.models import Organization
from mongoengine import signals  #blinker library may need to be installed
from bcrypt import hashpw, gensalt
import datetime
# class User(Document):
#     # id = fields.IntField(primary_key=True)
#     username = fields.StringField(required=True)
#     email = fields.EmailField()
#     organization = fields.ReferenceField('Organization', reverse_delete_rule=mongoengine.CASCADE)

from mongo_auth.utils import create_unique_object_id
class User(Document):
    email = fields.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        required=True
        )
    password = fields.StringField(required=True, min_length=6)
    first_name = fields.StringField(max_length=50, unique=False)
    last_name = fields.StringField(max_length=50, unique=False,null=True, blank=True)
    phone_number = fields.StringField(max_length=10,  null=False, blank=False)
    recovery_phone =fields.StringField(max_length=10,  null=True, blank=True)
    is_active = fields.BooleanField(default=True)
    is_staff = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)
    organization = fields.ReferenceField('Organization', required = False, null=True, reverse_delete_rule=mongoengine.NULLIFY)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Tells Django that the UserManager class defined above should manage
    # objects of this type.
    @classmethod
    def pre_save(cls, sender, document, **kwargs):
        hashed = hashpw(document.password.encode('utf8'), gensalt())
        document.password = hashed.decode('utf8')
    def __str__(self):
        return self.email

    def name(self):
        return f'{self.first_name} {self.last_name}'

signals.pre_save.connect(User.pre_save, sender=User)

class BlackListedToken(Document):
    user = fields.ReferenceField(User, related_name="token_user", reverse_delete_rule=mongoengine.CASCADE)
    token = fields.StringField(max_length=500, unique_with = 'user')
    timestamp = fields.DateTimeField(default = datetime.datetime.now())

    class Meta:
        unique_together = ("token", "user")
