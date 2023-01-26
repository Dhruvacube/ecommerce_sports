from django.urls import path
from .views import *

urlpatterns = [
    path("add_to_cart/", add_to_cart, name="add_to_cart"),
    path('remove_from_cart/', remove_from_cart, name="remove_from_cart"),
    path("product/<str:product_id>", product, name="about_product"),
    path("feedback/", feedback, name="feedback"),
    path("cart/", view_cart, name="cart"),
    path('', home, name='home'),
]
