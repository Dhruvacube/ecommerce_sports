from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include, path, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("payments/", include("payments.urls")),
    re_path(r'^filer/', include('filer.urls')),
    path('', include('main.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
