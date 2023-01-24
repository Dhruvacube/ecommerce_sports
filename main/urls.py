from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import *

urlpatterns = [
    path("product/<str:product_id>", product, name="about_product"),
    path('', home, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
