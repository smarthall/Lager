# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Blob'
        db.create_table('blobstore_blob', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('sha256sum', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('size', self.gf('django.db.models.fields.BigIntegerField')()),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('blobstore', ['Blob'])


    def backwards(self, orm):
        # Deleting model 'Blob'
        db.delete_table('blobstore_blob')


    models = {
        'blobstore.blob': {
            'Meta': {'object_name': 'Blob'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sha256sum': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'size': ('django.db.models.fields.BigIntegerField', [], {})
        }
    }

    complete_apps = ['blobstore']