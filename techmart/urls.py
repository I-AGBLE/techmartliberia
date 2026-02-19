from django.contrib import admin
from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "TechMart Liberia Admin"
admin.site.site_title = "TechMartLibera Administrator's Portal"
admin.site.index_title = "TechMart Liberia"