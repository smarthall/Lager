import sys, os, os.path, rpm
import subprocess, shutil

from django.db import models
from django.contrib import admin
from django.dispatch import receiver
from django.db.models.signals import post_delete, post_save, pre_save
from django.core import exceptions
from django.conf import settings
from django.utils import timezone

from blobstore.models import DataBlob

###### RPM ######
class RPM(models.Model):
  """
  Store an RPM
  * This model is automatically created when a datablob that is an RPM is uploaded.
  * Deleting this model deleted the associated datablob
  * The fields name, version, release, epoch and arch are filled in automatically on save
  """
  procblob = models.OneToOneField(DataBlob, primary_key=True)
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

  def add_repo(self, repo):
    RPMinRepo(rpm=self, repo=repo).save()

  def process_rpm(self):
    ts = rpm.ts()
    rpm_file = os.path.join(settings.MEDIA_ROOT, self.get_file().name)
    fdno = os.open(rpm_file, os.O_RDONLY)
    try:
        hdr = ts.hdrFromFdno(fdno)
    except rpm.error:
        fdno = os.open(rpm_file, os.O_RDONLY)
        ts.setVSFlags(rpm._RPMVSF_NOSIGNATURES)
        hdr = ts.hdrFromFdno(fdno)
    os.close(fdno)
    self.name = hdr[rpm.RPMTAG_NAME]
    self.version = hdr[rpm.RPMTAG_VERSION]
    self.release = hdr[rpm.RPMTAG_RELEASE]
    self.epoch = hdr[rpm.RPMTAG_EPOCH]
    self.arch = hdr[rpm.RPMTAG_ARCH]

  def save(self, *args, **kwargs):
    self.process_rpm()
    super(RPM, self).save(*args, **kwargs) # Call the "real" save() method.


@receiver(post_save, sender=DataBlob)
def blob_processor(sender, instance, **kwargs):
  if (instance.mimetype == 'application/x-rpm'):
    new = RPM()
    new.procblob = instance
    new.save()

@receiver(post_delete, sender=RPM)
def procblob_cleaner(sender, instance, **kwargs):
  try:
    instance.procblob.delete()
  except exceptions.ObjectDoesNotExist:
    pass

###### Repo ######
class Repository(models.Model):
  """
  Represents a repository.
  * Saving the model causes the model to flush to disk and generate a repo
  * Setting suspended means that updates wont be flushed to disk
  """
  name = models.CharField(max_length=64, unique=True)
  suspended = models.BooleanField(default=False)
  pushed = models.DateTimeField(blank=True,null=True)
  modified = models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)
  rpms = models.ManyToManyField(RPM, through='RPMinRepo', related_name='repositories')

  def get_basedir(self):
    return os.path.join(settings.MEDIA_ROOT, 'rpmmanager', self.name)

  def __unicode__(self):
    return self.name

  def add_rpm(self, rpm):
    RPMinRepo(repo=self, rpm=rpm).save()

  def to_disk(self):
    if self.suspended:
      return False

    basedir = self.get_basedir()

    # Create relevent directory if it doesnt exist
    if not os.path.exists(basedir):
      os.makedirs(basedir)

    # Link the RPMS in, removing any that no longer exist
    for rpm in self.rpms.all():
      rpmpath = os.path.join(settings.MEDIA_ROOT, rpm.get_file().name)
      newpath = os.path.join(basedir, os.path.basename(rpm.get_file().name))
      if not os.path.exists(newpath):
        os.link(rpmpath, newpath)

    # Prepare the repository
    subprocess.call(['createrepo', '-q', '--update', '--baseurl', basedir, basedir])

    # Success!
    return True

  def save(self, *args, **kwargs):
    if not self.id == None:
      if self.to_disk():
        self.updated = timezone.now()
    super(Repository, self).save(*args, **kwargs) # Call the "real" save() method.

@receiver(post_delete, sender=Repository)
def repository_cleaner(sender, instance, **kwargs):
  shutil.rmtree(instance.get_basedir())

###### RPMinRepo ######
class RPMinRepo(models.Model):
  """
  The relationship between a repository and the RPMS inside
  """
  rpm = models.ForeignKey(RPM)
  repo = models.ForeignKey(Repository)
  added = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = (('rpm', 'repo'),)

@receiver(post_save, sender=RPMinRepo)
def reposave_processor(sender, instance, **kwargs):
  instance.repo.save()

# Admin objects
class RPMinRepoInline(admin.TabularInline):
  model = RPMinRepo
  extra = 1

class RPMAdmin(admin.ModelAdmin):
  readonly_fields = ['gc', 'name', 'version', 'release', 'epoch', 'arch']
  list_display = ['name', 'arch', 'version', 'release', 'protected']
  inlines = (RPMinRepoInline, )

class RepositoryAdmin(admin.ModelAdmin):
  list_display = ['name', 'suspended', 'pushed', 'modified']
  exclude = ['pushed',]
  inlines = (RPMinRepoInline, )

admin.site.register(RPM, RPMAdmin)
admin.site.register(Repository, RepositoryAdmin)

