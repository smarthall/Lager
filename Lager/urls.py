from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings

from django.contrib import admin
from django.contrib.sites.models import Site

admin.autodiscover()
#admin.site.unregister(Site)

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'Lager.views.home'),
    url(r'^blobstore/', include('blobstore.urls')),

    # Admin pages
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

)  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
