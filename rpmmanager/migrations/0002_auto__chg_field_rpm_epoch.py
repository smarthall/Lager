# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'RPM.epoch'
        db.alter_column('rpmmanager_rpm', 'epoch', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

    def backwards(self, orm):

        # Changing field 'RPM.epoch'
        db.alter_column('rpmmanager_rpm', 'epoch', self.gf('django.db.models.fields.CharField')(default=None, max_length=50))

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
            'epoch': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'gc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'procblob': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['blobstore.ProcessedBlob']", 'unique': 'True', 'primary_key': 'True'}),
            'protected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'release': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['rpmmanager']