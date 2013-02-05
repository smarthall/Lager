import os.path
import hashlib
import magic

from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django.contrib import admin
from django.conf import settings

##### Blob Model #####
class Blob(models.Model):
  file = models.FileField(upload_to='blobs', max_length=150)

  def __unicode__(self):
    return self.file.name

admin.site.register(Blob)

@receiver(post_save, sender=Blob)
def blob_processor(sender, instance, **kwargs):
  processed = ProcessedBlob(blob=instance)
  hasher = hashlib.new(settings.HASHMETHOD)
  m = magic.open(magic.MAGIC_MIME_TYPE)
  m.load()
  filename = os.path.join(settings.MEDIA_ROOT, instance.file.name)
  f = open(filename, 'rb')
  while True:
     data = f.read(8192)
     if not data:
         break
     hasher.update(data)
  processed.hashtype = settings.HASHMETHOD
  processed.hash = hasher.hexdigest()
  processed.mimetype = m.file(filename)
  processed.filename = os.path.basename(instance.file.name)
  processed.save()

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

