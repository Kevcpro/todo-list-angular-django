# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_todo_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='todo',
            name='uri',
            field=models.CharField(default='dEfAu', max_length=50),
            preserve_default=False,
        ),
    ]
