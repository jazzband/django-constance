# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Constance'
        db.create_table('constance_config', (
            ('id', self.gf('django.db.models.fields.AutoField')(
                primary_key=True)),
            ('key', self.gf('django.db.models.fields.TextField')()),
            ('value', self.gf('picklefield.fields.PickledObjectField')()),
        ))
        db.send_create_signal('database', ['Constance'])

    def backwards(self, orm):
        # Deleting model 'Constance'
        db.delete_table('constance_config')

    models = {
        'database.constance': {
            'Meta': {'object_name': 'Constance',
                     'db_table': "'constance_config'"},
            'id': ('django.db.models.fields.AutoField', [],
                   {'primary_key': 'True'}),
            'key': ('django.db.models.fields.TextField', [], {}),
            'value': ('picklefield.fields.PickledObjectField', [], {})
        }
    }

    complete_apps = ['database']
