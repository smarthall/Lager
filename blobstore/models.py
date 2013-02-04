from django.db import models
from django.contrib import admin

class Blob(models.Model):
  file = models.FileField(upload_to='blobs')

admin.site.register(Blob)

