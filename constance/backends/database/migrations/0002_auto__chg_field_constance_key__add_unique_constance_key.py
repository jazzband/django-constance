# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Changing field 'Constance.key'
        db.alter_column('constance_config', 'key',
                        self.gf('django.db.models.fields.CharField')(
                            max_length=255))
        # Adding unique constraint on 'Constance', fields ['key']
        db.create_unique('constance_config', ['key'])

    def backwards(self, orm):
        # Removing unique constraint on 'Constance', fields ['key']
        db.delete_unique('constance_config', ['key'])

        # Changing field 'Constance.key'
        db.alter_column('constance_config', 'key',
                        self.gf('django.db.models.fields.TextField')())

    models = {
        'database.constance': {
            'Meta': {'object_name': 'Constance',
                     'db_table': "'constance_config'"},
            'id': ('django.db.models.fields.AutoField', [],
                   {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [],
                    {'unique': 'True', 'max_length': '255'}),
            'value': ('picklefield.fields.PickledObjectField', [], {})
        }
    }

    complete_apps = ['database']
