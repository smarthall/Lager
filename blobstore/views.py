from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from models import DataBlob, DataBlobForm

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

def detail(request, datablob_id):
  db = get_object_or_404(DataBlob, pk=datablob_id)
  return render(request, 'blobstore_detail.html', {'blob': db})

