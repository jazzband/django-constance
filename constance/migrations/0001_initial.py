from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Constance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=255, unique=True)),
                ('value', models.TextField(blank=True, editable=False, null=True)),
            ],
            options={
                'verbose_name': 'constance',
                'verbose_name_plural': 'constances',
                'permissions': [('change_config', 'Can change config'), ('view_config', 'Can view config')],
            },
        ),
    ]
