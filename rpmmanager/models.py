import sys, os, os.path, rpm
import subprocess, shutil

from django.db import models
from django.contrib import admin
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save, pre_save
from django.core import exceptions
from django.conf import settings

from blobstore.models import ProcessedBlob

###### RPM ######
class RPM(models.Model):
  procblob = models.OneToOneField(ProcessedBlob, primary_key=True)
  protected = models.BooleanField(default=False)
  gc = models.BooleanField(default=False)

  # Set automatically on save
  name = models.CharField(max_length=100)
  version = models.CharField(max_length=50)
  release = models.CharField(max_length=50)
  epoch = models.CharField(max_length=50,null=True,blank=True)
  arch = models.CharField(max_length=50)

  class Meta:
    unique_together = (('name', 'version', 'release', 'epoch', 'arch'),)

  def __unicode__(self):
    return self.name + '-' + self.version + '-' + self.release + '.' + self.arch

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

@receiver(post_delete, sender=RPM)
def procblob_cleaner(sender, instance, **kwargs):
  try:
    instance.procblob.delete()
  except exceptions.ObjectDoesNotExist:
    pass

###### Repo ######
class Repository(models.Model):
  name = models.CharField(max_length=64)
  suspended = models.BooleanField(default=False)
  pushed = models.DateTimeField(blank=True,null=True)
  modified = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)
  rpms = models.ManyToManyField(RPM, through='RPMinRepo', related_name='repositories')

  def get_basedir(self):
    return os.path.join(settings.MEDIA_ROOT, 'rpmmanager', self.name)

  def __unicode__(self):
    return self.name

class RepositoryAdmin(admin.ModelAdmin):
  list_display = ['name', 'suspended', 'pushed', 'modified']

admin.site.register(Repository, RepositoryAdmin)

@receiver(post_delete, sender=Repository)
def repository_cleaner(sender, instance, **kwargs):
  shutil.rmtree(instance.get_basedir())

@receiver(post_save, sender=Repository)
def repository_processor(sender, instance, **kwargs):
  basedir = instance.get_basedir()

  # Create relevent directory if it doesnt exist
  if not os.path.exists(basedir):
    os.makedirs(basedir)

  # Link the RPMS in, removing any that no longer exist
  for rpm in instance.rpms.all():
    rpmpath = os.path.join(settings.MEDIA_ROOT, rpm.get_file().name)
    newpath = os.path.join(basedir, os.path.basename(rpm.get_file().name))
    if not os.path.exists(newpath):
      os.link(rpmpath, newpath)

  # Prepare the repository
  subprocess.call(['createrepo', '-q', '--update', '--baseurl', basedir, basedir])

###### RPMinRepo ######
class RPMinRepo(models.Model):
  rpm = models.ForeignKey(RPM)
  repo = models.ForeignKey(Repository)
  added = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = (('rpm', 'repo'),)

class RPMinRepoAdmin(admin.ModelAdmin):
  list_display = ['rpm', 'repo', 'added']

admin.site.register(RPMinRepo, RPMinRepoAdmin)

@receiver(post_save, sender=RPMinRepo)
def reposave_processor(sender, instance, **kwargs):
  instance.repo.save()

