import datetime

from django.db import models
from django.utils import timezone

# Create your models here.
class ToDo(models.Model):
    task = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date created')
    status = models.BooleanField(default=False)
    task_id = models.CharField(max_length=50)

    # use __str__(self) for py3
    def __unicode__(self):
        return self.task

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    # ui display in admin page:  'was_published_recently' -> 'Published recently?'
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Created recently?'
