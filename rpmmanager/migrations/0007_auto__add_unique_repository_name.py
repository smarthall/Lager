# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Repository', fields ['name']
        db.create_unique('rpmmanager_repository', ['name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Repository', fields ['name']
        db.delete_unique('rpmmanager_repository', ['name'])


    models = {
        'blobstore.blob': {
            'Meta': {'object_name': 'Blob'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'blobstore.processedblob': {
            'Meta': {'unique_together': "(('hashtype', 'hash'),)", 'object_name': 'ProcessedBlob'},
            'blob': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['blobstore.Blob']", 'unique': 'True', 'primary_key': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hashtype': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'mimetype': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'rpmmanager.repository': {
            'Meta': {'object_name': 'Repository'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'pushed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'rpms': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'repositories'", 'symmetrical': 'False', 'through': "orm['rpmmanager.RPMinRepo']", 'to': "orm['rpmmanager.RPM']"}),
            'suspended': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'rpmmanager.rpm': {
            'Meta': {'unique_together': "(('name', 'version', 'release', 'epoch', 'arch'),)", 'object_name': 'RPM'},
            'arch': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'epoch': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'gc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'procblob': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['blobstore.ProcessedBlob']", 'unique': 'True', 'primary_key': 'True'}),
            'protected': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'release': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'rpmmanager.rpminrepo': {
            'Meta': {'unique_together': "(('rpm', 'repo'),)", 'object_name': 'RPMinRepo'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rpmmanager.Repository']"}),
            'rpm': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rpmmanager.RPM']"})
        }
    }

    complete_apps = ['rpmmanager']