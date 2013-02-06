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
from django.db import IntegrityError

class DataBlob(models.Model):
  blob = models.FileField(upload_to='datablobs', max_length=150)
  hashtype = models.CharField(max_length=32, blank=True, editable=False)
  hash = models.CharField(max_length=255, blank=True, editable=False)
  mimetype = models.CharField(max_length=100, blank=True, editable=False)
  filename = models.CharField(max_length=150, blank=True, editable=False)

  class Meta:
    unique_together = (('hashtype', 'hash'),)

  def __unicode__(self):
    return self.blob.name

  def get_file(self):
    self.blob

  def blob_process(self):
    hasher = hashlib.new(settings.HASHMETHOD)
    m = magic.open(magic.MAGIC_MIME_TYPE)
    m.load()
    filename = os.path.join(settings.MEDIA_ROOT, self.blob.name)
    f = open(filename, 'rb')
    while True:
       data = f.read(8192)
       if not data:
           break
       hasher.update(data)
    self.hashtype = settings.HASHMETHOD
    self.hash = hasher.hexdigest()
    self.mimetype = m.file(filename)
    self.filename = os.path.basename(self.blob.name)

  def save(self, *args, **kwargs):
    if self.id == None: # Save the file to disk if we havent yet
      super(DataBlob, self).save(*args, **kwargs)
    self.blob_process()
    try:
      super(DataBlob, self).save(*args, **kwargs) # Call the "real" save() method.
    except IntegrityError:
      self.delete()
      raise

@receiver(post_delete, sender=DataBlob)
def blobdelete_processor(sender, instance, **kwargs):
  os.unlink(os.path.join(settings.MEDIA_ROOT, instance.blob.name))

class DataBlobForm(ModelForm):
    class Meta:
        model = DataBlob

class DataBlobAdmin(admin.ModelAdmin):
  list_display = ('filename', 'mimetype', 'hashtype', 'hash')

admin.site.register(DataBlob, DataBlobAdmin)

