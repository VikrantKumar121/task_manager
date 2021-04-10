from django.db import models
from mongoengine import Document, EmbeddedDocument, fields
import mongoengine
from user.models import User
from django.utils import timezone
from organization.models import Organization
import datetime
# Create your models here.

class Project(Document):
    """"""
    name = fields.StringField(required=True)
    description = fields.StringField()
    maintainer  = fields.ReferenceField('User',required = True, reverse_delete_rule=mongoengine.CASCADE)
    organization  = fields.ReferenceField('Organization', required = True, reverse_delete_rule=mongoengine.CASCADE)
    start_date  = fields.DateField()
    end_date = fields.DateField()
    created_on = fields.DateTimeField()
    modified_on = fields.DateTimeField(default=datetime.datetime.now())
    time = fields.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.created_on:
            self.created_on = datetime.datetime.now()
        self.modified_on = datetime.datetime.now()
        return super(Project, self).save(*args, **kwargs)
