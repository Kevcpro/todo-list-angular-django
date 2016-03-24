from django.db import models
from django.utils import timezone

import datetime

class Question(models.Model):
    # type: Field, field(column) name: question_text
    question_text = models.CharField(max_length=200)
    # design a human readable name
    pub_date = models.DateTimeField('date published')

    # for display in Dj interactive shell
    def __unicode__(self):  # use __str__(self) for py3
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    # ui display in admin page:  'was_published_recently' -> 'Published recently?'
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question)   # many-to-one
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    # for display in Dj interactive shell
    def __unicode__(self): # use __str__(self) for py3
        return self.choice_text


# for todo website
class ToDo(models.Model):
    task = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date created')
    status = models.BooleanField(default=False)
    uri = models.CharField(max_length=50)

    # use __str__(self) for py3
    def __unicode__(self):
        return self.task

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    # ui display in admin page:  'was_published_recently' -> 'Published recently?'
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Created recently?'
