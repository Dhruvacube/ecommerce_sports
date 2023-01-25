from django.urls import path
from .views import *

urlpatterns = [
    path("add_to_cart/", add_to_cart, name="add_to_cart"),
    path("product/<str:product_id>", product, name="about_product"),
    path("feedback/", feedback, name="feedback"),
    path('', home, name='home'),
]
