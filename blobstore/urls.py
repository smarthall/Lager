from django.conf.urls import patterns, include, url

urlpatterns = patterns('blobstore.views',
    url(r'^upload/$', 'upload'),
    url(r'^detail/(?P<datablob_id>\d+)/$', 'detail'),
)
