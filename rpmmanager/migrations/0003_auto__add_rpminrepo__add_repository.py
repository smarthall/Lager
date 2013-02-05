# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RPMinRepo'
        db.create_table('rpmmanager_rpminrepo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rpm', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rpmmanager.RPM'])),
            ('repo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rpmmanager.Repository'])),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('rpmmanager', ['RPMinRepo'])

        # Adding model 'Repository'
        db.create_table('rpmmanager_repository', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('suspended', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pushed', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('rpmmanager', ['Repository'])


    def backwards(self, orm):
        # Deleting model 'RPMinRepo'
        db.delete_table('rpmmanager_rpminrepo')

        # Deleting model 'Repository'
        db.delete_table('rpmmanager_repository')


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
        'rpmmanager.repository': {
            'Meta': {'object_name': 'Repository'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'pushed': ('django.db.models.fields.DateTimeField', [], {}),
            'rpms': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['rpmmanager.RPM']", 'through': "orm['rpmmanager.RPMinRepo']", 'symmetrical': 'False'}),
            'suspended': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
        },
        'rpmmanager.rpminrepo': {
            'Meta': {'object_name': 'RPMinRepo'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'repo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rpmmanager.Repository']"}),
            'rpm': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['rpmmanager.RPM']"})
        }
    }

    complete_apps = ['rpmmanager']