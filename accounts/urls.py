from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetCompleteView
from django.urls import path, re_path

from . import views
from .views import PasswordResetConfirmViews, PasswordResetDoneViews, PasswordResetViews

urlpatterns = [
    path("password_reset/",
         PasswordResetViews.as_view(),
         name="password_reset"),
    path(
        "password_reset/done/",
        PasswordResetDoneViews.as_view(),
        name="password_reset_done",
    ),
    re_path(
        r"^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$",
        PasswordResetConfirmViews.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    re_path(r"^profile/$", views.view_profile, name="view_profile"),
    re_path(
        r"^changepassword/$", views.change_password, name="change_password"),
    re_path(r"^login/$", views.loginform, name="signin"),
    re_path(r"^logout/$", views.user_logout, name="signout"),
    path("signup/", views.signup, name="signup"),
    path("", include("django.contrib.auth.urls")),
]