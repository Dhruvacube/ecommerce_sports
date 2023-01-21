from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include, path, re_path


urlpatterns = [
    path('admin/', admin.site.urls),
    path("account/", include("accounts.urls")),
    re_path(r'^filer/', include('filer.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
