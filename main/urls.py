from django.urls import path,re_path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    path("add_to_cart/", add_to_cart, name="add_to_cart"),
    path('remove_from_cart/', remove_from_cart, name="remove_from_cart"),
    path("product/<str:product_id>", product, name="about_product"),
    path("feedback/", feedback, name="feedback"),
    path("cart/", view_cart, name="cart"),
    path("orders/", orders, name="orders"),
    path('orders/<str:order_id>', order_details, name='order_details'),
    path('category/<str:category_name>', view_category, name='category_details'),
    re_path(r'^search/$', search, name="search"),
    path('', home, name='home'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
