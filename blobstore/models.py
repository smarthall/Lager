from django.db import models
from django.contrib import admin

##### Blob Model #####
class Blob(models.Model):
  file = models.FileField(upload_to='blobs', max_length=150)

  def __unicode__(self):
    return self.file.name

admin.site.register(Blob)

##### ProcessedBlob Model #####
class ProcessedBlob(models.Model):
  blob = models.OneToOneField(Blob, primary_key=True)
  hashtype = models.CharField(max_length=32)
  hash = models.CharField(max_length=255)
  mimetype = models.CharField(max_length=100)
  filename = models.CharField(max_length=150)

  def __unicode__(self):
    return self.blob.file.name

admin.site.register(ProcessedBlob)

