from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name="logout"),    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('photo.urls')),
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
