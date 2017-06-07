# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import picklefield.fields


class Migration(migrations.Migration):
    replaces = [('database', '0001_initial')]

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Constance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True,
                                        auto_created=True, serialize=False)),
                ('key', models.CharField(unique=True, max_length=255)),
                ('value', picklefield.fields.PickledObjectField(editable=False)),
            ],
            options={
                'verbose_name': 'constance',
                'verbose_name_plural': 'constances',
                'db_table': 'constance_config',
            },
            bases=(models.Model,),
        ),
    ]
