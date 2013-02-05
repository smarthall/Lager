# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DataBlob'
        db.create_table('blobstore_datablob', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('blob', self.gf('django.db.models.fields.files.FileField')(max_length=150)),
            ('hashtype', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('mimetype', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=150)),
        ))
        db.send_create_signal('blobstore', ['DataBlob'])

        # Adding unique constraint on 'DataBlob', fields ['hashtype', 'hash']
        db.create_unique('blobstore_datablob', ['hashtype', 'hash'])


    def backwards(self, orm):
        # Removing unique constraint on 'DataBlob', fields ['hashtype', 'hash']
        db.delete_unique('blobstore_datablob', ['hashtype', 'hash'])

        # Deleting model 'DataBlob'
        db.delete_table('blobstore_datablob')


    models = {
        'blobstore.datablob': {
            'Meta': {'unique_together': "(('hashtype', 'hash'),)", 'object_name': 'DataBlob'},
            'blob': ('django.db.models.fields.files.FileField', [], {'max_length': '150'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hashtype': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mimetype': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['blobstore']