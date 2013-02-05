# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RPM'
        db.create_table('rpmmanager_rpm', (
            ('procblob', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['blobstore.DataBlob'], unique=True, primary_key=True)),
            ('protected', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('gc', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('release', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('epoch', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('arch', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('rpmmanager', ['RPM'])

        # Adding unique constraint on 'RPM', fields ['name', 'version', 'release', 'epoch', 'arch']
        db.create_unique('rpmmanager_rpm', ['name', 'version', 'release', 'epoch', 'arch'])

        # Adding model 'Repository'
        db.create_table('rpmmanager_repository', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('suspended', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('pushed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('rpmmanager', ['Repository'])

        # Adding model 'RPMinRepo'
        db.create_table('rpmmanager_rpminrepo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rpm', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rpmmanager.RPM'])),
            ('repo', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['rpmmanager.Repository'])),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('rpmmanager', ['RPMinRepo'])

        # Adding unique constraint on 'RPMinRepo', fields ['rpm', 'repo']
        db.create_unique('rpmmanager_rpminrepo', ['rpm_id', 'repo_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'RPMinRepo', fields ['rpm', 'repo']
        db.delete_unique('rpmmanager_rpminrepo', ['rpm_id', 'repo_id'])

        # Removing unique constraint on 'RPM', fields ['name', 'version', 'release', 'epoch', 'arch']
        db.delete_unique('rpmmanager_rpm', ['name', 'version', 'release', 'epoch', 'arch'])

        # Deleting model 'RPM'
        db.delete_table('rpmmanager_rpm')

        # Deleting model 'Repository'
        db.delete_table('rpmmanager_repository')

        # Deleting model 'RPMinRepo'
        db.delete_table('rpmmanager_rpminrepo')


    models = {
        'blobstore.datablob': {
            'Meta': {'unique_together': "(('hashtype', 'hash'),)", 'object_name': 'DataBlob'},
            'blob': ('django.db.models.fields.files.FileField', [], {'max_length': '150'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'hashtype': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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