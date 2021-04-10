from django.db import models
from django.db import models
from mongoengine import Document, EmbeddedDocument, fields
import mongoengine
from user.models import User
from project.models import Project
from django.utils import timezone
import datetime
# Create your models here.

PHASES_CHOICE = (
    'TODO',
    'Process',
    'Test',
    'Done'
)

class Task(Document):
    """"""
    name = fields.StringField(required = True)
    description = fields.StringField()
    start_date  = fields.DateField()
    end_date = fields.DateField()
    phase = fields.StringField(choices=PHASES_CHOICE, required=True)
    project = fields.ReferenceField('Project',required=True, reverse_delete_rule=mongoengine.CASCADE)
    assignee = fields.ReferenceField('User', required = True, reverse_delete_rule=mongoengine.CASCADE)
    reporter = fields.ReferenceField('User', reverse_delete_rule=mongoengine.NULLIFY)
    comments = fields.StringField(null = True)
    created_on = fields.DateTimeField()
    modified_on = fields.DateTimeField(default=datetime.datetime.now())
    parent_task = fields.ReferenceField('self', required = False, blank = True, null = True, reverse_delete_rule=mongoengine.CASCADE)

    def save(self, *args, **kwargs):
        if not self.created_on:
            self.created_on = datetime.datetime.now()
        self.modified_on = datetime.datetime.now()
        return super(Task, self).save(*args, **kwargs)

class SubTask(Document):
    """"""
    task = fields.ReferenceField('Task', required = True, unique=True, reverse_delete_rule=mongoengine.CASCADE)
    created_on = fields.DateTimeField()
    modified_on = fields.DateTimeField(default=datetime.datetime.now())
    task_parent = fields.ReferenceField('Task', required = False, null = True, blank = True, unique = False)
    sub_task = fields.ListField(fields.ReferenceField('Task', required = False, null = True, reverse_delete_rule=mongoengine.PULL),blank=True)

    def save(self, *args, **kwargs):
        if not self.created_on:
            self.created_on = datetime.datetime.now()
        self.modified_on = datetime.datetime.now()
        return super(SubTask, self).save(*args, **kwargs)
