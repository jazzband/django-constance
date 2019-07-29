# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import picklefield.fields


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name='ConfigLogEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True,
                                        auto_created=True, serialize=False)),
                ('key', models.CharField(max_length=255)),
                ('old_value', picklefield.fields.PickledObjectField(editable=False)),
                ('new_value', picklefield.fields.PickledObjectField(editable=False)),
            ],
        ),
    ]
