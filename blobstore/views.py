from django.shortcuts import render
from django.http import HttpResponseRedirect
from models import BlobForm

def upload(request):
  if request.method == 'POST':
    form = BlobForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/')
  else:
      form = BlobForm()

  return render(request, 'blobstore_upload.html', {
      'form': form,
  })

