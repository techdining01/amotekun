from django.urls import include, path
from . import views

urlpatterns = [
    path("logout/", views.custom_logout, name="account_logout"),
    path("logged-out/", views.logged_out, name="account_logged_out"),
    path("", include("allauth.urls")),
]
