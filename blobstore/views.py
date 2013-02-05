from django.shortcuts import render
from django.http import HttpResponseRedirect
from models import DataBlobForm

def upload(request):
  if request.method == 'POST':
    form = DataBlobForm(request.POST, request.FILES)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/')
  else:
      form = DataBlobForm()

  return render(request, 'blobstore_upload.html', {
      'form': form,
  })

