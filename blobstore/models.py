import os
import os.path
import hashlib
import magic

from django.db import models
from django.contrib import admin
from django.forms import ModelForm
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save
from django.contrib import admin
from django.conf import settings
from django.core import exceptions

##### Blob Model #####
class Blob(models.Model):
  file = models.FileField(upload_to='blobs', max_length=150)

  def __unicode__(self):
    return self.file.name


class BlobForm(ModelForm):
    class Meta:
        model = Blob

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

@receiver(post_delete, sender=Blob)
def blob_filecleaner(sender, instance, **kwargs):
  os.unlink(os.path.join(settings.MEDIA_ROOT, instance.file.name))

##### ProcessedBlob Model #####
class ProcessedBlob(models.Model):
  blob = models.OneToOneField(Blob, primary_key=True)
  hashtype = models.CharField(max_length=32)
  hash = models.CharField(max_length=255)
  mimetype = models.CharField(max_length=100)
  filename = models.CharField(max_length=150)

  def __unicode__(self):
    return self.blob.file.name

class ProcessedBlobAdmin(admin.ModelAdmin):
  list_display = ('filename', 'mimetype', 'hashtype', 'hash')

@receiver(post_delete, sender=ProcessedBlob)
def blob_cleaner(sender, instance, **kwargs):
  try:
    instance.blob.delete()
  except exceptions.ObjectDoesNotExist:
    pass

admin.site.register(ProcessedBlob, ProcessedBlobAdmin)

