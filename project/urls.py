from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .api import api


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]

admin.site.site_header = settings.SITE_NAME
admin.site.site_title = settings.SITE_NAME

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += path("__debug__/", include("debug_toolbar.urls")),
