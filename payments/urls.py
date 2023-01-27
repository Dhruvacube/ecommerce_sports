from django.urls import path
from .views import *

urlpatterns = [
    path("verify/" , payment_stats, name="payment_stats_verify"),
]