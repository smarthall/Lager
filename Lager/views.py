from django.shortcuts import render
from blobstore.models import DataBlobForm

def home(request):
    form = DataBlobForm()
    return render(request, 'index.html', {'form': form})
