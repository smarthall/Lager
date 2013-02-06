# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Repository.pushed'
        db.delete_column('rpmmanager_repository', 'pushed')


    def backwards(self, orm):
        # Adding field 'Repository.pushed'
        db.add_column('rpmmanager_repository', 'pushed',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)


    models = {
        'blobstore.datablob': {
            'Meta': {'unique_together': "(('hashtype', 'hash'),)", 'object_name': 'DataBlob'},
            'blob': ('django.db.models.fields.files.FileField', [], {'max_length': '150'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'hashtype': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mimetype': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'rpmmanager.repository': {
            'Meta': {'object_name': 'Repository'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'rpms': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'repositories'", 'symmetrical': 'False', 'through': "orm['rpmmanager.RPMinRepo']", 'to': "orm['rpmmanager.RPM']"}),
            'suspended': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'rpmmanager.rpm': {
            'Meta': {'unique_together': "(('name', 'version', 'release', 'epoch', 'arch'),)", 'object_name': 'RPM'},
            'arch': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'epoch': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'gc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'procblob': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['blobstore.DataBlob']", 'unique': 'True', 'primary_key': 'True'}),
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