# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RPM'
        db.create_table('rpmmanager_rpm', (
            ('procblob', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['blobstore.ProcessedBlob'], unique=True, primary_key=True)),
            ('gc', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('protected', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('release', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('epoch', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('arch', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('rpmmanager', ['RPM'])


    def backwards(self, orm):
        # Deleting model 'RPM'
        db.delete_table('rpmmanager_rpm')


    models = {
        'blobstore.blob': {
            'Meta': {'object_name': 'Blob'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'blobstore.processedblob': {
            'Meta': {'object_name': 'ProcessedBlob'},
            'blob': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['blobstore.Blob']", 'unique': 'True', 'primary_key': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hashtype': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'mimetype': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'rpmmanager.rpm': {
            'Meta': {'object_name': 'RPM'},
            'arch': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'epoch': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'gc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'procblob': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['blobstore.ProcessedBlob']", 'unique': 'True', 'primary_key': 'True'}),
            'protected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'release': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['rpmmanager']