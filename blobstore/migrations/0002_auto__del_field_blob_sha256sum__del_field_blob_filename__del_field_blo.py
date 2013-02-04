# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Blob.sha256sum'
        db.delete_column('blobstore_blob', 'sha256sum')

        # Deleting field 'Blob.filename'
        db.delete_column('blobstore_blob', 'filename')

        # Deleting field 'Blob.size'
        db.delete_column('blobstore_blob', 'size')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Blob.sha256sum'
        raise RuntimeError("Cannot reverse this migration. 'Blob.sha256sum' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Blob.filename'
        raise RuntimeError("Cannot reverse this migration. 'Blob.filename' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Blob.size'
        raise RuntimeError("Cannot reverse this migration. 'Blob.size' and its values cannot be restored.")

    models = {
        'blobstore.blob': {
            'Meta': {'object_name': 'Blob'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['blobstore']