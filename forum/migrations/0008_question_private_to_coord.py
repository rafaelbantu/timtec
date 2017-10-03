# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_questionnotification'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='private_to_coord',
            field=models.BooleanField(default=False, verbose_name='Private'),
        ),
    ]
