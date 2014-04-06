from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('photo.urls')),
    #url(r'^public/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    #url(r'^$', include('photo.urls')),
    #url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
    #        'document_root': settings.MEDIA_ROOT})

#)
# This helps displaying thumbnail.
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
