

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    AgencyViewSet,
    UserViewSet,
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    ProfileAPIView,
    ChangePasswordAPIView,
    ResetPasswordAPIView,
    NotificationPreferenceAPIView,
)

app_name = "accounts"

router = DefaultRouter()

router.register(
    "users",
    UserViewSet,
    basename="users",
)

router.register(
    "agencies",
    AgencyViewSet,
    basename="agencies",
)

urlpatterns = [

    # -------------------------
    # API
    # -------------------------

    path(
        "",
        include(router.urls),
    ),

    # -------------------------
    # Authentication
    # -------------------------

    path(
        "register/",
        RegisterAPIView.as_view(),
        name="register",
    ),

    path(
        "login/",
        LoginAPIView.as_view(),
        name="login",
    ),

    path(
        "logout/",
        LogoutAPIView.as_view(),
        name="logout",
    ),

    path(
        "profile/",
        ProfileAPIView.as_view(),
        name="profile",
    ),

    path(
        "change-password/",
        ChangePasswordAPIView.as_view(),
        name="change-password",
    ),

    path(
        "reset-password/",
        ResetPasswordAPIView.as_view(),
        name="reset-password",
    ),

    path(
        "notification-preferences/",
        NotificationPreferenceAPIView.as_view(),
        name="notification-preferences",
    ),

]
