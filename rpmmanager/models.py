import sys, os, os.path, rpm

from django.db import models
from django.contrib import admin
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save, pre_save
from django.conf import settings

from blobstore.models import ProcessedBlob

###### RPM ######
class RPM(models.Model):
  procblob = models.OneToOneField(ProcessedBlob, primary_key=True)
  protected = models.BooleanField(default=False)
  gc = models.BooleanField(default=False)

  # Set on save
  name = models.CharField(max_length=100)
  version = models.CharField(max_length=50)
  release = models.CharField(max_length=50)
  epoch = models.CharField(max_length=50,null=True,blank=True)
  arch = models.CharField(max_length=50)

  def get_file(self):
    return self.procblob.blob.file

@receiver(post_save, sender=ProcessedBlob)
def blob_processor(sender, instance, **kwargs):
  if (instance.mimetype == 'application/x-rpm'):
    new = RPM()
    new.procblob = instance
    new.save()

@receiver(pre_save, sender=RPM)
def rpm_processor(sender, instance, **kwargs):
  """Set the RPM file referred to by the model"""
  ts = rpm.ts()
  rpm_file = os.path.join(settings.MEDIA_ROOT, instance.get_file().name)
  fdno = os.open(rpm_file, os.O_RDONLY)
  try:
      hdr = ts.hdrFromFdno(fdno)
  except rpm.error:
      fdno = os.open(rpm_file, os.O_RDONLY)
      ts.setVSFlags(rpm._RPMVSF_NOSIGNATURES)
      hdr = ts.hdrFromFdno(fdno)
  os.close(fdno)
  instance.name = hdr[rpm.RPMTAG_NAME]
  instance.version = hdr[rpm.RPMTAG_VERSION]
  instance.release = hdr[rpm.RPMTAG_RELEASE]
  instance.epoch = hdr[rpm.RPMTAG_EPOCH]
  instance.arch = hdr[rpm.RPMTAG_ARCH]

class RPMAdmin(admin.ModelAdmin):
  readonly_fields = ['gc', 'name', 'version', 'release', 'epoch', 'arch']
  list_display = ['name', 'arch', 'version', 'release', 'protected']

admin.site.register(RPM, RPMAdmin)


