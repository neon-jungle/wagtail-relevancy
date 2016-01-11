# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailrelevancy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reminder',
            name='reminder_interval',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='reminder',
            unique_together=set([('user', 'page')]),
        ),
    ]
