from django.db import models
from django.contrib import admin

class Blob(models.Model):
  filename = models.CharField(max_length=255)
  sha256sum = models.CharField(max_length=64)
  size = models.BigIntegerField()
  file = models.FileField(upload_to='blobs')

admin.site.register(Blob)

